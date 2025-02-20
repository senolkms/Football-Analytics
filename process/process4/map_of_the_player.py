import cv2
import numpy as np


def read_coordinates_from_file(file_path):
    coordinatess = []
    with open(file_path, 'r') as file:
        for linee in file:
            xx, yy = map(float, linee.strip().split(','))
            coordinatess.append([xx, yy])
    return np.array(coordinatess, dtype="float32")


video_points = read_coordinates_from_file("outputs/txt_outputs/video_selected_points.txt")

image_points = read_coordinates_from_file("outputs/txt_outputs/image_selected_points.txt")

H, status = cv2.findHomography(video_points, image_points)


def apply_homography(xxx, yyy, HH):
    point = np.array([[xxx, yyy]], dtype="float32")
    point = np.array([point])
    transformed_point = cv2.perspectiveTransform(point, HH)
    return transformed_point[0][0]


image_path = 'input_media/sahafoto.png'
image = cv2.imread(image_path)

if image is None:
    print("Image couldn't be read.")
    exit()

coordinates = []
with open('outputs/txt_outputs/player_positions.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        x, y = map(float, line.strip().split(','))
        coordinates.append((x, y))

marker_path = 'input_media/marker.png'
marker = cv2.imread(marker_path, cv2.IMREAD_UNCHANGED)

if marker is None:
    print("Marker couldn't be read.")
    exit()

marker_size = (5, 5)
marker = cv2.resize(marker, marker_size, interpolation=cv2.INTER_AREA)


def add_marker(imagee, point, markerr):
    xxxx, yyyy = point
    mh, mw = markerr.shape[0], markerr.shape[1]

    top_left_x = int(xxxx - mw / 2)
    top_left_y = int(yyyy - mh / 2)

    img_h, img_w = imagee.shape[0], imagee.shape[1]

    if top_left_x < 0:
        top_left_x = 0
    if top_left_y < 0:
        top_left_y = 0
    if top_left_x + mw > img_w:
        mw = img_w - top_left_x
        markerr = markerr[:, :mw]
    if top_left_y + mh > img_h:
        mh = img_h - top_left_y
        markerr = markerr[:mh, :]

    if markerr.shape[2] == 4:
        alpha_mask = markerr[:, :, 3] / 255.0
        alpha_image = 1.0 - alpha_mask

        for c in range(0, 3):

            imagee[top_left_y:top_left_y + mh, top_left_x:top_left_x + mw, c] = (
                    alpha_mask * markerr[:, :, c] +
                    alpha_image * imagee[top_left_y:top_left_y + mh, top_left_x:top_left_x + mw, c]
            )

            imagee[top_left_y:top_left_y + mh, top_left_x:top_left_x + mw, c] = np.clip(
                imagee[top_left_y:top_left_y + mh, top_left_x:top_left_x + mw, c] * (1 + alpha_mask),
                0, 255
            )


for coord in coordinates:
    transformed_coord = apply_homography(coord[0], coord[1], H)
    add_marker(image, tuple(map(int, transformed_coord)), marker)

resized_image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))

cv2.namedWindow('Image with Markers', cv2.WINDOW_NORMAL)
cv2.imshow('Image with Markers', resized_image)
cv2.imwrite('outputs/img_outputs/last_output.png', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
