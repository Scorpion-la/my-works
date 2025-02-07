from ultralytics import YOLO
import cv2
import math
import time


CAMERA_INDEX = 0
TARGET_FPS = 40
HUMAN_PRESENT_DURATION = 5
CONFIDENCE_THRESHOLD = 0.5


model = YOLO("yolo-Weights/yolov8n.pt")


cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    raise IOError(f"Cannot open webcam at index {CAMERA_INDEX}")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))



human_detected = False
last_detection_time = 0
prev_frame_time = 0
new_frame_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or webcam disconnected.")
        break

    new_frame_time = time.time()


    results = model(frame, stream=True, conf=CONFIDENCE_THRESHOLD)

    human_in_frame = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = float(box.conf[0])
            cls = int(box.cls[0])
            class_name = model.names[cls]

            if class_name == "person":
                human_in_frame = True


                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    if human_in_frame and not human_detected:
        print("Human Detected!")
        human_detected = True
        last_detection_time = time.time()

    elif not human_in_frame:
        human_detected = False


    if human_detected and time.time() - last_detection_time < HUMAN_PRESENT_DURATION:
        cv2.putText(frame, "Human Present", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)


    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('.'):
        break

cap.release()
cv2.destroyAllWindows()