import cv2
import torch

# CUDA'nın kullanılabilirliğini kontrol edin
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Koordinat dosyasının yolu
coordinate_file_path = 'outputs/txt_outputs/ball_coordinates_final.txt'

# Koordinatları okuyun
with open(coordinate_file_path, 'r') as file:
    coordinates = [tuple(map(float, line.strip().split(','))) for line in file]

# Koordinatları PyTorch tensörüne dönüştürün ve GPU'ya taşıyın
coordinates_tensor = torch.tensor(coordinates, device=device)

# Video dosyasının yolu
input_video_path = 'input_media/videobu2.mp4'
output_video_path = 'output_video.mp4'

# Video dosyasını açın
video_capture = cv2.VideoCapture(input_video_path)

# Video özelliklerini alın
fps = video_capture.get(cv2.CAP_PROP_FPS)
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Çıktı video dosyasını oluşturun
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

frame_idx = 0
while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    if frame_idx < coordinates_tensor.size(0):
        x, y = coordinates_tensor[frame_idx].tolist()
        # Markörü ekleyin (kırmızı renkte ve çapı iki katına çıkarılmış)
        cv2.circle(frame, (int(x), int(y)), 10, (0, 0, 255), -1)  # Kırmızı renk (BGR: 0, 0, 255), çap 10

    # İşlenen kareyi çıktı video dosyasına yazın
    video_writer.write(frame)

    # Hangi karede olduğunu çıktı verin
    print(f"Kare {frame_idx} işlendi.")

    frame_idx += 1

# Her şeyi serbest bırakın
video_capture.release()
video_writer.release()
