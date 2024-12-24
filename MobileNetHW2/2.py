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
D = 500*(3**0.5)
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


P_receive = received_power_two_ray(distances)
P_receive_db = 10 * np.log10(P_receive)
SINRs = []

def calcculate_interference_power(D):
    sum = np.sum(D)
    print(sum)
    for i in range(num_devices):
        SINR = D[i]/(sum-D[i]+N)
        SINR_db = 10* np.log10(SINR)
        SINRs.append(SINR_db)
calcculate_interference_power(P_receive)


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

plt.figure(figsize=(8, 6))
plt.title('Received Power vs. Distance from Central BS')
plt.scatter(distances, P_receive_db, color='blue')
plt.xlabel('Distance (meters)')
plt.ylabel('Received_Power (dB)')
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
plt.title('SINR vs. Distance from Central BS')
plt.scatter(distances, SINRs, color='blue')
plt.xlabel('Distance (meters)')
plt.ylabel('SINR (dB)')
plt.grid(True)
plt.show()

