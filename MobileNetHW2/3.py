import matplotlib.pyplot as plt
import numpy as np

k = 1.38e-23
T = 273 + 27
BandWidth = 10e6
Pt_dbm = 33
G_trans = 14
G_rec = 14
h_base = 1.5 + 50
h_device = 1.5
sigma = 6
R = 500
D = 500 * (3 ** 0.5)
ISD = 500

Pt = 10 ** ((Pt_dbm - 30) / 10)
Gt = 10 ** (G_trans / 10)
Gr = 10 ** (G_rec / 10)
N = k * T * BandWidth

num_devices = 50
hex_radius = 250 * 2 / np.sqrt(3)


def in_hexagon(x, y, radius):
    if np.abs(y) > radius * (np.sqrt(3) / 2) and np.abs(x) < 0.5 * radius:
        return False
    if np.abs(x) > radius - np.abs(y) * (1 / np.sqrt(3)):
        return False
    else:
        return True


def generate_points_in_hexagon(num_points, radius):
    x_points = []
    y_points = []

    while len(x_points) < num_points:

        y = np.random.uniform(-radius * np.sqrt(3) / 2, radius * np.sqrt(3) / 2)
        x = np.random.uniform(-radius, radius)

        if in_hexagon(x, y, radius):
            x_points.append(x)
            y_points.append(y)

    return np.array(x_points), np.array(y_points)


def received_power_two_ray(d):
    return Pt * Gr * Gt * (h_device * h_base) ** 2 / (d ** 4)


def hexagon_vertices(side_length, original):
    return [
        (original[0] + side_length * np.cos(np.pi / 3 * i), original[1] + side_length * np.sin(np.pi / 3 * i))
        for i in range(6)
    ]


def hexagonal_grid(ISD):
    coords = [(0, 0)]  # 中心點
    for i in range(6):
        angle = -np.pi / 6 + (np.pi / 3 * i)
        x = np.cos(angle) * ISD
        y = np.sin(angle) * ISD
        coords.append((x, y))

    for i in range(6):
        angle = (np.pi / 3 * i)
        x = np.cos(angle) * ISD * np.sqrt(3)
        y = np.sin(angle) * ISD * np.sqrt(3)
        coords.append((x, y))

    for i in range(6):
        angle = (-np.pi / 6 + np.pi / 3 * (i + 1))
        x = np.cos(angle) * 1000
        y = np.sin(angle) * 1000
        coords.append((x, y))

    return np.array(coords)


x_devices, y_devices = generate_points_in_hexagon(num_devices, hex_radius)
distances_base = np.sqrt(x_devices ** 2 + y_devices ** 2)

Pr = received_power_two_ray(distances_base)
Pr_db = 10 * np.log10(Pr)

bs0_coords = hexagonal_grid(ISD)
bs_coords = np.delete(bs0_coords, 0, 0)


def calculate_power_indiff_bs(x_devices, y_devices, bs_coords):
    Pr_power = []
    distances = []

    for i in range(0, len(bs_coords)):
        x_chunk = x_devices[i]
        y_chunk = y_devices[i]
        x_bs, y_bs = bs_coords[i]
        distances_to_bs = np.sqrt((x_chunk - x_bs) ** 2 + (y_chunk - y_bs) ** 2)
        distances.append(distances_to_bs)  # 儲存距離
        power = received_power_two_ray(distances_to_bs)
        Pr_power.append(power)
    Pr_power1 = np.concatenate(Pr_power)
    distances = np.concatenate(distances)
    Pr_power_db = 10 * np.log10(Pr_power1)
    return Pr_power_db, distances, Pr_power1


x_values = [point[0] for point in bs0_coords]
y_values = [point[1] for point in bs0_coords]

random_points_x = []
random_points_y = []


for i in range(18):
    random_point_x, random_point_y = generate_points_in_hexagon(num_devices, hex_radius)
    random_points_x.append(x_values[i+1] + random_point_x)
    random_points_y.append(y_values[i+1] + random_point_y)


Power_db, distances, Pr_power = calculate_power_indiff_bs(random_points_x, random_points_y, bs_coords)

interference = []
PPr = np.concatenate((Pr, Pr_power))

distances_base = np.array(distances_base)
distances = np.array(distances)
Distances = np.concatenate((distances_base, distances))

x_all = np.concatenate([x_devices, np.concatenate(random_points_x)])
y_all = np.concatenate([y_devices, np.concatenate(random_points_y)])


def calculate_power_interference(bs_coords):
    distance = np.sqrt((x_all - bs_coords[0]) ** 2 + (y_all - bs_coords[1]) ** 2)
    bs_power = received_power_two_ray(distance)
    bs_powers = np.sum(bs_power)
    return bs_powers


for i in range(19):
    sum = calculate_power_interference(bs0_coords[i])
    for power in PPr[50 * i:50 * (i+1)]:
        interference.append(10 * np.log10(power / (sum-power+N)))

plt.figure(figsize=(8, 6))
vertices = []
for i in bs0_coords:
    vertices.append(hexagon_vertices(hex_radius, i))
for i, vertex in enumerate(vertices):
    hexagon = plt.Polygon(vertex, fill=None, edgecolor='red', label='Hexagon' if i == 0 else "")
    plt.gca().add_patch(hexagon)
plt.scatter(x_values, y_values, color='red', label='BS', marker='x', s=100)
plt.scatter(x_devices, y_devices, color='blue', label='Mobile Devices', marker='o', s=10)
plt.scatter(random_points_x, random_points_y, color='orange', label='Mobile Devices', marker='o', s=10)
plt.title('Location of Central BS and Mobile Devices')
plt.xlabel('x-axis (meters)')
plt.ylabel('y-axis (meters)')
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()

plt.figure(figsize=(8, 6))
plt.title('Received Power vs. Distance from Central BS')
plt.scatter(distances, Power_db, color='blue')
plt.xlabel('Distance (meters)')
plt.ylabel('Received_Power (dB)')
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
plt.title('SINR vs. Distance from Central BS')
plt.scatter(Distances, interference, color='blue',s=5)
plt.xlabel('Distance (meters)')
plt.ylabel('SINR (dB)')
plt.grid(True)
plt.show()
