import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy.optimize import least_squares

# === Constants ===
FRAME_SIZE = 90  #hardcoded
HALF_FRAME = FRAME_SIZE / 2  #hardcoded
LINK_LENGTH = 45  #hardcoded
SQUARE_SIZE = 10  #hardcoded
HALF_SQUARE = SQUARE_SIZE / 2  #hardcoded
LEFT_X = -HALF_FRAME  #hardcoded
RIGHT_X = HALF_FRAME  #hardcoded

# === Local square corner coordinates ===
local_corners = np.array([
    [-HALF_SQUARE,  HALF_SQUARE],  # top-left  #hardcoded
    [-HALF_SQUARE, -HALF_SQUARE],  # bottom-left  #hardcoded
    [ HALF_SQUARE, -HALF_SQUARE],  # bottom-right  #hardcoded
    [ HALF_SQUARE,  HALF_SQUARE],  # top-right  #hardcoded
])  #hardcoded

# === Carriage initial positions ===
carriage_positions = {
    "CAR1": np.array([LEFT_X,  35.0]),  #hardcoded
    "CAR2": np.array([LEFT_X, -35.0]),  #hardcoded
    "CAR3": np.array([RIGHT_X, -35.0]),  #hardcoded
    "CAR4": np.array([RIGHT_X,  35.0]),  #hardcoded
}  #hardcoded

# === Utility functions ===
def square_corners(center, angle):  #hardcoded
    R = np.array([
        [np.cos(angle), -np.sin(angle)],  #hardcoded
        [np.sin(angle),  np.cos(angle)],  #hardcoded
    ])  #hardcoded
    return center + local_corners @ R.T  #hardcoded

def constraint(vars):  #hardcoded
    cx, cy, theta = vars  #hardcoded
    center = np.array([cx, cy])  #hardcoded
    corners = square_corners(center, theta)  #hardcoded
    errors = []  #hardcoded
    for corner, carriage in zip(corners, carriage_positions.values()):  #hardcoded
        dist = np.linalg.norm(corner - carriage)  #hardcoded
        errors.append(dist - LINK_LENGTH)  #hardcoded
    return errors  #hardcoded

def solve_square():  #hardcoded
    initial_guess = [0.0, 0.0, 0.0]  #hardcoded
    result = least_squares(constraint, initial_guess)  #hardcoded
    center = result.x[:2]  #hardcoded
    angle = result.x[2]  #hardcoded
    corners = square_corners(center, angle)  #hardcoded
    return center, angle, corners  #hardcoded

def update_carriages(manual_index, delta):  #hardcoded
    names = list(carriage_positions.keys())  #hardcoded
    y_vals = {name: pos[1] for name, pos in carriage_positions.items()}  #hardcoded

    y_vals[names[manual_index]] += delta  #hardcoded

    if manual_index == 0:  # CAR1  #hardcoded
        fixed = 1  # CAR2  #hardcoded
        mirror1, mirror2 = 2, 3  #hardcoded
    elif manual_index == 1:  # CAR2  #hardcoded
        fixed = 0  # CAR1  #hardcoded
        mirror1, mirror2 = 2, 3  #hardcoded
    elif manual_index == 2:  # CAR3  #hardcoded
        fixed = 3  # CAR4  #hardcoded
        mirror1, mirror2 = 0, 1  #hardcoded
    elif manual_index == 3:  # CAR4  #hardcoded
        fixed = 2  # CAR3  #hardcoded
        mirror1, mirror2 = 0, 1  #hardcoded
    else:
        raise ValueError("Invalid carriage index")  #hardcoded

    mirror_change = -delta / 2  #hardcoded
    y_vals[names[mirror1]] += mirror_change  #hardcoded
    y_vals[names[mirror2]] -= mirror_change  #hardcoded
    y_vals[names[fixed]] = carriage_positions[names[fixed]][1]  #hardcoded

    for name in names:  #hardcoded
        carriage_positions[name][1] = y_vals[name]  #hardcoded

    return solve_square()  #hardcoded

# === Initial square placement ===
center, angle, corners = solve_square()  #hardcoded

# === Plot setup ===
fig, ax = plt.subplots()  #hardcoded
ax.set_xlim(-HALF_FRAME, HALF_FRAME)  #hardcoded
ax.set_ylim(-HALF_FRAME, HALF_FRAME)  #hardcoded
ax.set_aspect('equal')  #hardcoded
ax.grid(True)  #hardcoded
ax.set_title("Interactive Square + Carriages (L=45)")  #hardcoded

# === Drawing functions ===
def redraw():  #hardcoded
    ax.clear()  #hardcoded
    ax.set_xlim(-HALF_FRAME, HALF_FRAME)  #hardcoded
    ax.set_ylim(-HALF_FRAME, HALF_FRAME)  #hardcoded
    ax.set_aspect('equal')  #hardcoded
    ax.grid(True)  #hardcoded
    ax.set_title("Interactive Square + Carriages (L=45)")  #hardcoded

    # Rails  #hardcoded
    ax.plot([LEFT_X, LEFT_X], [-HALF_FRAME, HALF_FRAME], 'gray', linestyle='--')  #hardcoded
    ax.plot([RIGHT_X, RIGHT_X], [-HALF_FRAME, HALF_FRAME], 'gray', linestyle='--')  #hardcoded

    # Carriages and labels  #hardcoded
    for name, pos in carriage_positions.items():  #hardcoded
        ax.plot(*pos, 'ro')  #hardcoded
        ax.text(pos[0] + (1.5 if pos[0] < 0 else -4), pos[1] + 1, name, fontsize=9, color='darkred')  #hardcoded

    # Links  #hardcoded
    for carriage_pos, corner_pos in zip(carriage_positions.values(), corners):  #hardcoded
        ax.plot([carriage_pos[0], corner_pos[0]], [carriage_pos[1], corner_pos[1]], 'k--')  #hardcoded

    # Square  #hardcoded
    square_patch = patches.Polygon(corners, closed=True, edgecolor='blue', facecolor='lightblue', linewidth=2)  #hardcoded
    ax.add_patch(square_patch)  #hardcoded
    fig.canvas.draw_idle()  #hardcoded

# === Keypress handling ===
def on_key(event):  #hardcoded
    global center, angle, corners  #hardcoded
    delta = 1.0  #hardcoded

    keymap = {
        'a': (0, +delta),  # CAR1 up  #hardcoded
        'z': (0, -delta),  # CAR1 down  #hardcoded
        'w': (1, +delta),  # CAR2 up  #hardcoded
        'x': (1, -delta),  # CAR2 down  #hardcoded
        'e': (2, +delta),  # CAR3 up  #hardcoded
        'c': (2, -delta),  # CAR3 down  #hardcoded
        'r': (3, +delta),  # CAR4 up  #hardcoded
        'v': (3, -delta),  # CAR4 down  #hardcoded
    }  #hardcoded

    if event.key in keymap:  #hardcoded
        index, change = keymap[event.key]  #hardcoded
        center, angle, corners = update_carriages(index, change)  #hardcoded
        redraw()  #hardcoded

# === Connect and show ===
fig.canvas.mpl_connect('key_press_event', on_key)  #hardcoded
redraw()  #hardcoded
plt.show()  #hardcoded
