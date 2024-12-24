import random
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

# Define parameters
min_speed = 1  # Minimum speed (m/s)
max_speed = 15  # Maximum speed (m/s)
min_t = 1  # Minimum travel time (s)
max_t = 6  # Maximum travel time (s)
total_time = 900  # Total simulation time (s)
hex_radius = 500  # Radius of hexagonal cell (m)

num_devices = 50
hex_radius = 250 * 2 / np.sqrt(3)
handoff_log = []


def in_hexagon(x, y, radius):
    if np.abs(y) > radius * (np.sqrt(3) / 2) and np.abs(x) < 0.5 * radius:
        return False
    if np.abs(x) > radius - np.abs(y) * (1 / np.sqrt(3)):
        return False
    else:
        return True


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


cells = hexagonal_grid(ISD)
bs_coords = np.delete(cells, 0, 0)


def get_current_cell(x, y, cells):
    distances = [np.sqrt((x - cx) ** 2 + (y - cy) ** 2) for (cx, cy) in cells]
    return np.argmin(distances) + 1  #返回索引


time = 0
x, y = 250, 0
current_cell = get_current_cell(x, y, cells)
handoff = 0

moving_x = []
moving_y = []
while time < total_time:
    direction = random.uniform(0, 2 * np.pi)
    speed = random.uniform(min_speed, max_speed)
    travel_time = random.uniform(min_t, max_t)

    dx = speed * np.cos(direction) * travel_time
    dy = speed * np.sin(direction) * travel_time
    x += dx
    y += dy
    moving_x.append(x)
    moving_y.append(y)
    time += travel_time

    new_cell = get_current_cell(x, y, cells)


    if new_cell != current_cell:
        handoff_log.append(f"{int(time)}s {current_cell} {new_cell}")
        handoff += 1
        current_cell = new_cell  # Update to the new cell

print(handoff)
x_values = [point[0] for point in cells]
y_values = [point[1] for point in cells]

print(handoff_log)

plt.figure(figsize=(8, 6))
vertices = []
for i in cells:
    vertices.append(hexagon_vertices(hex_radius, i))
for i, vertex in enumerate(vertices):
    hexagon = plt.Polygon(vertex, fill=None, edgecolor='red', label='Hexagon' if i == 0 else "")
    plt.gca().add_patch(hexagon)

plt.scatter(x_values, y_values, color='red', label='BS', marker='x', s=1)
for i, (x, y) in enumerate(cells):
    plt.text(x, y, str(i + 1), color='blue', ha='center', va='center', fontsize=12)
plt.xlabel('x-axis (meters)')
plt.ylabel('y-axis (meters)')
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()
