from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
from pymongo import MongoClient
import os
import base64
from datetime import datetime
from flask_cors import CORS


result = DeepFace.verify(
    "captured.jpg",
    "studentsPhotos/S25010106507.jpeg",
    enforce_detection=False
)
print(result)

app = Flask(__name__)
CORS(app)  # enable CORS for all origins

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["attendance"]
students_col = db["students"]
attendance_col = db["attendance"]

# Folder where student images are stored
STUDENT_IMAGES = os.path.join(os.getcwd(), "studentsPhotos")
print("Looking for images in:", STUDENT_IMAGES)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    image_data = data.get('image')
    if not image_data:
        return jsonify({"status": "error", "message": "No image received"})

    # Save captured image
    try:
        img_data = base64.b64decode(image_data.split(',')[1])
    except Exception as e:
        return jsonify({"status": "error", "message": "Invalid image format"})

    captured_path = "captured.jpg"
    with open(captured_path, "wb") as f:
        f.write(img_data)

    # Loop through students
    for student in students_col.find():
        student_id = student.get("student_id")
        filename = student.get("image")
        if not filename:
            continue

        student_img = os.path.join(STUDENT_IMAGES, filename)
        if not os.path.exists(student_img):
            print("Student image not found:", student_img)
            continue

        try:
            result = DeepFace.verify(
                img1_path=captured_path,
                img2_path=student_img,
                enforce_detection=False
            )

            if result["verified"]:
                today = datetime.now().strftime("%Y-%m-%d")
                exists = attendance_col.find_one({"student_id": student_id, "date": today})

                if exists:
                    return jsonify({
                        "status": "already_marked",
                        "name": student.get("name"),
                        "student_id": student_id
                    })

                # Mark attendance
                attendance_col.insert_one({
                    "student_id": student_id,
                    "name": student.get("name"),
                    "Section": student.get("Section"),
                    "Branch": student.get("Branch"),
                    "Course": student.get("Course"),
                    "year": student.get("year"),
                    "semester": student.get("semester"),
                    "date": today,
                    "time": datetime.now().strftime("%H:%M:%S")
                })

                return jsonify({
                    "status": "success",
                    "name": student.get("name"),
                    "student_id": student_id,
                    "Section": student.get("Section"),
                    "Branch": student.get("Branch"),
                    "Course": student.get("Course"),
                    "year": student.get("year"),
                    "semester": student.get("semester")
                })

        except Exception as e:
            print("DeepFace error:", e)
            continue

    return jsonify({"status": "not_found"})




if __name__ == '__main__':
    app.run(debug=True)