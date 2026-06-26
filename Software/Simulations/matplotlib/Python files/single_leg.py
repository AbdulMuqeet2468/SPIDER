#works fine
#included fade trail feature
#side view gait analysis
#Everything is perfect, all what I wanted
#gamma can take any value 


import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

# --- Hardware / design constants ---
coxa = 7        # base link length
femur = 9       # middle link length
tibia = 11      # end link length

step_length = 10
step_height = 5
radius = 5
x_center=12


# --- Inverse Kinematics Function ---
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

# Created a cirle in XY plane just to visualise the ground
def draw_circle_xy(ax, x_center = x_center, y_center=0, radius=radius, num_points=100):
    """
    Draws a circle in the XY plane. 
    Coordinates can be updated later.
    """
    angles = np.linspace(0, 2*np.pi, num_points)
    xs = x_center + radius * np.cos(angles)
    ys = y_center + radius * np.sin(angles)
    zs =  -step_height #np.zeros_like(xs)  # XY plane → Z=0
    ax.plot(xs, ys, zs, color='magenta', linestyle='--', linewidth=1)

#Again used for visualising straight line
def draw_diameter_line(ax, x_center = x_center, z = -step_height, step_length = step_length, gamma_deg = 0):
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
    y1 = r * math.cos(gamma)
    
    # Diametrically opposite point
    x2 = x_center - r * math.sin(gamma)
    y2 = -r * math.cos(gamma)
    
    # Line joining points
    ax.plot([x1, x2], [y1, y2], [z, z], color='black', linewidth=2)

#gives end points on the circle depending on gamma
def circular_step_points(step_length = step_length, step_height = step_height, gamma_deg = 0, x_center = x_center):
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
    y1 = r * math.cos(gamma_rad)
    z1 = -step_height
    
    # Opposite point on the diameter
    x2 = x_center - r * math.sin(gamma_rad)
    y2 = -r * math.cos(gamma_rad)
    z2 = -step_height
    
    return (x1, y1, z1), (x2, y2, z2), gamma_rad, gamma_deg

# --- Forward Kinematics & Plotting Function with Trail ---
trail_points = []   # global list for storing tibia end path

#All plotting logic is done here
#Check for some comments to enable extra features
def plot_3d(theta_c, theta_f, theta_ti, x, y, z, ax, trail_length=30):
    """
    Draws the leg in 3D for given joint angles, with a fading trail of end-effector.
    """
    theta_c_rad = math.radians(theta_c)

    # Base coordinates
    base = [0, 0, 0]

    # Coxa end
    coxa_end = [coxa * math.cos(theta_c_rad), coxa * math.sin(theta_c_rad), 0]

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

    # --- Add tibia end to trail ---
    trail_points.append([tibia_end_x, tibia_end_y, tibia_end_z])
    if len(trail_points) > trail_length:
        trail_points.pop(0)

    # Clear previous plot
    ax.cla()

    # Draw segments
    ax.plot([base[0], coxa_end[0]], [base[1], coxa_end[1]], [base[2], coxa_end[2]],
            color='red', linewidth=3, marker='o', label='Coxa')
    ax.plot([coxa_end[0], femur_end_x], [coxa_end[1], femur_end_y], [coxa_end[2], femur_end_z],
            color='green', linewidth=3, marker='o', label='Femur')
    ax.plot([femur_end_x, tibia_end_x], [femur_end_y, tibia_end_y], [femur_end_z, tibia_end_z],
            color='blue', linewidth=3, marker='x', label='Tibia')

    # --- Draw trail (fading effect) ---
    xs, ys, zs = zip(*trail_points)
    ax.plot(xs, ys, zs, color='black', linestyle=':', linewidth=1)

    # Axes limits & labels
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.set_zlim(-25, 25)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3-DOF Leg Inverse Kinematics Animation with Trail")

    #circle on xy plane
    draw_circle_xy(ax)

    #arguements => (ax, circle_center_x, circle_z, step_length, gamma_deg)
    draw_diameter_line(ax)

    # --- Fix camera view (YZ plane) ---
    #ax.set_proj_type('ortho')       # orthographic projection
    #ax.view_init(elev=0, azim=0)   # looking YZ plane only, i.e general side view in our case
    plt.draw()
    plt.pause(0.05)

# --- Function to move leg to a single point ---
#created this function to mimic servo function in cpp
def goToPoint(x, y, z, ax):
    """
    Moves the leg to a single (x,y,z) point.
    """
    angles = invkin(x, y, z)
    if angles:  # Only plot if reachable
        plot_3d(*angles, x, y, z, ax)

# --- Function to define a trajectory ---
#cosine path is followed by the end point
def trajectory_leg1():
    """
    Moves the leg along a predefined trajectory by calling goToPoint().
    Repeats until 'q' is pressed in the plot window.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    stop_flag = {"stop": False}

    # define key event handler
    def on_key(event):
        if event.key == 'q':
            stop_flag["stop"] = True
            plt.close(fig)

    # connect handler to figure
    fig.canvas.mpl_connect('key_press_event', on_key)

      
    
    (x1,y1,z1),(x2,y2,z2), gamma_rad, gamma_deg = circular_step_points(step_length=step_length, step_height=step_height, gamma_deg=180)

    if -90 <= gamma_deg <= 90:

        while not stop_flag["stop"]:

            #Actual trajectory is defined here
            #works only for gamma_deg -90 to +90
            
            
            

            
            n = 0
            y = y2
            x = x2
            z = z2

            while y <= y1:
                
                goToPoint(x, y, z, ax)
                # parametric form of line along gamma
                x = x2 + n * 0.5 * np.sin(gamma_rad)
                y = y2 + n * 0.5 * np.cos(gamma_rad)

                # z with cosine stepping
                z = step_height * np.cos(y/(step_length * np.cos(gamma_rad)) * np.pi) - step_height
                print(n)
                n += 1

            y = y1
            x = x1
            z = z1
            n = 0

            while y >= y2:
                
                goToPoint(x, y, z, ax)
                x = x1 - n * 0.5 * np.sin(gamma_rad)
                y = y1 - n * 0.5 * np.cos(gamma_rad)

                z = - step_height# * np.cos(gamma_rad)
                
                n += 1

    else: 

        while not stop_flag["stop"]:

            
            
            
            

            
            n = 0
            y = y2
            x = x2
            z = z2

            while y >= y1:
                
                goToPoint(x, y, z, ax)
                # parametric form of line along gamma
                x = x2 + n * 0.5 * np.sin(gamma_rad)
                y = y2 + n * 0.5 * np.cos(gamma_rad)

                # z with cosine stepping
                z = step_height * np.cos(y/(step_length * np.cos(gamma_rad)) * np.pi) - step_height

                n += 1

            y = y1
            x = x1
            z = z1
            n = 0

            while y <= y2:
                
                goToPoint(x, y, z, ax)
                x = x1 - n * 0.5 * np.sin(gamma_rad)
                y = y1 - n * 0.5 * np.cos(gamma_rad)

                z = - step_height# * np.cos(gamma_rad)
                
                n += 1




print("Trajectory stopped by user.")

        


    
# --- Run Animation ---

trajectory_leg1()

