import cv2
from ultralytics import YOLO
import torch

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

roi = cv2.selectROI('Frame', frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

x, y, w, h = roi

# Oyuncunun seçtiği alanın alanını hesapla
roi_area = w * h  # Seçilen dikdörtgenin alanı

tracker = cv2.TrackerCSRT_create()
tracker.init(frame, (x, y, w, h))

output_file = 'outputs/txt_outputs/player_positions.txt'

with open(output_file, 'w') as f:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Tespit işlemi
        #results = model(frame)  # Frame üzerinde nesne tespiti yapar

        success, bbox = tracker.update(frame)

        if success:
            x, y, w, h = [int(v) for v in bbox]
            center_x = x + w / 2
            center_y = y + h / 2
            f.write(f"{center_x},{center_y},{roi_area}\n")  # Alanı da kaydet

cap.release()
cv2.destroyAllWindows()