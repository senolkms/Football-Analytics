import numpy as np
import matplotlib.pyplot as plt


def read_coordinates_from_file(file_path):
    coordinates = []
    with open(file_path, 'r') as filee:
        for line in filee:
            x, y = map(float, line.strip().split(','))
            coordinates.append([x, y])
    return np.array(coordinates, dtype="float32")


def write_distances_to_file(file_path, distancess):
    with open(file_path, 'w') as filee:
        for distance in distancess:
            filee.write(f"{distance:.2f}\n")


def write_velocities_to_file(file_path, velocitiess):
    with open(file_path, 'w') as filee:
        for velocity in velocitiess:
            filee.write(f"{velocity:.2f}\n")


def calculate_distances(points):
    distancess = []
    for ii in range(len(points) - 1):
        distance = np.linalg.norm(points[ii + 1] - points[ii])
        distancess.append(distance)
    return distancess


def calculate_velocities(distancess, fpss):
    velocitiess = [distance / (1 / fpss) for distance in distancess]
    return velocitiess


def read_velocities_from_file(file_path):
    velocitiess = []
    with open(file_path, 'r') as filee:
        for line in filee:
            velocity = float(line.strip())
            velocitiess.append(velocity)
    return velocitiess


transformed_positions = read_coordinates_from_file('outputs/txt_outputs/homographic_positions.txt')

distances = calculate_distances(transformed_positions)

write_distances_to_file('outputs/txt_outputs/distances.txt', distances)

with open('outputs/txt_outputs/distances.txt', 'r') as file:
    data = [float(line.strip()) for line in file]

mean = np.mean(data)
std_dev = np.std(data)

threshold = 3
for i in range(1, len(data)):
    if abs(data[i] - mean) > threshold * std_dev:
        data[i] = data[i - 1]

mean = np.mean(data)
std_dev = np.std(data)

print(f"Standart Sapma: {std_dev}")

threshold = 3
for i in range(1, len(data)):
    if abs(data[i] - mean) > threshold * std_dev:
        data[i] = data[i - 1]

total_distance = 0.00

for i in range(1, len(data)):
    total_distance += data[i]

total_distance = total_distance / 1000
total_distance = "{:.3f}".format(total_distance)

print(f"Total run data of the player: {total_distance} km")

fps = 30

velocities = calculate_velocities(data, fps)
velocities = [x * 3.6 for x in velocities]

write_velocities_to_file('outputs/txt_outputs/velocities.txt', velocities)

velocities = read_velocities_from_file('outputs/txt_outputs/velocities.txt')

time_intervals = np.arange(len(velocities)) / fps

interval = 10
selected_indices = np.arange(0, len(velocities), interval)
selected_velocities = np.array(velocities)[selected_indices]
selected_times = time_intervals[selected_indices]

plt.figure(figsize=(10, 6))
plt.plot(selected_times, selected_velocities, linestyle='-', color='b')
plt.title('Player Velocity Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Velocity (km/h)')
plt.grid(True)
plt.savefig('outputs/img_outputs/velocity_graph.png')
