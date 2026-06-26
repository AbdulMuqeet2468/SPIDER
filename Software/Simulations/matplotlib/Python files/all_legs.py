#   "That's one small step for robot, a giant leap for me"

#=========== ALL THE LIBRARIES ================
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import time

#=========== HARDWARE DESIGN ================
coxa = 7        # base link length
femur = 9       # middle link length
tibia = 11      # end link length

#=========== GLOBAL VARIABLES ================
#   Change these values to alter walking pattern
step_length = 10
step_height = 5
radius = 5
x_center=12
y_center = 5
step = 39 

side = 15 #body side
big_side = 100 #Side of ground
tile_size = 5 #checkered pattern tile size
ground_level = -10 #Change value to move ground
feature = 1 #invert to 0 if you dont want to see circle and other effects on the ground
trail_leg1 = []
trail_leg2 = []
trail_leg3 = []
trail_leg4 = []
trail_memory = [trail_leg1, trail_leg2, trail_leg3, trail_leg4]



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
stop_flag = {"stop": False}


'''
  2  _ _ _ _ _ _ _  1
    |             |  
    |    Body     |             ^ Front Direction
    |             |             
    |_ _ _ _ _ _ _|
   3                4

   origin at center of body
'''
leg1 = [side/2 , side/2 , 0]
leg2 = [-side/2 , side/2 , 0]
leg3 = [-side/2 , -side/2 , 0]
leg4 = [side/2 , -side/2 , 0]


#=========== INVERSE KINEMATICS FUNCTION ================
def invkin(x, y, z):
    """
    Calculates joint angles (coxa, femur, tibia) to reach the point (x, y, z)
    """
    # Coxa angle (rotation at base)
    theta_c_rad = math.atan2(y, x)
    theta_c = math.degrees(theta_c_rad)

    # Project into side-view plane
    x1 = x - (coxa * math.cos(theta_c_rad))
    y1 = y - (coxa * math.sin(theta_c_rad))
    x_new = math.sqrt(x1**2 + y1**2)

    # Distance from femur base to target
    L = math.sqrt(x_new**2 + z**2)
    alpha = math.degrees(math.atan2(z, x_new))

    # Femur angle using cosine law
    term1 = (femur**2 + L**2 - tibia**2) / (2 * femur * L)
    if -1 <= term1 <= 1:
        theta_f = math.degrees(math.acos(term1)) + alpha
    else:
        print("term1 out of range")
        return

    # Tibia angle using cosine law
    term2 = (femur**2 + tibia**2 - L**2) / (2 * femur * tibia)
    if -1 <= term2 <= 1:
        theta_ti = math.degrees(math.acos(term2))
    else:
        print("term2 out of range")
        return

    return theta_c, theta_f, theta_ti

