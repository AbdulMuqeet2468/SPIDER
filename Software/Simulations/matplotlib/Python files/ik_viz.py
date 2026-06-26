'''
*Visualising Inv Kin function in static mode*
With the logic ready, now its time to test it by visualising. For that I will be using matplotlib module. 
Furthermore I am changing colours of different segments of legs for easier differentiation. 
Author: M Abdul Muqeet
'''

import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Change values according to the hardware/design
coxa = 7
femur = 9
tibia = 11

def invkin(x, y, z):
    '''
    Takes in 3 coordinate values and uses trignometric method of solving Inverse Kinematics function to return required angles.
    '''
    #Getting Coxa angle
    theta_c_rad = math.atan2(y, x) #radians
    theta_c = math.degrees(theta_c_rad) #degrees

    #going to side view plane origin
    x1 = x - (coxa * math.cos(theta_c_rad))
    y1 = y - (coxa * math.sin(theta_c_rad))

    #equivalent x coordinate
    x_new = math.sqrt(x1**2 + y1**2)

    #w.r.t side view plane
    L = math.sqrt(x_new**2 + z**2)
    alpha = math.degrees(math.atan2(z, x_new))

    #Getting Femur angle
    term1 = (femur**2 + L**2 - tibia**2)/(2 * femur * L)
    if -1 <= term1 <= 1:
        theta_f = math.degrees(math.acos(term1)) + alpha
    else:
        print("term1 out of range") #use for debugging
        return

    #Getting Tibia angle
    term2 = (femur**2 + tibia**2 - L**2)/(2 * femur * tibia)
    if -1 <= term2 <= 1:
        theta_ti = math.degrees(math.acos(term2))
    else:
        print("term2 out of range") #use for debugging
        return

    #uncomment for debugging
    #print(f"theta_c = {theta_c:.2f}")
    #print(f"theta_f = {theta_f:.2f}")
    #print(f"theta_ti = {theta_ti:.2f}")
    #print("===================================")
    return theta_c, theta_f, theta_ti

def plot_3d(theta_c, theta_f, theta_ti):
    '''
    Takes in 3 angle arguements and returns 3d plot
    '''

    theta_c_rad = math.radians(theta_c) #in radians

    #base at origin
    base = [0, 0, 0]

    #defining coxa end
    coxa_end = [coxa * math.cos(theta_c_rad), coxa * math.sin(theta_c_rad), 0]

    #defining femur end
    theta_f_rad = math.radians(theta_f) #in radians 
    femur_end_x = coxa_end[0] + femur * math.cos(theta_f_rad) * math.cos(theta_c_rad)
    femur_end_y = coxa_end[1] + femur * math.cos(theta_f_rad) * math.sin(theta_c_rad)
    femur_end_z = coxa_end[2] + femur * math.sin(theta_f_rad)

    #defining tibia end
    theta_fk_deg = theta_f + theta_ti - 180 #relative angle for tibia point
    theta_fk = math.radians(theta_fk_deg) #in radians
    tibia_end_x = femur_end_x + tibia * math.cos(theta_fk) * math.cos(theta_c_rad)
    tibia_end_y = femur_end_y + tibia * math.cos(theta_fk) * math.sin(theta_c_rad)
    tibia_end_z = femur_end_z + tibia * math.sin(theta_fk)

    #end point is final end effector point
    end_point = [tibia_end_x, tibia_end_y, tibia_end_z]
    print("End Effector:", end_point)

    #Have to work on this
    #it says 'unreachable' even if there is a difference of 10e-4 (i.e very small difference)
    if end_point != [x,y,z]:
        print('Point not reachable')
        #return 
         

    #plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #using different colours for each segment

    # Segment 1: base to coxa
    ax.plot([base[0], coxa_end[0]],
            [base[1], coxa_end[1]],
            [base[2], coxa_end[2]],
            color='red', linewidth=3, marker='o', label='Coxa')

    # Segment 2: coxa to femur
    ax.plot([coxa_end[0], femur_end_x],
            [coxa_end[1], femur_end_y],
            [coxa_end[2], femur_end_z],
            color='green', linewidth=3, marker='o', label='Femur')

    # Segment 3: femur to tibia
    ax.plot([femur_end_x, tibia_end_x],
            [femur_end_y, tibia_end_y],
            [femur_end_z, tibia_end_z],
            color='blue', linewidth=3, marker='x', label='Tibia')

    #modify these parameters if you want
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.set_zlim(-25, 25)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3-DOF Leg Inverse Kinematics")

    plt.show()


def vis(x,y,z):
    ''' Small function used for calling plotting function'''
    angles = invkin(x, y, z)
    plot_3d(*angles)    

#Takes inputs 
x, y, z = map(float, input("Enter x, y, z: ").split(','))
vis(x,y,z)

