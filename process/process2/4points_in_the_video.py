import cv2
import torch
from ultralytics import YOLO

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def load_model(model_pathh):
    modell = YOLO(model_pathh)
    modell.to(device)
    return modell

model_path = 'best.pt'
model = load_model(model_path)

video_path = 'input_media/videobu2.mp4'
cap = cv2.VideoCapture(video_path)

ret, frame = cap.read()

if not ret:
    print("Video couldn't be read.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.imshow('Frame', frame)

points = []

def select_point(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Frame', frame)
        if len(points) == 4:
            cv2.destroyAllWindows()

cv2.setMouseCallback('Frame', select_point)
cv2.waitKey(0)

if len(points) != 4:
    print("4 points didn't choose. Program is closing.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

print("Choosed points:")
for i, point in enumerate(points):
    print(f"Point {i + 1}: {point}")

with open('outputs/txt_outputs/video_selected_points.txt', 'w') as f:
    for point in points:
        f.write(f"{point[0]},{point[1]}\n")

cap.release()
cv2.destroyAllWindows()