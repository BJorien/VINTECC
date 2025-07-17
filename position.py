import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# === Frame Settings ===
frame_size = 90
half_frame = frame_size / 2
link_length = 50
square_size = frame_size / 20  # small, for clarity

# === Carriage Vertical Positions (editable) ===
CAR1 = 10
CAR2 = -5
CAR3 = -3
CAR4 = 15

# === Rail X positions ===
left_x = -half_frame
right_x = half_frame

# === Carriage positions ===
carriages = {
    "CAR1": np.array([left_x,  CAR1]),  # top-left
    "CAR2": np.array([left_x,  CAR2]),  # bottom-left
    "CAR3": np.array([right_x, CAR3]),  # bottom-right
    "CAR4": np.array([right_x, CAR4]),  # top-right
}

# === Local square corner coordinates (centered, square_size side) ===
local_corners = np.array([
    [-square_size/2,  square_size/2],  # top-left
    [-square_size/2, -square_size/2],  # bottom-left
    [ square_size/2, -square_size/2],  # bottom-right
    [ square_size/2,  square_size/2],  # top-right
])

# === Solve for position: center + rotation ===
# We'll find a center and rotation angle so that each corner is 50 units from each carriage

# Simplify: average carriage positions → use as initial square center
square_center = np.mean(list(carriages.values()), axis=0)

# Search for a rotation angle that minimizes the error in link lengths
def rotated_corners(center, angle_rad):
    R = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                  [np.sin(angle_rad),  np.cos(angle_rad)]])
    return center + local_corners @ R.T

def total_link_error(center, angle_rad):
    corners = rotated_corners(center, angle_rad)
    error = 0
    for corner, carriage in zip(corners, carriages.values()):
        dist = np.linalg.norm(corner - carriage)
        error += (dist - link_length) ** 2
    return error

# Brute-force search for a good rotation angle (fast enough for one frame)
angles = np.linspace(0, 2 * np.pi, 360)
best_error = float('inf')
best_angle = 0
for angle in angles:
    err = total_link_error(square_center, angle)
    if err < best_error:
        best_error = err
        best_angle = angle

# Final square corners
square_corners = rotated_corners(square_center, best_angle)

# === Plot ===
fig, ax = plt.subplots()
ax.set_xlim(-half_frame, half_frame)
ax.set_ylim(-half_frame, half_frame)
ax.set_aspect('equal')
ax.grid(True)
ax.axhline(0, color='black', lw=0.5)
ax.axvline(0, color='black', lw=0.5)

# Draw rails
ax.plot([left_x, left_x], [-half_frame, half_frame], 'gray', linestyle='--')
ax.plot([right_x, right_x], [-half_frame, half_frame], 'gray', linestyle='--')

# Draw carriages
for name, pos in carriages.items():
    ax.plot(*pos, 'ro')
    ax.text(pos[0] + (0.5 if pos[0] < 0 else -2.0), pos[1] + 1.5, name, fontsize=9, color='darkred')

# Draw links (from carriages to corners)
for carriage_pos, corner_pos in zip(carriages.values(), square_corners):
    ax.plot([carriage_pos[0], corner_pos[0]], [carriage_pos[1], corner_pos[1]], 'k--')

# Draw square
square_patch = patches.Polygon(square_corners, closed=True, edgecolor='blue', facecolor='lightblue', linewidth=2)
ax.add_patch(square_patch)

plt.title("Movable Square with Fixed-Length Links (L=50)")
plt.show()
