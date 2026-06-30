# ============================================================
#   kinematics.py  —  Does the math thingy
# ============================================================

import math
from config import COXA, FEMUR, TIBIA


def invkin(x, y, z):
    """
    Inverse kinematics for a 3-DOF leg.
    Given foot target (x, y, z) in leg-local frame,
    returns joint angles in DEGREES.

    Returns:
        (theta_coxa, theta_femur, theta_tibia) in degrees
        None if target is unreachable
    """
    # ── Coxa: rotation at base, in XY plane ──────────────────
    theta_c_rad = math.atan2(y, x)
    theta_c     = math.degrees(theta_c_rad)

    # ── Project remaining distance into side-view plane ───────
    x1    = x - COXA * math.cos(theta_c_rad)
    y1    = y - COXA * math.sin(theta_c_rad)
    x_new = math.sqrt(x1**2 + y1**2)

    # ── Distance from femur pivot to foot ─────────────────────
    L     = math.sqrt(x_new**2 + z**2)
    alpha = math.degrees(math.atan2(z, x_new))

    # ── Femur angle (cosine rule) ─────────────────────────────
    term1 = (FEMUR**2 + L**2 - TIBIA**2) / (2 * FEMUR * L)
    if not (-1 <= term1 <= 1):
        return None     # unreachable
    theta_f = math.degrees(math.acos(term1)) + alpha

    # ── Tibia angle (cosine rule) ─────────────────────────────
    term2 = (FEMUR**2 + TIBIA**2 - L**2) / (2 * FEMUR * TIBIA)
    if not (-1 <= term2 <= 1):
        return None     # unreachable
    theta_ti = math.degrees(math.acos(term2))

    return theta_c, theta_f, theta_ti


def forward_positions(base, theta_c, theta_f, theta_ti):
    """
    Forward kinematics — given joint angles, returns the 3D
    positions of coxa-end, femur-end, and tibia-end (foot).
    Used by the visualiser to draw the leg segments.

    base       : [x, y, z] leg attachment point on body
    theta_*    : joint angles in DEGREES

    Returns:
        coxa_end, femur_end, tibia_end  — each a [x, y, z] list
    """
    c_rad = math.radians(theta_c)
    f_rad = math.radians(theta_f)

    # Coxa end
    coxa_end = [
        base[0] + COXA * math.cos(c_rad),
        base[1] + COXA * math.sin(c_rad),
        base[2]
    ]

    # Femur end
    femur_end = [
        coxa_end[0] + FEMUR * math.cos(f_rad) * math.cos(c_rad),
        coxa_end[1] + FEMUR * math.cos(f_rad) * math.sin(c_rad),
        coxa_end[2] + FEMUR * math.sin(f_rad)
    ]

    # Tibia end (foot)
    fk_deg = theta_f + theta_ti - 180
    fk_rad = math.radians(fk_deg)
    tibia_end = [
        femur_end[0] + TIBIA * math.cos(fk_rad) * math.cos(c_rad),
        femur_end[1] + TIBIA * math.cos(fk_rad) * math.sin(c_rad),
        femur_end[2] + TIBIA * math.sin(fk_rad)
    ]

    return coxa_end, femur_end, tibia_end


# ── Standalone test ───────────────────────────────────────────
if __name__ == '__main__':
    test_points = [
        (12, 0, -10),
        (10, 5, -10),
        (12, 0, -5),
    ]
    print("IK self-test:")
    for pt in test_points:
        result = invkin(*pt)
        if result:
            print(f"  invkin{pt} → coxa={result[0]:+.1f}°  femur={result[1]:+.1f}°  tibia={result[2]:+.1f}°")
        else:
            print(f"  invkin{pt} → UNREACHABLE")