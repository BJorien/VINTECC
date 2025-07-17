import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# === Parameters ===
FRAME_SIZE = 90
LINK_LENGTH = 45
SQUARE_SIZE = 10

# === Derived Values ===
HALF_FRAME = FRAME_SIZE / 2
HALF_SQUARE = SQUARE_SIZE / 2
left_x = -HALF_FRAME
right_x = HALF_FRAME

# === Initial Square Setup ===
square_center = np.array([0.0, 0.0])  # Centered at origin
local_corners = np.array([
    [-HALF_SQUARE,  HALF_SQUARE],  # top-left
    [-HALF_SQUARE, -HALF_SQUARE],  # bottom-left
    [ HALF_SQUARE, -HALF_SQUARE],  # bottom-right
    [ HALF_SQUARE,  HALF_SQUARE],  # top-right
])
square_corners = square_center + local_corners  # Upright, unrotated

# === Carriage Positions (based on fixed link lengths from corners) ===
# For each corner, find corresponding point on rail that is 50 units away
carriage_positions = {
    "CAR1": np.array([left_x,  square_corners[0,1] + np.sqrt(LINK_LENGTH**2 - (left_x - square_corners[0,0])**2)]),
    "CAR2": np.array([left_x,  square_corners[1,1] - np.sqrt(LINK_LENGTH**2 - (left_x - square_corners[1,0])**2)]),
    "CAR3": np.array([right_x, square_corners[2,1] - np.sqrt(LINK_LENGTH**2 - (right_x - square_corners[2,0])**2)]),
    "CAR4": np.array([right_x, square_corners[3,1] + np.sqrt(LINK_LENGTH**2 - (right_x - square_corners[3,0])**2)]),
}

# === Plotting ===
fig, ax = plt.subplots()
ax.set_xlim(-HALF_FRAME, HALF_FRAME)
ax.set_ylim(-HALF_FRAME, HALF_FRAME)
ax.set_aspect('equal')
ax.grid(True)
ax.axhline(0, color='black', lw=0.5)
ax.axvline(0, color='black', lw=0.5)

# Draw vertical rails
ax.plot([left_x, left_x], [-HALF_FRAME, HALF_FRAME], 'gray', linestyle='--')
ax.plot([right_x, right_x], [-HALF_FRAME, HALF_FRAME], 'gray', linestyle='--')

# Draw carriages
for name, pos in carriage_positions.items():
    ax.plot(*pos, 'ro')
    ax.text(pos[0] + (0.5 if pos[0] < 0 else -2.0), pos[1] + 1.5, name, fontsize=9, color='darkred')

# Draw links
for carriage_pos, corner_pos in zip(carriage_positions.values(), square_corners):
    ax.plot([carriage_pos[0], corner_pos[0]], [carriage_pos[1], corner_pos[1]], 'k--')

# Draw square
square_patch = patches.Polygon(square_corners, closed=True, edgecolor='blue', facecolor='lightblue', linewidth=2)
ax.add_patch(square_patch)

plt.title(f"Centered Upright Square (size={SQUARE_SIZE}) with Links (L={LINK_LENGTH})")
plt.show()
