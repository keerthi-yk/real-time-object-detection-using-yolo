import cv2
import time
import pyttsx3
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # You can use yolov8s.pt for better accuracy if needed

# Constants
KNOWN_WIDTH = 20  # in cm
FOCAL_LENGTH = 615  # in pixels

# Initialize TTS engine
tts = pyttsx3.init()

def speak(text):
    print("object:", text)
    tts.say(text)
    tts.runAndWait()

def estimate_distance(known_width, focal_length, pixel_width):
    return (known_width * focal_length) / pixel_width if pixel_width != 0 else 0

def get_position(center_x, frame_width):
    if center_x < frame_width / 3:
        return "Left"
    elif center_x > 2 * frame_width / 3:
        return "Right"
    else:
        return "Center"

def detect_objects(duration=60):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Camera not detected.")
        return

    print("[INFO] Starting Object Detection. Press 'q' to quit.")
    end_time = time.time() + duration

    while time.time() < end_time:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w = x2 - x1
            center_x = x1 + w // 2
            label = model.names[int(box.cls[0])]
            distance = estimate_distance(KNOWN_WIDTH, FOCAL_LENGTH, w)
            position = get_position(center_x, frame.shape[1])

            # Draw box and text
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label}", (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.putText(frame, f"{distance:.1f} cm", (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"{position}", (x1, y1 - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            speak(f"{label} detected on {position} at {distance:.1f} centimeters")

        cv2.imshow("Object Detection", frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run object detection directly
if __name__ == "__main__":
    detect_objects()
