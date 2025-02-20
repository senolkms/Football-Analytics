# FootballAnalytics

Futbol maç videolarından oyuncu ve top hareketlerini analiz eden bir yazılım.

### Programlama Dili
- Python

### Temel Kütüphaneler
- OpenCV (cv2): Video işleme ve görüntü analizi
- NumPy: Matematiksel işlemler ve array manipülasyonu
- CUDA: GPU hızlandırma (opsiyonel)
- PyTorch: Derin öğrenme modelleri için
- TorchVision: Görüntü işleme modelleri

### Kullanılan Teknikler
- Nesne Tespiti (Object Detection)
- Nesne Takibi (Object Tracking)
- Homografik Dönüşüm
- Koordinat Sistemi Dönüşümleri
- Hız ve Mesafe Hesaplamaları

### Ana Dosyalar
- `main.py`: Tüm modülleri sırayla çalıştıran ana orkestrasyon dosyası
- `4points_in_the_image.py`: Saha kalibrasyonu için görüntü üzerinde 4 referans noktası belirleme
- `4points_in_the_video.py`: Video üzerinde belirlenen 4 noktayı takip etme
- `track_and_save_coordinates.py`: Oyuncu ve top koordinatlarını takip edip kaydetme
- `map_of_the_player.py`: Oyuncuların saha üzerindeki hareket haritasını oluşturma
- `homographic_poses.py`: Saha görüntüsünü kuş bakışı perspektife dönüştürme
- `speed_data.py`: Oyuncuların hız verilerini hesaplama ve analiz etme
- `ball_optimization.py`: Top hareketlerini optimize etme ve düzenleme
- `ball_test.py`: Top takip sisteminin test edilmesi
- `player_ball_interaction.py`: Oyuncu-top etkileşimlerini analiz etme
- `ball_loses.py`: Top kayıplarını analiz etme
