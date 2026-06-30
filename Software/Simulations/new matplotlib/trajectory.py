# ============================================================
#   trajectory.py  —  Foot path math
#   KEY IDEA: Everything uses phase (0.0 → 1.0)
#
#   0.0 ──────── 0.7 ──────── 1.0
#   |   STANCE   |   SWING   |
#   foot on ground           foot in air
# ============================================================

import math
import numpy as np
from config import STEP_LENGTH, STEP_HEIGHT, GROUND_LEVEL


STANCE_RATIO = 0.7      # 70% of cycle = stance (foot on ground)
SWING_RATIO  = 0.3      # 30% of cycle = swing  (foot in air)


def get_foot_position(phase, theta_rotation_deg, x_center):
    """
    Given a phase (0.0 → 1.0), returns the foot's (x, y, z)
    in leg-local frame.

    phase              : float 0.0 → 1.0, position in gait cycle
    theta_rotation_deg : direction of travel (0=forward, 90=right, etc.)
    x_center           : how far forward the leg reaches

    Returns: (x, y, z)
    """
    gamma = math.radians(theta_rotation_deg)
    r     = STEP_LENGTH / 2

    # The two endpoints of the step
    x_start = x_center + r * math.sin(gamma)
    y_start =            r * math.cos(gamma)

    x_end   = x_center - r * math.sin(gamma)
    y_end   =           -r * math.cos(gamma)

    if phase < STANCE_RATIO:
        # ── Stance: foot drags from start → end along ground ──
        t = phase / STANCE_RATIO           # 0.0 → 1.0 within stance
        x = x_start + t * (x_end - x_start)
        y = y_start + t * (y_end - y_start)
        z = GROUND_LEVEL

        """
        else:
            # ── Swing: foot lifts from end → start through arc ────
            t = (phase - STANCE_RATIO) / SWING_RATIO   # 0.0 → 1.0 within swing
            x = x_end + t * (x_start - x_end)
            y = y_end + t * (y_start - y_end)

            # Cosine arc for smooth lift and land
            # cos goes from -1 → +1 → -1 as t goes 0 → 0.5 → 1
            z = STEP_HEIGHT * math.cos((t - 0.5) * math.pi * 2) * (0.5) \
                + STEP_HEIGHT * 0.5 + GROUND_LEVEL
        """

    else:
        t = (phase - STANCE_RATIO) / SWING_RATIO   # 0 → 1 within swing

        x = x_end + t * (x_start - x_end)
        y = y_end + t * (y_start - y_end)

        # angle sweeps from -pi/2 to +pi/2 as t goes 0 -> 1
        angle = (t - 0.5) * math.pi
        z = STEP_HEIGHT * math.cos(angle) + GROUND_LEVEL

    return x, y, z


def get_step_endpoints(theta_rotation_deg, x_center):
    """
    Returns the two foot endpoints for a given direction.
    Useful for drawing the step circle/line in visualiser.
    """
    gamma = math.radians(theta_rotation_deg)
    r     = STEP_LENGTH / 2

    x_start = x_center + r * math.sin(gamma)
    y_start =            r * math.cos(gamma)
    x_end   = x_center - r * math.sin(gamma)
    y_end   =           -r * math.cos(gamma)

    return (x_start, y_start, GROUND_LEVEL), (x_end, y_end, GROUND_LEVEL)


# ── Standalone test ───────────────────────────────────────────
if __name__ == '__main__':
    print("Trajectory self-test (phase 0.0 → 1.0, forward direction):")
    for p in [0.0, 0.3, 0.6, 0.8, 1.0]:
        x, y, z = get_foot_position(p, theta_rotation_deg=0, x_center=12)
        print(f"  phase={p:.1f}  →  x={x:+6.2f}  y={y:+6.2f}  z={z:+6.2f}")