# ============================================================
#   visualiser.py  —  All matplotlib drawing.
#
#   Reads joint angles from Leg objects and draws.
#   Zero logic here — pure rendering.
#   Delete this file and replace with CoppeliaSim code if you want to move to real hardware.
# ============================================================

import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from kinematics import forward_positions
from config import (SIDE, AXIS_LIMIT, GROUND_LEVEL,
                    STEP_LENGTH, SHOW_TRAIL, SHOW_CIRCLE, TIMESTEP)


# Leg segment colours
COLOURS = {
    'coxa' : 'red',
    'femur': 'green',
    'tibia': 'blue',
}

LEG_COLOURS = {
    'R1': 'darkorange',
    'R2': 'royalblue',
    'L1': 'forestgreen',
    'L2': 'orchid',
}


class Visualiser:

    def __init__(self):
        self.fig = plt.figure(figsize=(10, 8))
        self.ax  = self.fig.add_subplot(111, projection='3d')
        self.stop_flag = {'stop': False}
        self.fig.canvas.mpl_connect('key_press_event', self._on_key)

    def _on_key(self, event):
        if event.key == 'q':
            self.stop_flag['stop'] = True
            plt.close(self.fig)

    def is_running(self):
        return not self.stop_flag['stop']

    # ── Call at start of every frame ─────────────────────────
    def begin_frame(self):
        self.ax.cla()
        self._draw_body()
        self._draw_ground()

    # ── Call at end of every frame ───────────────────────────
    def end_frame(self):
        self.ax.set_xlim(-AXIS_LIMIT, AXIS_LIMIT)
        self.ax.set_ylim(-AXIS_LIMIT, AXIS_LIMIT)
        self.ax.set_zlim(-AXIS_LIMIT, AXIS_LIMIT)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title("Quadruped Simulation  |  press Q to quit")
        plt.draw()
        plt.pause(TIMESTEP)

    # ── Draw one leg from a Leg object ───────────────────────
    def draw_leg(self, leg):
        """
        Reads leg.theta_c / theta_f / theta_ti and draws coxa, femur, tibia.
        Also draws trail if enabled.
        """
        base = leg.base
        coxa_end, femur_end, tibia_end = forward_positions(
            base, leg.theta_c, leg.theta_f, leg.theta_ti
        )
        col = LEG_COLOURS[leg.name]

        # Coxa
        self.ax.plot([base[0],     coxa_end[0]],
                     [base[1],     coxa_end[1]],
                     [base[2],     coxa_end[2]],
                     color=COLOURS['coxa'], linewidth=3, marker='o')
        # Femur
        self.ax.plot([coxa_end[0],  femur_end[0]],
                     [coxa_end[1],  femur_end[1]],
                     [coxa_end[2],  femur_end[2]],
                     color=COLOURS['femur'], linewidth=3, marker='o')
        # Tibia
        self.ax.plot([femur_end[0], tibia_end[0]],
                     [femur_end[1], tibia_end[1]],
                     [femur_end[2], tibia_end[2]],
                     color=COLOURS['tibia'], linewidth=3, marker='x')

        # Trail
        if SHOW_TRAIL and len(leg.trail) > 1:
            xs, ys, zs = zip(*leg.trail)
            self.ax.plot(xs, ys, zs, color=col, linestyle='-', linewidth=1, alpha=0.5)

        # Step circle
        if SHOW_CIRCLE:
            circle_x = leg.base[0] + leg.reach
            circle_y = leg.base[1]
            self._draw_step_circle(circle_x, circle_y, col)

        # Leg label
        self.ax.text(tibia_end[0], tibia_end[1], tibia_end[2] + 1,
                     leg.name, fontsize=8, color=col, ha='center')

    # ── Body square ──────────────────────────────────────────
    def _draw_body(self):
        corners = [
            [ SIDE/2,  SIDE/2, 0],
            [-SIDE/2,  SIDE/2, 0],
            [-SIDE/2, -SIDE/2, 0],
            [ SIDE/2, -SIDE/2, 0],
            [ SIDE/2,  SIDE/2, 0],
        ]
        xs = [c[0] for c in corners]
        ys = [c[1] for c in corners]
        zs = [c[2] for c in corners]
        self.ax.plot(xs, ys, zs, color='brown', linewidth=3, marker='o')

        # Forward arrow
        self.ax.quiver(0, 0, 0, 0, SIDE*0.6, 0,
                       color='black', arrow_length_ratio=0.3, linewidth=2)
        self.ax.text(0, SIDE*0.7, 0.5, 'FWD', fontsize=8, ha='center')

    # ── Ground plane (simple) ─────────────────────────────────
    def _draw_ground(self):
        s = 25
        xx, yy = np.meshgrid([-s, s], [-s, s])
        zz = np.full_like(xx, GROUND_LEVEL, dtype=float)
        self.ax.plot_surface(xx, yy, zz, alpha=0.08, color='gray')

    # ── Step circle under foot ───────────────────────────────
    def _draw_step_circle(self, bx, by, color):
        angles = np.linspace(0, 2*np.pi, 60)
        r = STEP_LENGTH / 2
        xs = bx + r * np.cos(angles)
        ys = by + r * np.sin(angles)
        zs = np.full_like(xs, GROUND_LEVEL)
        self.ax.plot(xs, ys, zs, color=color, linestyle='--', linewidth=0.8, alpha=0.5)