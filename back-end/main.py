from simulation.py import simul
from solver.py import iterative_solve
from constraint.py import constrain
from energyanalysis.py import energy
from trajectory_matplotlib.py import graph_trajectory
from energy_matplotlib.py import graph_energy
from aeropreset.py import aeroprofile

if __name__ == "__main__":
    main()

def main():
    true_ivelocity = 20
    constrain(true_ivelocity,0,50)
    true_iheight = 20
    constrain(true_iheight,0,50)
    if true_iheight == "0":
        true_iheight = 0.001
    
    true_iangle = 45
    if bool(true_iangle):
        true_iangle = int(true_iangle)
        if true_iangle > 90 or true_iangle < -90:
            print(f"regard constraints for {true_iangle}, enter a value between -90 and 90 degrees")
            load_trajectory = False
    
    true_gravity = "g"
    if bool(true_gravity):
        if true_gravity == "g":
            true_gravity = 9.80665
        else:
            true_gravity = float(true_gravity)
            if true_gravity > 50 or true_iangle < 0:
                print(f"regard constraints for {true_gravity}, enter a value between 0 and 50 m/s^2")
                load_trajectory = False
    
    true_distance = ""
    constrain(true_distance,0,100)
    true_maxheight = ""
    constrain(true_maxheight,0,100)
    true_time = ""
    constrain(true_time,0,10)
    true_fvelocity = ""
    constrain(true_fvelocity,0,100)

    is_baseball = True
    is_football = False
    is_pingpongball = False
    is_soccerball = False
    is_tennisball = False
    is_paperairplane = False
    is_paperball = False
    allow_timestamps = True
    allow_energyanalysis = True
    load_trajectory = True

    if is_baseball:
        aeroprofile(0.145,0.35,0.0042)
    elif is_football:
        aeroprofile(0.415,0.06,0.0365)
    elif is_pingpongball:
        aeroprofile(0.003,0.48,0.0013)
    elif is_soccerball:
        aeroprofile(0.415,0.25,0.0375)
    elif is_tennisball:
        aeroprofile(0.057,0.6,0.0035)
    elif is_paperairplane:
        aeroprofile(0.004,0.005,0.002)
    elif is_paperball:
        aeroprofile(0.04,0.55,0.0028)
    else:
        true_mass = input("Enter projectile mass (that of a baseball will be assumed otherwise) (kg) (larger than one - 50 kg accepted) ")
        constrain(true_mass,0.001,50)
        true_density = input("Enter fluid density (air will be assumed otherwise) (kg/m^3) (0.5-3 kg/m^3) ")
        constrain(true_density,0.5,3)
        true_cd = input("Enter drag coefficient (that of a baseball will be assumed otherwise) (smaller than 1 and larger than 0 accepted) ")
        constrain(true_cd,0.001,0.999)
        true_area = input("Enter projectile cross-sectional area (that of a baseball will be assumed otherwise) (m^2) (larger than one - 20 m^3 accepted) ")
        constrain(true_area,0.001,20)
    
    if bool(true_fvelocity) and bool(true_ivelocity):
        if true_fvelocity > true_ivelocity:
            print("Impossible Scenario, total velocity cannot increase during projectile motion")
            load_trajectory = False
    
    if allow_timestamps_str == "True" or allow_timestamps_str == "Yes" or allow_timestamps_str == "true" or allow_timestamps_str == "yes" or allow_timestamps_str == " True" or allow_timestamps_str == " Yes" or allow_timestamps_str == " true" or allow_timestamps_str == " yes":
        allow_timestamps = True
    else:
        allow_timestamps = False
    if allow_energyanalysis_str == "True" or allow_energyanalysis_str == "Yes" or allow_energyanalysis_str == "true" or allow_energyanalysis_str == "yes" or allow_energyanalysis_str == " True" or allow_energyanalysis_str == " Yes" or allow_energyanalysis_str == " true" or allow_energyanalysis_str == " yes":
        allow_energyanalysis = True
    else:
        allow_energyanalysis = False
    if not bool(true_density):
        true_density = 1.225
    if not bool(true_cd):
        true_cd = 0.35
    if not bool(true_area):
        true_area = 0.0043
    if not bool(true_mass):
        true_mass = 0.145
    if true_iheight == "0":
        true_iheight = bool(true_iheight) + 0.0001
    
    result_ivelocity = 0
    result_iheight = 0
    result_iangle1 = 0
    result_iangle2 = 0
    result_gravity = 0
    result_distance = 0
    result_maxheight = 0
    result_time = 0
    result_fvelocity = 0
    result_fangle = 0
        
    nindependent = 0
    ndependent = 0
    if bool(true_ivelocity):
        result_ivelocity = float(true_ivelocity)
        nindependent += 1
    if bool(true_iheight):
        result_iheight = float(true_iheight)
        nindependent += 1
    if bool(true_iangle):
        result_iangle1 = float(true_iangle)
        nindependent += 1
    if bool(true_gravity):
        result_gravity = float(true_gravity)
        nindependent += 1
    if bool(true_distance):
        result_distance = float(true_distance)
        ndependent += 1
    if bool(true_maxheight):
        result_maxheight = float(true_maxheight)
        ndependent += 1
    if bool(true_fvelocity):
        result_fvelocity = float(true_fvelocity)
        ndependent += 1
    if bool(true_time):
        result_time = float(true_time)
        ndependent += 1
    
    if nindependent < 3:
        print("insufficient data provided, provide at least 3 independent variables (initial velocity, initial height, launch angle, or gravity")
        load_trajectory = False
    elif ndependent == 0 and not nindependent == 4:
        print("insufficient data provided, provide at least 1 dependent variable (total distance, peak height, time, final velocity, impact angle")
        load_trajectory = False
    elif nindependent == 3 and not bool(true_gravity) and bool(true_fvelocity):
        print("specific case: missing variables cannot be inferred since energy is conserved and increasing gravity keeps energy simulataneously conserved, while drag acts at the same rate for both scenarios")
        load_trajectory = False
    elif nindependent == 4:
        list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,true_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
        result_distance = list_distance[-1]
        result_maxheight = max(list_height)
        result_time = list_time[-1]
        result_fvelocity = list_velocity[-1]
        result_fangle = list_angle[-1]
        uncertainty = 0
        if allow_timestamps:
            print("\nNo timestamps available due to no performed iterations")
    else:
        iterative_solve(true_ivelocity,true_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)

    list_height, list_distance, list_time, list_velocity, list_angle = simul(result_ivelocity,result_iheight,result_iangle1,result_gravity,true_mass,true_density,true_cd,true_area)
    
    result_distance = float(list_distance[-1])
    result_time = float(list_time[-1])
    result_fvelocity = float(list_velocity[-1])
    result_fangle = float(list_angle[-1])
    result_maxheight = float(max(list_height))

    if load_trajectory:
        graph_trajectory(list_distance,list_height)
        print(f"\nTrajectory Data:\n")
        print(f"Distance Travelled: {round(result_distance,2)} meters")
        print(f"Peak Height Reached: {round(result_maxheight,2)} meters")
        print(f"Total Time: {round(result_time,2)} seconds")
        print(f"Final Speed: {round(result_fvelocity,2)} meters/second")
        print(f"Impact Angle: {round(result_fangle,2)} degrees")
        print(f"Iteration Relative Uncertainty (0-1): {round(abs(uncertainty),8)}")
        print(f"\nParameters:\n")
        print(f"Initial Velocity: {round(result_ivelocity,2)} meters/second")
        print(f"Initial Height: {round(result_iheight,2)} meters")
        print(f"Launch Angle: {round(result_iangle1,2)} degrees")
        print(f"Ambient Gravity: {round(result_gravity,2)} meters/second squared")

    if allow_energyanalysis:
        energy(result_ivelocity,result_gravity,result_iheight,true_mass,result_fvelocity,list_velocity,list_height)
        graph_energy(list_time,list_velocity,list_height,true_mass,true_gravity)