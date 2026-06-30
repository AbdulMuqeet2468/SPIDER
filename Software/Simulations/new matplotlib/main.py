# ============================================================
#   main.py  —  Entry point. Wires all modules together.
#
#   This is the ONLY file you run:  python3 main.py
#
#   To change behaviour:
#     - Walking speed / step size  →  config.py
#     - Gait pattern               →  config.py  (GAIT_PHASES)
#     - Foot trajectory shape      →  trajectory.py
#     - IK math                    →  kinematics.py
#     - Move to CoppeliaSim        →  leg.py  (goto_point)
# ============================================================

from leg        import Leg
from gait       import GaitController
from visualiser import Visualiser
from config     import LEG_ORDER

# ── 1. Create all legs ───────────────────────────────────────
legs = {name: Leg(name) for name in LEG_ORDER}

# ── 2. Create gait controller ────────────────────────────────
gait = GaitController(legs)

# ── 3. Configure — change these lines to try different things ─
gait.set_gait('ripple')       # 'ripple', 'trot', 'walk'
gait.set_direction(0)         # 0=forward, 90=strafe right, 180=back, 270=strafe left
gait.set_speed(2.0)           # 0.5=slow, 1.0=normal, 2.0=fast

# ── 4. Create visualiser ─────────────────────────────────────
vis = Visualiser()

# ── 5. Main loop ─────────────────────────────────────────────
print("Running simulation. Press Q in the plot window to quit.")
print(f"  Gait: {gait.gait}  |  Direction: {gait.direction}°  |  Speed: {gait.speed}x\n")

while vis.is_running():
    # Update all legs — phase_increment defaults to 1/STEP from config.py
    # so a full gait cycle takes exactly STEP frames at speed=1.0
    gait.update()

    # Draw this frame
    vis.begin_frame()
    for name in LEG_ORDER:
        vis.draw_leg(legs[name])
    vis.end_frame()

    # Optional: print angles every frame (comment out if too noisy)
    # for name in LEG_ORDER:
    #     legs[name].print_angles()

print("Simulation ended.")


# ============================================================
#   QUICK REFERENCE — how to use each module from here
# ============================================================
#
#   ONE LEG COMMAND:
#       legs['R1'].goto_point(x=12, y=0, z=-10)
#
#   CHANGE GAIT MID-RUN:
#       gait.set_gait('trot')
#
#   CHANGE DIRECTION MID-RUN:
#       gait.set_direction(90)   # strafe right
#
#   CHANGE SPEED MID-RUN:
#       gait.set_speed(0.5)      # slow down
#
#   PRINT JOINT ANGLES:
#       legs['R1'].print_angles()
#
#   ACCESS CURRENT FOOT POSITION:
#       legs['R1'].foot_world     # [x, y, z] in world frame
#
#   ACCESS CURRENT PHASE:
#       legs['R1'].phase          # 0.0 → 1.0
# ============================================================