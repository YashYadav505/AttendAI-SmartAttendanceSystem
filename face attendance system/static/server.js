console.log("server.js loaded");

let video = document.getElementById("video");
let button = document.getElementById("startBtn");
let resultBox = document.getElementById("result");
let stream = null;
let scanning = false;

button.onclick = async function() {
    if (scanning) return;
    scanning = true;

    resultBox.innerHTML = "📷 Starting camera...";
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        video.onloadedmetadata = () => {
            resultBox.innerHTML = "📸 Look at the camera... Capturing in 3s";
            setTimeout(captureImage, 3000);
        };
    } catch (err) {
        console.error("Camera error:", err);
        resultBox.innerHTML = "❌ Camera access denied";
        scanning = false;
    }
};

function captureImage() {
    let canvas = document.createElement("canvas");
    canvas.width = 320;
    canvas.height = 240;
    let ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    let image = canvas.toDataURL("image/jpeg");
    resultBox.innerHTML = "⏳ Scanning face...";

    sendToBackend(image);
    stopCamera();  // stop camera immediately after capture
}

function sendToBackend(image) {
    fetch("http://127.0.0.1:5000/mark_attendance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: image })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);

        if (data.status === "success") {
            resultBox.innerHTML = `✅ ${data.name} (${data.student_id})<br>
                                   ${data.Section}, ${data.Branch}<br>
                                   ${data.Course}, Year ${data.year}, Sem ${data.semester}<br>
                                   Attendance Marked`;
        } else if (data.status === "already_marked") {
            resultBox.innerHTML = `⚠️ ${data.name}<br>Already Marked`;
        } else if (data.status === "not_found") {
            resultBox.innerHTML = "❌ Face Not Recognized";
        } else {
            resultBox.innerHTML = "❌ Unknown error";
        }
        scanning = false;
    })
    .catch(error => {
        console.error("Fetch error:", error);
        resultBox.innerHTML = "❌ Server error";
        scanning = false;
    });
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
        console.log("Camera stopped");
    }
}