#=========== CREATES GROUND PATTERN ================
def create_ground_pattern(ax, ground_level=ground_level, big_side=big_side, tile_size=tile_size):
    '''
    Computes the values for all tiles, then stores in ground_tiles. This variable will be used further to plot
    '''
    ground_tiles = []  # store all tile objects

    for i in range(-int(big_side/2), int(big_side/2), tile_size):
        for j in range(-int(big_side/2), int(big_side/2), tile_size):
            color = 'black' if (i//tile_size + j//tile_size) % 2 == 0 else 'white'
            verts = [[
                [i, j, ground_level],
                [i+tile_size, j, ground_level],
                [i+tile_size, j+tile_size, ground_level],
                [i, j+tile_size, ground_level]
            ]]
            tile = Poly3DCollection(verts, facecolors=color, edgecolor='none', alpha=0.15)
            ground_tiles.append(tile)

    return ground_tiles

#=========== INITIALIZE PLOT ================
def start_plot():
    '''
    Initialize plotting sequence and creates ground and body
    '''
    
    #=======    These lines will stop the program if user presses 'q'   ========
    
    ax.cla()

    def on_key(event):
        if event.key == 'q':
            stop_flag["stop"] = True
            plt.close(fig)

    fig.canvas.mpl_connect('key_press_event', on_key)
    #===============================================================================

    #   Uncomment to create a checkered pattern ground
    #   This is causing a lag in animation, need good cpu to run smoothly
    #ground_tiles = create_ground_pattern(ax)
    #for tile in ground_tiles:
    #    ax.add_collection3d(tile)
    #===============================================================================

    #   Body plot in a form of square
    ax.plot([side/2,-side/2],[side/2,side/2],[0,0],color='brown', linewidth=3, marker='o', label='side1')
    ax.plot([-side/2,-side/2],[side/2,-side/2],[0,0],color='brown', linewidth=3, marker='o', label='side2')
    ax.plot([-side/2,side/2],[-side/2,-side/2],[0,0],color='brown', linewidth=3, marker='o', label='side3')
    ax.plot([side/2,side/2],[-side/2,side/2],[0,0],color='brown', linewidth=3, marker='o', label='side4')

#=========== CONCLUDE PLOT ================
def end_plot():
    '''
    Has the code to be placed at the end of plotting sequence
    '''

    # Axes limits & labels
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.set_zlim(-25, 25)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3-DOF Leg Inverse Kinematics Animation with Trail")
    #   Uncomment below two lines to remove grid and axis from the window
    #ax.grid(False)
    #ax._axis3don = False
    
    #   Uncomment and set appropriate values to fix 2D camera view
    #ax.set_proj_type('ortho')       
    #ax.view_init(elev=0, azim=0)   

    plt.draw()
    plt.pause(0.005) #   Frame time in seconds

#=========== Bottom two functions are just to enhance visualisation ================
# Created a cirle in XY plane just to visualise the ground
def draw_circle_xy(ax, x_center = x_center, y_center=0, radius=step_length/2, num_points=100):
    """
    Draws a circle in the XY plane. 
    Coordinates can be updated later.
    """
    angles = np.linspace(0, 2*np.pi, num_points)
    xs = x_center + radius * np.cos(angles)
    ys = y_center + radius * np.sin(angles)
    zs =  ground_level #np.zeros_like(xs)  # XY plane → Z=0
    ax.plot(xs, ys, zs, color='magenta', linestyle='--', linewidth=1)

#Again used for visualising straight line
def draw_diameter_line(ax, x_center = x_center, z = ground_level, step_length = step_length, gamma_deg = 0, y_center = 0):
    """
    Draws a solid line along a diameter passing through a point on the circle.
    Circle is in XY plane at height z.
    
    ax        : matplotlib 3D axis
    x_center  : x-coordinate of circle center
    z         : z-coordinate of circle center
    step_length : length of step (circle radius = step_length/2)
    gamma     : angle in radians to locate first point on circle
    """
    r = step_length / 2
    
    gamma = math.radians(gamma_deg)
    # First point on circle
    x1 = x_center + r * math.sin(gamma)
    y1 = r * math.cos(gamma) + y_center
    
    # Diametrically opposite point
    x2 = x_center - r * math.sin(gamma)
    y2 = -r * math.cos(gamma) + y_center
    
    # Line joining points
    ax.plot([x1, x2], [y1, y2], [z, z], color='black', linewidth=2, alpha=0.5, linestyle=':')

#This function gets two end points which we will use as our leg's limit of movement
# Based on the value of gamma, the end points will change  
def get_points(gamma_deg, step_length = step_length, x_center = x_center):
    """
    Computes two points on a circular step in XY plane:
    - Point at given gamma angle
    - Opposite point on the diameter
    
    Parameters:
    - step_length : length of step (radius = step_length / 2)
    - step_height : z-coordinate of leg end (height)
    - gamma_deg   : angle on circle in degrees
    - x_center    : x-coordinate of circle center (default 0)
    
    Returns:
    - (x1, y1, z1), (x2, y2, z2) : coordinates of point and opposite point
    """
    r = step_length / 2
    gamma_rad = math.radians(gamma_deg)
    
    # First point on circle
    x1 = x_center + r * math.sin(gamma_rad)
    y1 =  r * math.cos(gamma_rad)
    z1 = ground_level
    
    # Opposite point on the diameter
    x2 = x_center - r * math.sin(gamma_rad)
    y2 = - r * math.cos(gamma_rad)
    z2 = ground_level
    
    return (x1, y1, z1), (x2, y2, z2), gamma_rad

#   This function gives a 'fading effect' of leg motion
#   Used just for enhancing visualisation
def fade_effect(x, y, z, leg_number, trail_length=30):
    
    trail = trail_memory[leg_number-1]
    trail.append([x, y, z])
    if len(trail) > trail_length:
        trail.pop(0)
    xs, ys, zs = zip(*trail)
    ax.plot(xs, ys, zs, color='black', linestyle=':', linewidth=1, alpha=0.6)


def leg_goToPoint(leg_number_base, x, y, z, feature = feature, x_center = x_center):
    
    if leg_number_base == leg1:
        leg_number = 1
    elif leg_number_base == leg2:
        leg_number = 2
    elif leg_number_base == leg3:
        leg_number = 3
    elif leg_number_base == leg4:
        leg_number = 4

    base = leg_number_base
    theta_c, theta_f, theta_ti = invkin(x,y,z)
    theta_c_rad = math.radians(theta_c)
    # Coxa end
    coxa_end = [base[0] + coxa * math.cos(theta_c_rad),base[1]+ coxa * math.sin(theta_c_rad),base[2] + 0]

    # Femur end
    theta_f_rad = math.radians(theta_f)
    femur_end_x = coxa_end[0] + femur * math.cos(theta_f_rad) * math.cos(theta_c_rad)
    femur_end_y = coxa_end[1] + femur * math.cos(theta_f_rad) * math.sin(theta_c_rad)
    femur_end_z = coxa_end[2] + femur * math.sin(theta_f_rad)

    # Tibia end
    theta_fk_deg = theta_f + theta_ti - 180
    theta_fk = math.radians(theta_fk_deg)
    tibia_end_x = femur_end_x + tibia * math.cos(theta_fk) * math.cos(theta_c_rad)
    tibia_end_y = femur_end_y + tibia * math.cos(theta_fk) * math.sin(theta_c_rad)
    tibia_end_z = femur_end_z + tibia * math.sin(theta_fk)

    # Draw segments
    ax.plot([base[0], coxa_end[0]], [base[1], coxa_end[1]], [base[2], coxa_end[2]],
            color='red', linewidth=3, marker='o', label='Coxa')
    ax.plot([coxa_end[0], femur_end_x], [coxa_end[1], femur_end_y], [coxa_end[2], femur_end_z],
            color='green', linewidth=3, marker='o', label='Femur')
    ax.plot([femur_end_x, tibia_end_x], [femur_end_y, tibia_end_y], [femur_end_z, tibia_end_z],
            color='blue', linewidth=3, marker='x', label='Tibia')
    
    if feature:
        draw_circle_xy(ax, x_center= x_center+base[0], y_center=base[1])
        draw_diameter_line(ax, x_center= x_center + base[0], y_center=base[1])
        fade_effect(x+base[0], y+base[1], z+base[2], leg_number)

def phase_shifter(start, step):
    pass
    



def move():
    
    
    (x1a,y1a,z1a),(x2a,y2a,z2a), gamma_rad1 = get_points(gamma_deg=0, x_center=12)
    (x1b,y1b,z1b),(x2b,y2b,z2b), gamma_rad2 = get_points(gamma_deg=30, x_center=-12)
    (x1c,y1c,z1c),(x2c,y2c,z2c), gamma_rad3 = get_points(gamma_deg=90, x_center=-12)
    (x1d,y1d,z1d),(x2d,y2d,z2d), gamma_rad4 = get_points(gamma_deg=180, x_center=12)

   

    while not stop_flag['stop']:
        xa,ya,za = x1a,y1a,z1a
        xb,yb,zb = x1b,y1b,z1b
        xc,yc,zc = x1c,y1c,z1c
        xd,yd,zd = x1d,y1d,z1d

        for n in range(step+1):
            start_plot()
            leg_goToPoint(leg1,xa,ya,za, x_center=12)
            leg_goToPoint(leg2,xb,yb,zb, x_center=-12)
            leg_goToPoint(leg3,xc,yc,zc, x_center=-12)
            leg_goToPoint(leg4,xd,yd,zd, x_center=12)
            end_plot()
            xa = x1a - n * step_length/step * np.sin(gamma_rad1)
            ya = y1a - n * step_length/step * np.cos(gamma_rad1)
            za = ground_level
            
            xb = x1b - n * step_length/step * np.sin(gamma_rad2)
            yb = y1b - n * step_length/step * np.cos(gamma_rad2)
            zb = ground_level

            xc = x1c - n * step_length/step * np.sin(gamma_rad3)
            yc = y1c - n * step_length/step * np.cos(gamma_rad3)
            zc = ground_level
            
            xd = x1d - n * step_length/step * np.sin(gamma_rad4)
            yd = y1d - n * step_length/step * np.cos(gamma_rad4)
            zd = ground_level

        
        for n in range(step+1):
            start_plot()
            leg_goToPoint(leg1,xa,ya,za, x_center=12)
            leg_goToPoint(leg2,xb,yb,zb, x_center=-12)
            leg_goToPoint(leg3,xc,yc,zc, x_center=-12)
            leg_goToPoint(leg4,xd,yd,zd, x_center=12)
            end_plot()
            xa = x2a + n * step_length/step * np.sin(gamma_rad1)
            ya = y2a + n * step_length/step * np.cos(gamma_rad1)
            za = step_height * np.cos(ya/(step_length * np.cos(gamma_rad1)) * np.pi) + ground_level
            
            xb = x2b + n * step_length/step * np.sin(gamma_rad2)
            yb = y2b + n * step_length/step * np.cos(gamma_rad2)
            zb = step_height * np.cos(yb/(step_length * np.cos(gamma_rad2)) * np.pi) + ground_level

            xc = x2c + n * step_length/step * np.sin(gamma_rad3)
            yc = y2c + n * step_length/step * np.cos(gamma_rad3)
            zc = step_height * np.cos(yc/(step_length * np.cos(gamma_rad3)) * np.pi) + ground_level
            
            xd = x2d + n * step_length/step * np.sin(gamma_rad4)
            yd = y2d + n * step_length/step * np.cos(gamma_rad4)
            zd = step_height * np.cos(yd/(step_length * np.cos(gamma_rad4)) * np.pi) + ground_level

    
a = b = c = d = 0
a_offset = 0
b_offset = 0
c_offset = 0
d_offset = 0

def check_offset(offset_variable, start_value,n):
    if not offset_variable:
        n += start_value #for creating offset
        offset_variable = 1

    return offset_variable, n


def cosine_trajectory(start_value, leg_number, x_center, theta_rotation):
    
    global a, b, c, d, a_offset, b_offset, c_offset, d_offset

    if leg_number == leg1:
        n = a
        a_offset, n = check_offset(a_offset, start_value,n)
    elif leg_number == leg2:
        n = b
        b_offset, n = check_offset(b_offset, start_value,n)
    elif leg_number == leg3:
        n = c
        c_offset, n = check_offset(c_offset, start_value,n)
    elif leg_number == leg4:
        n = d
        d_offset, n = check_offset(d_offset, start_value,n)
    
    

    (x1,y1,z1),(x2,y2,z2), gamma_rad = get_points(gamma_deg=theta_rotation, x_center = x_center)

    if 0 <= n <= (step+1):
        x = x1 - n * step_length/step * np.sin(gamma_rad)
        y = y1 - n * step_length/step * np.cos(gamma_rad)
        z = ground_level
        #start_plot()
        leg_goToPoint(leg_number ,x,y,z, x_center=x_center)
        #end_plot()
        #print("n1 = ", n)
        n+=1

    #here is the issue
    elif step+1 < n < (2*step):
        n_new = n - (step+1)
        for i in range(step//3):
            n_new += 1
            x = x2 + n_new * step_length/step * np.sin(gamma_rad)
            y = y2 + n_new * step_length/step * np.cos(gamma_rad)
            z = step_height * np.cos(y/(step_length * np.cos(gamma_rad)) * np.pi) + ground_level
            #start_plot()
            leg_goToPoint(leg_number ,x,y,z, x_center=x_center)
            #end_plot()
            #print("n2 = ", n)
            n+=1
            
            

    
    if n >= 2*step:
        n = 0
    

    if leg_number == leg1:
        a = n
    elif leg_number == leg2:
        b = n
    elif leg_number == leg3:
        c = n
    elif leg_number == leg4:
        d = n


def ripple_gait():
    while not stop_flag['stop']:
        start_plot()
        cosine_trajectory(start_value=0, leg_number=leg1, x_center=12, theta_rotation=0)
        cosine_trajectory(start_value=26, leg_number=leg2, x_center=-12, theta_rotation=0)
        cosine_trajectory(start_value=13, leg_number=leg3, x_center=-12, theta_rotation=0)
        cosine_trajectory(start_value=39, leg_number=leg4, x_center=12, theta_rotation=0)
        end_plot()

def turn_right():
    while not stop_flag['stop']:
        start_plot()
        cosine_trajectory(start_value=0, leg_number=leg1, x_center=12, theta_rotation=135)
        cosine_trajectory(start_value=26, leg_number=leg2, x_center=-12, theta_rotation=45)
        cosine_trajectory(start_value=13, leg_number=leg3, x_center=-12, theta_rotation=315)
        cosine_trajectory(start_value=39, leg_number=leg4, x_center=12, theta_rotation=225)
        end_plot()

def trot_gait():
    while not stop_flag['stop']:
        start_plot()
        cosine_trajectory(start_value=13, leg_number=leg1, x_center=12)
        cosine_trajectory(start_value=0, leg_number=leg2, x_center=-12)
        cosine_trajectory(start_value=26, leg_number=leg3, x_center=-12)
        cosine_trajectory(start_value=39, leg_number=leg4, x_center=12)
        end_plot()


ripple_gait()
#trot_gait()
#turn_right()