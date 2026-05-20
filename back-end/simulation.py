import math

def simul(true_ivelocity,true_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area):
    list_height = [float(true_iheight)]
    list_distance = [0]
    list_velocity = [float(true_ivelocity)]
    list_angle = [float(true_iangle)]
    list_time = [0]
    true_iangle *= (2 * math.pi / 360)
    ivelocity_x = float(true_ivelocity) * math.cos(true_iangle)
    ivelocity_y = float(true_ivelocity) * math.sin(true_iangle)
    instvelocity_x = ivelocity_x
    instvelocity_y = ivelocity_y
    insttime = 0
    instdistance = 0
    instvelocity = 0
    instheight = float(true_iheight)
    instangle = true_iangle
    while float(instheight) > 0:
        instvelocity_y -= ((true_mass * true_gravity) + (1/2 * true_density * true_cd * true_area * instvelocity_y ** 2)) / true_mass * 0.001
        instvelocity_x -= (1/2 * true_density * true_cd * true_area * instvelocity_x ** 2) / true_mass * 0.001
        instvelocity = math.sqrt(instvelocity_x ** 2 + instvelocity_y ** 2)
        instheight += instvelocity_y * 0.001
        instdistance += instvelocity_x * 0.001
        instangle = math.atan2(instvelocity_y, instvelocity_x) * (360 / (2 * math.pi))
        list_height.append(float(instheight))
        list_distance.append(float(instdistance))
        list_velocity.append(float(instvelocity))
        list_angle.append(float(instangle))
        list_time.append(float(insttime))
        insttime += 0.001
    
    return list_height, list_distance, list_time, list_velocity, list_angle