# ============================================================
#   gait.py  —  Gait scheduler.
#
#   This layer decides:
#     - which gait pattern to run
#     - what phase each leg starts at
#     - what direction to walk
#     - how fast to move
#
#   It calls leg.step() for every leg every frame.
#   All legs update every single timestep — no leg ever blocks another.
# ============================================================

from config import GAIT_PHASES, LEG_ORDER, PHASE_INCREMENT


class GaitController:

    def __init__(self, legs):
        """
        legs : dict  {'R1': Leg, 'R2': Leg, 'L1': Leg, 'L2': Leg}
        """
        self.legs      = legs
        self.gait      = 'ripple'   # current gait
        self.direction = 0.0        # degrees: 0=forward, 90=strafe right, 180=back
        self.speed     = 1.0        # multiplier: 0.5=slow, 1.0=normal, 2.0=fast
        self._initialized = False

    def set_gait(self, gait_name):
        """
        Switch to a different gait. Options: 'ripple', 'trot', 'walk'
        Phase offsets reset to the new gait's values.
        """
        if gait_name not in GAIT_PHASES:
            raise ValueError(f"Unknown gait '{gait_name}'. Options: {list(GAIT_PHASES.keys())}")
        self.gait = gait_name
        self._initialized = False   # force re-init of phase offsets

    def set_direction(self, degrees):
        """
        Set walking direction.
        0   = forward
        90  = strafe right
        180 = backward
        270 = strafe left
        Any angle in between = diagonal
        """
        self.direction = degrees % 360

    def set_speed(self, speed):
        """
        Set movement speed multiplier.
        0.5 = slow,  1.0 = normal,  2.0 = fast
        """
        self.speed = max(0.1, speed)

    def _init_phases(self):
        """Apply phase offsets for the current gait to all legs."""
        offsets = GAIT_PHASES[self.gait]
        for leg_name, offset in zip(LEG_ORDER, offsets):
            self.legs[leg_name].set_phase(offset)
        self._initialized = True

    def update(self, phase_increment=None):
        """
        Call this every frame from the main loop.
        Advances all legs by one timestep.
 
        phase_increment : how much phase advances per frame.
                          Defaults to PHASE_INCREMENT from config.py,
                          which is derived from STEP (1/STEP).
                          A full gait cycle then takes exactly STEP frames
                          at speed=1.0 — same idea as your original
                          "for n in range(step+1)" loop, just continuous now.
                          Scaled by self.speed.
        """
        if phase_increment is None:
            phase_increment = PHASE_INCREMENT
 
        if not self._initialized:
            self._init_phases()
 
        increment = phase_increment * self.speed
 
        for leg_name in LEG_ORDER:
            self.legs[leg_name].step(
                phase_increment=increment,
                theta_rotation=self.direction,
            )