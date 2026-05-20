from simulation import simul
from solver import iterative_solve
from energyanalysis import energy

def main():
    true_ivelocity = ""
    true_iheight = 0.455
    true_iangle = 63.556
    true_gravity = "g"
    true_distance = 1.388
    true_maxheight = ""
    true_time = ""
    true_fvelocity = ""

    is_baseball = False
    is_football = False
    is_pingpongball = True
    is_soccerball = False
    is_tennisball = False
    is_paperairplane = False
    is_paperball = False
    allow_timestamps = False
    allow_energyanalysis = True
    load_trajectory = True
    true_mass = 0
    true_cd = 0
    true_area = 0
    true_density = 1.225
    depprofile = "none"



    def aeroprofile(mass,cd,area):
        true_mass = mass
        true_cd = cd
        true_area = area        

    if is_baseball:
        aeroprofile(0.145,0.35,0.0042)
    elif is_football:
        aeroprofile(0.415,0.06,0.0365)
    elif is_pingpongball:
        aeroprofile(0.0027,0.445,0.00126)
    elif is_soccerball:
        aeroprofile(0.415,0.25,0.0375)
    elif is_tennisball:
        aeroprofile(0.057,0.6,0.0035)
    elif is_paperairplane:
        aeroprofile(0.004,0.005,0.002)
    elif is_paperball:
        aeroprofile(0.04,0.55,0.0028)
    else:
        aeroprofile(0.145,0.35,0.0042)
    
    if true_iheight == "0":
        true_iheight = 0.001
    if true_gravity == "g":
        true_gravity = 9.80665

    if not bool(true_density):
        true_density = 1.225
    if not bool(true_cd):
        true_cd = 0.445
    if not bool(true_area):
        true_area = 0.00126
    if not bool(true_mass):
        true_mass = 0.0027
    if true_iheight == "0":
        true_iheight = bool(true_iheight) + 0.0001
    
    nindependent = 0
    ndependent = 0

    if bool(true_ivelocity):
        result_ivelocity = true_ivelocity
        nindependent += 1
    if bool(true_iheight):
        result_iheight = true_iheight
        nindependent += 1
    if bool(true_iangle):
        result_iangle = true_iangle
        nindependent += 1
    if bool(true_gravity):
        result_gravity = true_gravity
        nindependent += 1
    if bool(true_distance):
        result_distance = true_distance
        ndependent += 1
        depprofile = "distance"
    if bool(true_maxheight):
        result_maxheight = true_maxheight
        ndependent += 1
        depprofile = "maxheight"
    if bool(true_time):
        result_time = true_time
        ndependent += 1
        depprofile = "time"
    if bool(true_fvelocity):
        result_fvelocity = true_fvelocity
        ndependent += 1
        depprofile = "fvelocity"

    if nindependent < 3:
        print("insufficient data provided, provide at least 3 independent variables (initial velocity, initial height, launch angle, or gravity")
        load_trajectory = False
    elif nindependent == 3 and ndependent == 0: 
        print("insufficient data provided, provide at least 1 dependent variable (total distance, peak height, time, final velocity, impact angle alongside missing launch parameter")
        load_trajectory = False
    elif ndependent == 1 and not bool(true_gravity) and bool(true_fvelocity):
        print("specific case: missing variables cannot be inferred since energy is conserved and increasing gravity keeps energy simulataneously conserved, while drag acts at the same rate for both scenarios")
        load_trajectory = False
    elif bool(true_fvelocity) and bool(true_ivelocity):
        if true_fvelocity > true_ivelocity:
            print("Impossible Scenario, total velocity cannot increase during projectile motion")
            load_trajectory = False
    elif nindependent == 4:
        list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,true_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
        result_distance = list_distance[-1]
        result_maxheight = max(list_height)
        result_time = list_time[-1]
        result_fvelocity = list_velocity[-1]
        result_fangle = list_angle[-1]
        uncertainty = 0
        iterations = 0
        if allow_timestamps:
            print("\nNo timestamps available due to no performed iterations")
    else:
        result_ivelocity,result_iheight,result_iangle,result_gravity,uncertainty,iterations = iterative_solve(true_ivelocity,true_iheight,true_iangle,true_gravity,true_distance,true_maxheight,true_time,true_fvelocity,true_mass,true_density,true_cd,true_area,allow_timestamps,depprofile)
    
    list_height, list_distance, list_time, list_velocity, list_angle = simul(result_ivelocity,result_iheight,result_iangle,result_gravity,true_mass,true_density,true_cd,true_area)
    
    if depprofile == "distance":
        result_maxheight = max(list_height)
        result_time = list_time[-1]
        result_fvelocity = list_velocity[-1]
        result_fangle = list_angle[-1]
    if depprofile == "maxheight":
        result_distance = list_distance[-1]
        result_fvelocity = list_velocity[-1]
        result_time = list_time[-1]
        result_fangle = list_angle[-1]
    if depprofile == "time":
        result_distance = list_distance[-1]
        result_maxheight = max(list_height)
        result_fvelocity = list_velocity[-1]
        result_fangle = list_angle[-1]
    if depprofile == "fvelocity":
        result_distance = list_distance[-1]
        result_maxheight = max(list_height)
        result_time = list_time[-1]
        result_fangle = list_angle[-1]

    if load_trajectory:
        print(f"\nTrajectory Data:\n")
        print(f"Distance Travelled: {round(result_distance,3)} meters")
        print(f"Peak Height Reached: {round(result_maxheight,3)} meters")
        print(f"Total Time: {round(result_time,3)} seconds")
        print(f"Final Speed: {round(result_fvelocity,3)} meters/second")
        print(f"Impact Angle: {round(result_fangle,3)} degrees")
        print(f"Iterative Relative Uncertainty (0-1): {round(abs(uncertainty),8)}")
        print(f"Iterations Completed: {iterations}")
        print(f"\nParameters:\n")
        print(f"Initial Velocity: {round(result_ivelocity,3)} meters/second")
        print(f"Initial Height: {round(result_iheight,3)} meters")
        print(f"Launch Angle: {round(result_iangle,3)} degrees")
        print(f"Ambient Gravity: {round(result_gravity,3)} meters/second squared")

    if allow_energyanalysis:
        index = int(list_height.index(max(list_height)))
        energy(result_ivelocity,result_gravity,result_iheight,result_maxheight,true_mass,result_fvelocity,list_velocity,index)

if __name__ == "__main__":
    main()