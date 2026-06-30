# ============================================================
#   config.py  —  All robot parameters
#   Change numbers here only
# ============================================================

# ── Link lengths (cm) ────────────────────────────────────────
#   Change according to hardware design
COXA  = 7
FEMUR = 9
TIBIA = 11

# ── Gait parameters ──────────────────────────────────────────
STEP_LENGTH  = 10      # how far the foot travels per step (cm)
STEP_HEIGHT  = 5       # how high the foot lifts during swing (cm)
GROUND_LEVEL = -10     # z height of foot when on ground (cm)

#   STEP = how many discrete increments make up ONE FULL gait cycle
#   Higher STEP  → finer motion, smoother but slower to complete a cycle
#   Lower  STEP  → coarser motion, faster but choppier
STEP = 100
 
#   Derived: how much phase (0.0 -> 1.0) advances per frame at normal speed
#   One full cycle (phase 0 -> 1) takes exactly STEP frames to complete
PHASE_INCREMENT = 1 / STEP

# ── Body geometry ────────────────────────────────────────────
SIDE = 15              # body square half-side (cm)

#   Leg base positions (where each leg attaches to the body)
#   Origin at body center
#
#      L1 ───────── R1
#       |           |       ^ Front
#       |           |
#      L2 ───────── R2
#
LEG_BASES = {
    'R1': [ SIDE/2,  SIDE/2, 0],
    'R2': [ SIDE/2, -SIDE/2, 0],
    'L1': [-SIDE/2,  SIDE/2, 0],
    'L2': [-SIDE/2, -SIDE/2, 0],
}

# ── Reach center for each leg (x_center in matplotlib code) ──
#   How far forward the leg reaches from its base
LEG_REACH = {
    'R1':  12,
    'R2':  12,
    'L1': -12,
    'L2': -12,
}

# ── Gait phase offsets (fraction of cycle 0.0 → 1.0) ────────
#   Each value = where in the cycle that leg starts
#   This is what creates ripple / trot / walk coordination
GAIT_PHASES = {
    #           R1    R2    L1    L2
    'ripple': [0.00, 0.50, 0.25, 0.75],
    'trot':   [0.00, 0.50, 0.50, 0.00],
    'walk':   [0.00, 0.25, 0.50, 0.75],
}

LEG_ORDER = ['R1', 'R2', 'L1', 'L2']

# ── Visualisation ────────────────────────────────────────────
TIMESTEP     = 0.005   # seconds per frame (matplotlib pause)
TRAIL_LENGTH = 30      # foot trail length
AXIS_LIMIT   = 30      # plot axis limit (cm)
SHOW_TRAIL   = True
SHOW_CIRCLE  = True