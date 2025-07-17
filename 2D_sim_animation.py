import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.interpolate import splprep, splev

from simulation_base import (
    plot_frame,
    plot_side_axes,
    plot_origin,
    plot_point_P,
    plot_y_crosses,
    H, B, l  # constants
)

x_start, y_start = (-B/2 + 10, -H/2 + 10)  
TOTAL_FRAMES = 500

def defined_path(frame, x0, y0):
    total_frames = TOTAL_FRAMES
    corner2 = (x0, y0)                     # Start (under left)
    corner4 = (B/2 - 10, H/2 - 10)           # Upper right
    corner3 = (B/2 - 10, -H/2 + 10)          # Lower right
    corner1 = (-B/2 + 10, H/2 - 10)          # Upper left
    origin = (0, 0)

    waypoints = [corner2, corner4, origin, corner1, corner3]
    waypoints_np = np.array(waypoints).T

    tck, _ = splprep(waypoints_np, s=0, k=2)

    u = np.linspace(0, 1, total_frames)
    out = splev(u, tck)

    positions = list(zip(out[0], out[1]))

    # Return position for the current frame
    return positions[frame]

fig, ax = plt.subplots(figsize=(6, 9))
fig.patch.set_facecolor('black')


animation_mode = 'once'  # could be 'once', 'loop', or 'stopped'
frame_counter = 0
ani = None  # will hold the FuncAnimation object

def update(frame):
    global frame_counter, animation_mode

    ax.clear()
    ax.set_facecolor('black')

    # Draw static elements
    plot_frame(ax, B, H)
    plot_side_axes(ax, B, H)
    plot_origin(ax)

    # Get point position
    x_P, y_P = defined_path(frame, x_start, y_start)

    # Plot point
    plot_point_P(ax, x_P, y_P)

    # Plot red crosses + check bounds
    in_bounds = plot_y_crosses(ax, x_P, y_P, B, H)

    if not in_bounds:
        print(f"STOP: P is out of bounds at frame {frame} (x={x_P:.2f}, y={y_P:.2f})")
        ani.event_source.stop()  # Freeze plot

    # Style
    ax.set_xlim(-B/2, B/2)
    ax.set_ylim(-H/2, H/2)
    ax.set_aspect('equal')
    ax.set_title("Moving Point Simulation", color='white')
    ax.tick_params(colors='white')

    # One-time stop condition
    if animation_mode == 'once' and frame_counter >= TOTAL_FRAMES:
        ani.event_source.stop()
    frame_counter += 1

def on_key(event):
    global ani, animation_mode, frame_counter

    if event.key == 's':
        print("Stopping and closing the window.")
        plt.close(fig)

    elif event.key == 'p':
        print("Playing animation once.")
        animation_mode = 'once'
        frame_counter = 0
        ani.event_source.stop()
        ani.frame_seq = ani.new_frame_seq()
        ani.event_source.start()

    elif event.key == 'l':
        print("Playing in infinite loop.")
        animation_mode = 'loop'
        ani.event_source.stop()
        ani.frame_seq = ani.new_frame_seq()
        ani.event_source.start()

fig.canvas.mpl_connect('key_press_event', on_key)

animation_mode = 'once'
save = True

ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=100, repeat=False)

if save:
    ani.save("animation_cross.gif", writer="pillow")
else:
    plt.show()


