# ============================================================
#   leg.py —  One leg of the spider
#   Each Leg object owns:
#     - its base position on the body
#     - its current phase in the gait cycle
#     - its trail (for visualisation)
#     - a goto_point() method  ← the one function you command
#
#   To move to real hardware : only change goto_point().
# ============================================================

from kinematics import invkin, forward_positions
from trajectory import get_foot_position
from config    import LEG_BASES, LEG_REACH, TRAIL_LENGTH


class Leg:

    def __init__(self, name):
        """
        name : 'R1', 'R2', 'L1', 'L2'
        """
        self.name  = name
        self.base  = LEG_BASES[name]      # [x, y, z] on body
        self.reach = LEG_REACH[name]      # x_center for this leg
        self.phase = 0.0                  # position in gait cycle (0.0 → 1.0)

        # Last computed joint angles (degrees) — for display
        self.theta_c  = 0.0
        self.theta_f  = 0.0
        self.theta_ti = 0.0

        # Last foot world position — for trail
        self.foot_world = [self.base[0] + self.reach,
                           self.base[1],
                           self.base[2]]
        self.trail = []

    # ── The main command function ─────────────────────────────
    def goto_point(self, x, y, z):
        """
        Command this leg's foot to (x, y, z) in leg-local frame.

        This is the function you call to move one leg.
        It runs IK and sends angles to the output layer.

        For matplotlib: output is stored in self.theta_* for the visualiser.
        For CoppeliaSim: replace the bottom of this function with sim calls.
        For real hardware: replace with servo commands.
        """
        result = invkin(x, y, z)
        if result is None:
            return   # skip unreachable targets silently

        self.theta_c, self.theta_f, self.theta_ti = result

        # ── OUTPUT LAYER ──────────────────────────────────────
        # matplotlib: nothing to do here, visualiser reads self.theta_*
        # CoppeliaSim: uncomment and fill handles
        # sim.setJointTargetPosition(self.handles['coxa'],  math.radians(self.theta_c))
        # sim.setJointTargetPosition(self.handles['femur'], math.radians(self.theta_f))
        # sim.setJointTargetPosition(self.handles['tibia'], math.radians(self.theta_ti))

        # Update foot world position for trail
        _, _, foot = forward_positions(
            self.base, self.theta_c, self.theta_f, self.theta_ti
        )
        self.foot_world = foot
        self.trail.append(foot[:])
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

    # ── Advance one timestep in the gait cycle ────────────────
    def step(self, phase_increment, theta_rotation, x_center=None):
        """
        Advance this leg's phase by phase_increment,
        then call goto_point() with the trajectory position.

        phase_increment : how much to advance per frame
                          (controls speed — larger = faster)
        theta_rotation  : direction of travel in degrees
        x_center        : override reach center (optional)
        """
        if x_center is None:
            x_center = self.reach

        self.phase = (self.phase + phase_increment) % 1.0
        x, y, z   = get_foot_position(self.phase, theta_rotation, x_center)
        self.goto_point(x, y, z)

    def set_phase(self, phase):
        """Directly set the phase offset (call once at startup for gait coordination)."""
        self.phase = phase % 1.0

    def print_angles(self):
        print(f"  {self.name} | coxa: {self.theta_c:+7.2f}°  "
              f"femur: {self.theta_f:+7.2f}°  tibia: {self.theta_ti:+7.2f}°")