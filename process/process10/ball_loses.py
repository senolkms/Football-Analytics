import numpy as np
import cv2

# Oyuncu ve takım bilgilerini içeren bir yapı
players = {}

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

def determine_possession(teamA_positions, teamB_positions, ball_position, threshold=50.0):
    for player_id, player_pos in enumerate(teamA_positions, start=1):
        player_center = player_pos[:2]
        distance = np.linalg.norm(np.array(player_center) - np.array(ball_position))
        if distance <= threshold:
            return player_id, 'TeamA'
    
    for player_id, player_pos in enumerate(teamB_positions, start=1):
        player_center = player_pos[:2]
        distance = np.linalg.norm(np.array(player_center) - np.array(ball_position))
        if distance <= threshold:
            return player_id, 'TeamB'
    
    return None, None

def select_team(event, x, y, flags, param):
    global points, team, frame, teamA_players_positions, teamB_players_positions
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 11:
            points.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Frame', frame)
        if len(points) == 11:
            cv2.destroyAllWindows()
            team = input("Enter team name for selected points (TeamA/TeamB): ")
            if team == 'TeamA':
                for point in points:
                    teamA_players_positions.append((point[0], point[1], team))
            elif team == 'TeamB':
                for point in points:
                    teamB_players_positions.append((point[0], point[1], team))
            points.clear()

def main():
    global frame, points, teamA_players_positions, teamB_players_positions, team
    points = []
    teamA_players_positions = []
    teamB_players_positions = []
    team = None

    video_path = 'input_media/videobu2.mp4'
    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()
    if not ret:
        print("Video couldn't be read.")
        cap.release()
        cv2.destroyAllWindows()
        exit()

    # İlk kareyi sakla
    initial_frame = frame.copy()

    # İlk takımın oyuncularını seç
    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.imshow('Frame', frame)
    cv2.setMouseCallback('Frame', select_team)
    cv2.waitKey(0)

    # İkinci takımın oyuncularını seç
    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.imshow('Frame', frame)
    cv2.setMouseCallback('Frame', select_team)
    cv2.waitKey(0)

    # Oyuncu pozisyonlarını dosyaya kaydet
    with open('outputs/txt_outputs/teamA_player_positions.txt', 'w') as fA, open('outputs/txt_outputs/teamB_player_positions.txt', 'w') as fB:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Burada oyuncu pozisyonlarını tespit eden bir kod olmalı
            # Örneğin, bir nesne tespit modeli kullanarak oyuncu pozisyonlarını tespit edebilirsiniz
            # Bu örnekte, oyuncu pozisyonlarını rastgele oluşturuyoruz
            for pos in teamA_players_positions:
                x, y = pos[0], pos[1]
                fA.write(f"{x},{y},{"TeamA"}\n")

            for pos in teamB_players_positions:
                x, y = pos[0], pos[1]
                fB.write(f"{x},{y},{team}\n")

    ball_positions = read_positions('outputs/txt_outputs/ball_coordinates_final.txt')
    
    possession_history = []
    current_possession = None
    ball_loss_count = {'TeamA': 0, 'TeamB': 0}

    for frame_idx in range(0, min(len(ball_positions), len(ball_positions))):
        ball_position = ball_positions[frame_idx]
        player_id, team = determine_possession(teamA_players_positions, teamB_players_positions, ball_position)
        
        if player_id is not None:
            if current_possession is None:
                current_possession = team
            elif current_possession != team:
                ball_loss_count[current_possession] += 1
                current_possession = team

        possession_history.append(current_possession)

    print(f"Top kayıpları: {ball_loss_count}")

if __name__ == "__main__":
    main()