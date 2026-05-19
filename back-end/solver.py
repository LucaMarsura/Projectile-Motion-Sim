from simulation.py import simul

def iterative_solve(true_ivelocity,true_iheight,true_iangle,true_mass,true_density,true_cd,true_area):
    uncertainty = 1
    iterations = 0
    if not bool(true_ivelocity):
        experimental_ivelocity = 20
        x = 10
        if bool(true_distance):
            true_distance = float(true_distance)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(experimental_ivelocity,true_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_distance = max(list_distance)
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial velocity: {round(experimental_ivelocity,3)} m/s\nResultant trial distance: {round(trial_distance,3)} m\nTrue distance: {round(true_distance,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_distance > true_distance:
                    experimental_ivelocity -= x
                elif trial_distance < true_distance:
                    experimental_ivelocity += x
                x /= 2
                iterations += 1
                uncertainty = (trial_distance - true_distance) / true_distance
            result_ivelocity = float(experimental_ivelocity)
            result_maxheight = max(list_height)
            result_time = float(max(list_time))
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        if bool(true_maxheight):
            true_maxheight = float(true_maxheight)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(experimental_ivelocity,true_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_maxheight = max(list_height)
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial velocity: {round(experimental_ivelocity,3)} m/s\nResultant trial maximum height: {round(trial_maxheight,3)} m\nTrue maximum height: {round(true_maxheight,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_maxheight > true_maxheight:
                    experimental_ivelocity -= x
                elif trial_maxheight < true_maxheight:
                    experimental_ivelocity += x
                x /= 2
                iterations += 1
                uncertainty = (trial_maxheight - true_maxheight) / true_maxheight
            result_ivelocity = float(experimental_ivelocity)
            result_distance = list_distance[-1]
            result_time = float(max(list_time))
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_time):
            true_time = float(true_time)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(experimental_ivelocity,true_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_time = list_time[-1]
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial velocity: {round(experimental_ivelocity,3)} m/s\nResultant trial time: {round(trial_time,3)} m\nTrue time: {round(true_time,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_time > true_time:
                    experimental_ivelocity -= x
                elif trial_time < true_time:
                    experimental_ivelocity += x
                x /= 2
                iterations += 1
                uncertainty = (trial_time - true_time) / true_time
            result_ivelocity = float(experimental_ivelocity)
            result_distance = list_distance[-1]
            result_maxheight = max(list_height)
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_fvelocity):
            true_fvelocity = float(true_fvelocity)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(experimental_ivelocity,true_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_fvelocity = list_velocity[-1]
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial velocity: {round(experimental_ivelocity,3)} m/s\nResultant trial final velocity: {round(trial_fvelocity,3)} m\nTrue final velocity: {round(true_fvelocity,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_fvelocity > true_fvelocity:
                    experimental_ivelocity -= x
                elif trial_fvelocity < true_fvelocity:
                    experimental_ivelocity += x
                x /= 2
                iterations += 1
                uncertainty = (trial_fvelocity - true_fvelocity) / true_fvelocity
            result_ivelocity = float(experimental_ivelocity)
            result_distance = list_distance[-1]
            result_maxheight = max(list_height)
            result_time = list_time[-1]
            result_fangle = list_angle[-1]
    elif not bool(true_iheight):
        experimental_iheight = 100
        x = 50
        if bool(true_distance):
            true_distance = float(true_distance)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,experimental_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_distance = max(list_distance)
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial height: {round(experimental_iheight,3)} m\nResultant trial distance: {round(trial_distance,3)} m\nTrue distance: {round(true_distance,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_distance > true_distance:
                    experimental_iheight -= x
                elif trial_distance < true_distance:
                    experimental_iheight += x
                x /= 2
                iterations += 1
                uncertainty = (trial_distance - true_distance) / true_distance
            result_iheight = float(experimental_iheight)
            result_maxheight = max(list_height)
            result_time = list_time[-1]
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_maxheight):
            true_maxheight = float(true_maxheight)
            experimental_iheight = 100
            x = 50
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,experimental_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_maxheight = max(list_height)
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial height: {round(experimental_iheight,3)} m\nResultant trial maximum height: {round(trial_maxheight,3)} m\nTrue maximum height: {round(true_maxheight,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_maxheight > true_maxheight:
                    experimental_iheight -= x
                elif trial_maxheight < true_maxheight:
                    experimental_iheight += x
                x /= 2
                iterations += 1
                uncertainty = (trial_maxheight - true_maxheight) / true_maxheight
            result_iheight = float(experimental_iheight)
            result_distance = list_distance[-1]
            result_time = list_time[-1]
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_time):
            true_time = float(true_time)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,experimental_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_time = list_time[-1]
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial height: {round(experimental_iheight,3)} m\nResultant trial time: {round(trial_time,3)} m\nTrue time: {round(true_time,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_time > true_time:
                    experimental_iheight -= x
                elif trial_time < true_time:
                    experimental_iheight += x
                x /= 2
                iterations += 1
                uncertainty = (trial_time - true_time) / true_time
            result_iheight = float(experimental_iheight)
            result_distance = list_distance[-1]
            result_maxheight = max(list_height)
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_fvelocity):
            true_fvelocity = float(true_fvelocity)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,experimental_iheight,true_iangle,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_fvelocity = list_velocity[-1]
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial height: {round(experimental_iheight,3)} m\nResultant trial final velocity: {round(trial_fvelocity,3)} m\nTrue final velocity: {round(true_fvelocity,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_fvelocity > true_fvelocity:
                    experimental_iheight -= x
                elif trial_fvelocity < true_fvelocity:
                    experimental_iheight += x
                x /= 2
                iterations += 1
                uncertainty = (trial_fvelocity - true_fvelocity) / true_fvelocity
            result_iheight = float(experimental_iheight)
            result_distance = list_distance[-1]
            result_maxheight = max(list_height)
            result_time = list_time[-1]
            result_fangle = list_angle[-1]
    elif not bool(true_iangle):
        experimental_iangle1 = 45
        x = 22.5
        if bool(true_distance):
            true_distance = float(true_distance)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,true_iheight,experimental_iangle1,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_distance = list_distance[-1]
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial angle: {round(experimental_iangle1,3)} degrees\nnResultant trial distance: {round(trial_distance,3)} m\nTrue distance: {round(true_distance,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_distance > true_distance:
                    experimental_iangle1 -= x
                elif trial_distance < true_distance:
                    experimental_iangle1 += x
                x /= 2
                iterations += 1
                uncertainty = (trial_distance - true_distance) / true_distance
            result_iangle1 = float(experimental_iangle1)
            result_maxheight = max(list_height)
            result_time = list_time[-1]
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_maxheight):
            true_maxheight = float(true_maxheight)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle =  simul(true_ivelocity,true_iheight,experimental_iangle1,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_maxheight = max(list_height)
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial angle: {round(experimental_iangle1,3)} degrees\nResultant trial maximum height: {round(trial_maxheight,3)} m\nTrue maximum height: {round(true_maxheight,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_maxheight > true_maxheight:
                    experimental_iangle1 -= x
                elif trial_maxheight < true_maxheight:
                    experimental_iangle1 += x
                x /= 2
                iterations += 1
                uncertainty = (trial_maxheight - true_maxheight) / true_maxheight
            result_iangle1 = float(experimental_iangle1)
            result_distance = list_distance[-1]
            result_time = list_time[-1]
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_time):
            true_time = float(true_time)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,true_iheight,experimental_iangle1,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_time = list_time[-1]
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial angle: {round(experimental_iangle1,3)} degrees\nResultant trial time: {round(trial_time,3)} m\nTrue time: {round(true_time,3)} m\nRelative uncertainty: {round(abs(uncertainty),5)}")
                if trial_time > true_time:
                    experimental_iangle1 -= x
                elif trial_time < true_time:
                    experimental_iangle1 += x
                x /= 2
                iterations += 1
                uncertainty = (trial_time - true_time) / true_time
            result_iangle1 = float(experimental_iangle1)
            result_distance = list_distance[-1]
            result_maxheight = max(list_height)
            result_time = list_time[-1]
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_fvelocity):
            true_fvelocity = float(true_fvelocity)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,true_iheight,experimental_iangle1,true_gravity,true_mass,true_density,true_cd,true_area)
                trial_fvelocity = list_fvelocity[-1]
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested initial angle: {experimental_iangle1} degrees\nResultant trial final velociy: {trial_fvelocity} m\nTrue final velocity: {true_fvelocity} m\nRelative uncertainty: {uncertainty}")
                if trial_fvelocity > true_fvelocity:
                    experimental_iangle1 -= x
                elif trial_fvelocity < true_fvelocity:
                    experimental_iangle1 += x
                x /= 2
                iterations += 1
                uncertainty = (trial_fvelocity - true_fvelocity) / true_fvelocity
            result_iangle1 = float(experimental_iangle1)
            result_gravity = true_gravity
            result_distance = list_distance[-1]
            result_maxheight = max(list_height)
            result_time = list_time[-1]
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
    elif not bool(true_gravity):
        experimental_gravity = 25
        x = 12.5
        if bool(true_distance):
            true_distance = float(true_distance)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,true_iheight,true_iangle,experimental_gravity,true_mass,true_density,true_cd,true_area)
                trial_distance = list_distance[-1]
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested gravity:  {experimental_gravity} m/s^2\nResultant trial distance: {trial_distance} m\nTrue distance: {true_distance} m\nRelative uncertainty: {uncertainty}")
                if trial_distance > true_distance:
                    experimental_gravity += x
                elif trial_distance < true_distance:
                    experimental_gravity -= x
                x /= 2
                iterations += 1
                uncertainty = (trial_distance - true_distance) / true_distance
            result_gravity = float(experimental_gravity)
            result_maxheight = max(list_height)
            result_time = list_time[-1]
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_maxheight):
            true_maxheight = float(true_maxheight)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,true_iheight,true_iangle,experimental_gravity,true_mass,true_density,true_cd,true_area)
                trial_maxheight = max(list_height)
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested gravity:  {experimental_gravity} m/s^2\nResultant trial maximum height: {trial_maxheight} m\nTrue maximum height: {true_maxheight} m\nRelative uncertainty: {uncertainty}")
                if trial_maxheight > true_maxheight:
                    experimental_gravity += x
                elif trial_distance < true_distance:
                    experimental_gravity -= x
                x /= 2
                iterations += 1
                uncertainty = (trial_maxheight - true_maxheight) / true_maxheight
            result_gravity = float(experimental_gravity)
            result_distance = list_distance[-1]
            result_time = list_time[-1]
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]
        elif bool(true_time):
            true_time = float(true_time)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simul(true_ivelocity,true_iheight,true_iangle,experimental_gravity,true_mass,true_density,true_cd,true_area)
                trial_time = list_time[-1]
                if allow_timestamps:
                    print(f"\nIteration {iterations + 1}\nTested gravity:  {experimental_gravity} m/s^2\nResultant trial time: {trial_time} m\nTrue time: {true_time} m\nRelative uncertainty: {uncertainty}")
                if trial_time > true_time:
                    experimental_gravity += x
                elif trial_time < true_time:
                    experimental_gravity -= x
                x /= 2
                iterations +=1
            result_gravity = float(experimental_gravity)
            result_distance = list_distance[-1]
            result_maxheight = max(list_height)
            result_fvelocity = list_velocity[-1]
            result_fangle = list_angle[-1]