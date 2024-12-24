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

# 六邊形邊長
hex_radius = 250 * 2 / np.sqrt(3)


def in_hexagon(x, y, radius):

    if np.abs(y) > radius * (np.sqrt(3)/2) and np.abs(x) < 0.5*radius:
        return False
    if np.abs(x) > radius - np.abs(y) * (1/np.sqrt(3)):
        return False
    else:
        return True

def hexagon_vertices(side_length):
    return [
        (side_length * np.cos(np.pi / 3 * i), side_length * np.sin(np.pi / 3 * i))
        for i in range(6)
    ]


def generate_points_in_hexagon(num_points, radius):
    x_points = []
    y_points = []

    while len(x_points) < num_points:

        x = np.random.uniform(-radius * np.sqrt(3) / 2, radius * np.sqrt(3) / 2)
        y = np.random.uniform(-radius, radius)

        if in_hexagon(x, y, radius):
            x_points.append(x)
            y_points.append(y)

    return np.array(x_points), np.array(y_points)


x_devices, y_devices = generate_points_in_hexagon(num_devices, hex_radius)

def received_power_two_ray(d):
    return Pt * Gr * Gt * (h_device * h_base) ** 2 / (d ** 4)


distances = np.sqrt(x_devices ** 2 + y_devices ** 2)
for index in distances:
    if index >= 250:
        print(index)

Pr = received_power_two_ray(distances)
Pr_db = 10 * np.log10(Pr)


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
        angle = (-np.pi / 6+ np.pi / 3 * (i+1))
        x = np.cos(angle) * 1000
        y = np.sin(angle) * 1000
        coords.append((x, y))

    return np.array(coords)


bs_coords = hexagonal_grid(ISD)
bs_coords = np.delete(bs_coords, 0, 0)


def calculate_interference(x_devices, y_devices, bs_coords):
    interference_power = np.zeros(len(x_devices))
    for x_bs, y_bs in bs_coords:
        distances_to_bs = np.sqrt((x_devices - x_bs) ** 2 + (y_devices - y_bs) ** 2)
        Pr_interference = received_power_two_ray(distances_to_bs)
        interference_power += Pr_interference
    return interference_power


interference_power = calculate_interference(x_devices, y_devices, bs_coords)
SINR = Pr / (interference_power + N)
SINR_dB = 10 * np.log10(SINR)

plt.figure(figsize=(6, 6))
vertices = hexagon_vertices(hex_radius)
hexagon = plt.Polygon(vertices, fill=None, edgecolor='red', label='Hexagon')
plt.gca().add_patch(hexagon)
plt.scatter(0, 0, color='red', marker='x', s=200, label='Central BS')
plt.scatter(x_devices, y_devices, color='blue', label='Mobile Devices')
plt.title('Location of Central BS and Mobile Devices')
plt.xlabel('x-axis (meters)')
plt.ylabel('y-axis (meters)')
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()

# Plot the base stations
plt.figure(figsize=(8, 6))
plt.scatter(distances, Pr_db, color='green', label='Power(dB)')
plt.title('Received Power vs. Distance from Central BS')
plt.xlabel('Distance (meters)')
plt.ylabel('Received_Power (dB)')
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(6, 6))
plt.scatter(distances, SINR_dB, color='blue')
plt.xlabel("Distance from Central BS (meters)")
plt.ylabel("SINR (dB)")
plt.title("SINR vs Distance")
plt.grid(True)
plt.show()




