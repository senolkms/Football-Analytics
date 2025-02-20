import cv2

image_path = 'input_media/sahafoto.png'
image = cv2.imread(image_path)

if image is None:
    print("Image couldn't be read.")
    exit()

cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', image)

points = []

def select_point(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Image', image)
        if len(points) == 4:
            cv2.destroyAllWindows()


cv2.setMouseCallback('Image', select_point)
cv2.waitKey(0)

if len(points) != 4:
    print("4 point didn't choose. Program closing.")
    exit()

print("Choosed points:")
for i, point in enumerate(points):
    print(f"Point {i + 1}: {point}")

with open('outputs/txt_outputs/image_selected_points.txt', 'w') as f:
    for point in points:
        f.write(f"{point[0]},{point[1]}\n")

cv2.imwrite('outputs/img_outputs/image_selected_points.png', image)