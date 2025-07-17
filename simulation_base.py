import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root_scalar

# Constantes
H = 100  # Hoogte
B = 56   # Breedte
l = 100



def plot_frame(ax, B, H):
    """Teken de rechthoekige frame-rand in het wit."""
    left = -B / 2
    bottom = -H / 2
    frame = plt.Rectangle((left, bottom), B, H,
                          edgecolor='white', facecolor='none', linewidth=2)
    ax.add_patch(frame)

def plot_side_axes(ax, B, H):
    """Teken de verticale assen langs de zijkanten."""
    left = -B / 2
    right = B / 2
    ax.plot([left, left], [-H/2, H/2], linestyle='--', color='white', linewidth=1)
    ax.plot([right, right], [-H/2, H/2], linestyle='--', color='white', linewidth=1)
    ax.plot([left], [0], 'wo')   # midden links
    ax.plot([right], [0], 'wo')  # midden rechts

def plot_origin(ax):
    """Markeer de oorsprong en assen."""
    ax.plot(0, 0, 'wo')  # oorsprong
    ax.axhline(0, color='grey', linewidth=0.5)
    ax.axvline(0, color='grey', linewidth=0.5)

    def point_relative_to_corners(x_P, y_P, B, H):
    # Corner coordinates
        corners = {
            "top_left": (-B/2, H/2),
            "top_right": (B/2, H/2),
            "bottom_left": (-B/2, -H/2),
            "bottom_right": (B/2, -H/2),
        }

        # P relative to each corner = P_origin - corner
        rel_coords = {}
        for name, (x_c, y_c) in corners.items():
            x_rel = x_P - x_c
            y_rel = y_P - y_c
            rel_coords[name] = (x_rel, y_rel)
        
        return rel_coords

def plot_point_P(ax, x_P, y_P):
    ax.plot(x_P, y_P, 'ro')  # red point for P
    ax.text(x_P + 2, y_P, "P", color='red')

def plot_y_crosses(ax, x_P, y_P, B, H):

    # P relative to the corners
    x1_P = B / 2 + x_P
    y1_P = H / 2 - y_P
    d1 = np.sqrt(x1_P**2 + y1_P**2)
    x2_P = B / 2 + x_P
    y2_P = H / 2 + y_P
    d2 = np.sqrt(x2_P**2 + y2_P**2)
    x3_P = B / 2 - x_P
    y3_P = H / 2 + y_P
    d3 = np.sqrt(x3_P**2 + y3_P**2)
    x4_P = B / 2 - x_P
    y4_P = H / 2 - y_P
    d4 = np.sqrt(x4_P**2 + y4_P**2)

    ds = [d1, d2, d3, d4]

    if not all(d < l for d in ds):
        print("This point is out of bounds (l is too short)")
        return False

    # Apply your formulas
    y1 = 50 - (l - np.sqrt(x1_P**2 + y1_P**2))
    y2 = (l - np.sqrt(x2_P**2 + y2_P**2)) - 50
    y3 = (l - np.sqrt(x3_P**2 + y3_P**2)) - 50
    y4 = 50 - (l - np.sqrt(x4_P**2 + y4_P**2))

    ys = [y1, y2, y3, y4]

    if not all(-50 <= y <= 50 for y in ys):
        print("This point is out of bounds (y_max reached)")
        return False
    if (abs(y1) + abs(y2)) <= 10:
        print("This point is out of bounds (the rollers touch)")
        return False
    if (abs(y3) + abs(y4)) <= 10:
        print("This point is out of bounds (the rollers touch)")
        return False
    

    # X-positions of vertical sides
    left_x = -B / 2
    right_x = B / 2

    # Plot red crosses
    ax.plot([left_x], [y1], 'rx', markersize=10, markeredgewidth=2)
    ax.plot([left_x], [y2], 'rx', markersize=10, markeredgewidth=2)
    ax.plot([right_x], [y3], 'rx', markersize=10, markeredgewidth=2)
    ax.plot([right_x], [y4], 'rx', markersize=10, markeredgewidth=2)


    return True
 

def main():
    fig, ax = plt.subplots(figsize=(6, 9))

    # Zwarte achtergrond
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Plotonderdelen
    plot_frame(ax, B, H)
    plot_side_axes(ax, B, H)
    plot_origin(ax)

    # Define point P
    x_P = 10
    y_P = 10

    # Plot point P
    plot_point_P(ax, x_P, y_P)

    # Plot red crosses for y1..y4
    plot_y_crosses(ax, x_P, y_P, B, H)

    # Uiterlijk
    ax.set_title("2D Frame", color='white')
    ax.set_xlabel("X", color='white')
    ax.set_ylabel("Y", color='white')
    ax.tick_params(colors='white')
    ax.set_aspect('equal')
    ax.grid(True, color='gray')

    plt.show()



if __name__ == "__main__":
    main()

