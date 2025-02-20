import numpy as np
import cv2


def calculate_homography(src_points, dst_points):
    h, status = cv2.findHomography(src_points, dst_points)
    return h


def apply_homography(h, points):
    transformed_points = cv2.perspectiveTransform(points.reshape(-1, 1, 2), h)
    return transformed_points.reshape(-1, 2)


def write_coordinates_to_file(file_path, coordinates):
    with open(file_path, 'w') as file:
        for coord in coordinates:
            file.write(f"{coord[0]}, {coord[1]}\n")


def read_coordinates_from_file(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            coordinates.append([x, y])
    return np.array(coordinates, dtype="float32")

video_points = read_coordinates_from_file("outputs/txt_outputs/video_selected_points.txt")

# MANCHESTER CITY ETIHAD STADIUM SIZES - we will found them from internet, may be wrong :)
world_points = np.array([
    [0, 0],
    [0, 68],
    [105, 68],
    [105, 0]
], dtype="float32")

h_matrix = calculate_homography(video_points, world_points)

player_positions = read_coordinates_from_file('outputs/txt_outputs/player_positions.txt')

transformed_positions = apply_homography(h_matrix, player_positions)

write_coordinates_to_file('outputs/txt_outputs/homographic_positions.txt', transformed_positions)