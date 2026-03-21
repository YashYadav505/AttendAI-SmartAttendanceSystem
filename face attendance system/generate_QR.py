import qrcode
import socket

# Get your local IP automatically
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# URL for the Flask app
url = f"http://{local_ip}:5000/"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

# Save the QR code
img.save("attendance_qr.png")
print(f"QR Generated! Scan to open: {url}")