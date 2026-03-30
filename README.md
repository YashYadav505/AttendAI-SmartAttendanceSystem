# 📸 Smart Attendance System

A **Smart Attendance System** that uses AI-based **face recognition** to automatically mark student attendance using a camera. The system detects faces, matches them with a stored database, and records attendance in real-time—removing the need for manual attendance.

---

## 🚀 Features

- 🎯 Real-time face recognition
- 📷 Camera-based student detection
- 🧠 AI-powered face matching (DeepFace / FaceNet / OpenCV)
- 🗂️ Student database integration (MongoDB / JSON)
- 📊 Automatic attendance marking
- 🧾 Student details display after recognition
- 🔒 Secure data handling
- 🌐 Web-based interface (React + Node.js / Python backend)

---

![Smart Attendance System]('demo.png')
## 🏗️ Project Structure

```bash
face attendance-system/
│
├── static/ # Node.js + Express backend
│ ├── server.js
|
├── studentsPhoto/              # Stores students profile pic
│ ├── student1.png
│ ├── student2.png
│ ├── student3.png
│ ├── student4.png
│ └── student5.png
│
├── templates/ # Face recognition AI logic
│ ├── app.py
│ ├── attendance_qr.py
│ ├── generate_QR.py
│ 
│
├── README.md
└── index.html
```

---

## 🛠️ Tech Stack

### Frontend
- React.js
- HTML5, CSS3
- JavaScript
- Axios

### Backend
- Node.js
- Express.js
- MongoDB (Mongoose)

### AI / ML
- Python
- OpenCV
- DeepFace / FaceNet
- NumPy, Pandas

---

## ⚙️ How It Works

1. Admin stores student details (name, ID, photo).
2. AI model encodes and saves face features.
3. Camera captures live video.
4. System detects faces in real-time.
5. AI compares faces with database.
6. If matched:
   - Attendance is marked
   - Student details are shown on UI
7. Data is saved in logs/database.

---

## 📦 Installation Guide

### 1. Clone Repository
```bash
git clone https://github.com/your-username/smart-attendance-system.git
cd smart-attendance-system
```
---

### 1. Setting frontend
```bash
cd frontend
npm install
npm start
```
###2. Setting backend
```bash
cd backend
npm install
node server.js
```
3. Setting ai model
```bash
cd ai-model
pip install -r requirements.txt
python model.py
```
