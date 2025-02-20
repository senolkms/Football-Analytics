import numpy as np

def read_positions(file_path):
    positions = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split(',')
            if len(values) == 2:  # Top için sadece x, y var
                x, y = map(float, values)
                positions.append((x, y))  # Sadece x, y kaydedilir
            elif len(values) == 3:  # Oyuncu için x, y, roi_area var
                x, y, roi_area = map(float, values)
                positions.append((x, y, roi_area))  # Alanı da kaydet
            else:
                print(f"Geçersiz satır: {line.strip()}")  # Hatalı satırı yazdır
    return positions

def main():
    player_positions = read_positions('outputs/txt_outputs/player_positions.txt')
    ball_positions = read_positions('outputs/txt_outputs/ball_coordinates_final.txt')  # Top koordinat dosyası
    interaction_count = 0

    # Her saniye için etkileşimleri kontrol et (30 karede bir)
    for frame_idx in range(0, min(len(player_positions), len(ball_positions)), 30):
        player_center = player_positions[frame_idx][:2]  # Sadece x, y koordinatlarını al
        ball_center = ball_positions[frame_idx]

        # Mesafeyi hesapla
        distance = np.linalg.norm(np.array(player_center) - np.array(ball_center))

        # Mesafe eşiğini kontrol et (roi_area'yı 1000'e bölerek kullan)
        adjusted_roi_area = player_positions[frame_idx][2] / 25.0  # Dönüşüm
        if distance <= adjusted_roi_area:
            interaction_count += 1

    print(f"Toplam etkileşim sayısı: {interaction_count}")

if __name__ == "__main__":  # Düzeltildi
    main()