from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Error: Could not open webcam.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Get the dimensions of the frame
        height, width, _ = frame.shape

        # Determine the size of the square (1:1 aspect ratio)
        square_size = min(height, width)

        # Calculate the cropping coordinates
        x_start = (width - square_size) // 2
        y_start = (height - square_size) // 2
        x_end = x_start + square_size
        y_end = y_start + square_size

        # Crop the frame to a square
        square_frame = frame[y_start:y_end, x_start:x_end]

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', square_frame)
        frame = buffer.tobytes()

        # Yield the frame as part of a multipart HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)