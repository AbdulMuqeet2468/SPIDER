import math
coxa = 7
femur = 9
tibia = 11

def invkin(x,y,z):

    #define coxa angle
    theta_c = math.atan(y/x) #in radians
    

    #going to side view plane origin
    x1 = x - (coxa * math.cos(theta_c))
    y1 = y - (coxa * math.sin(theta_c))

    theta_c = math.degrees(theta_c) #in degrees
    

    #equivalent x coordinate
    x_new = math.sqrt(x1**2 + y1**2)

    print("(x,y) = (",x,y,")")
    print("(x1,y1) = (",x1,y1,")")
    print(f"theta_c ={theta_c:.2f}")

    #w.r.t side view plane
    L = math.sqrt(x_new**2 + z**2)
    alpha = math.degrees(math.atan(z/x_new)) # in degrees
    print(f"alpha ={alpha:.2f}")

    #femur angle
    term1 = (femur**2 + L**2 - tibia**2)/(2 * femur * L)
    if (-1<= term1 <=1):
        theta_f = math.degrees(math.acos(term1)) + alpha # in degrees
        print(f"theta_f ={theta_f:.2f}")
    else:
        print("term1 value error")

    #tibia angle
    term2 = (femur**2 + tibia**2 - L**2)/(2 * femur * tibia)
    if (-1<= term2 <=1):
        theta_ti = math.degrees(math.acos(term2))
        print(f"theta_ti ={theta_ti:.2f}")
    else:
        print("term2 value error")
    print("=========================================")


    


go = 1
while(go):
    x, y, z = map(float, input("Enter x, y, z: ").split(','))
    invkin(x,y,z)
    go = int(input("Do you want to continue?\n 1 for yes and 0 for no"))



    