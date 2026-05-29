from simulation import simulation


def iterative_solve(true_ivelocity, true_iheight, true_iangle, true_gravity, true_distance, true_maxheight, true_time, true_fvelocity, true_mass, true_density, true_cd, true_area, allow_timestamps, depvariable):
    uncertainty = 1
    iterations  = 0

    if true_ivelocity == "":
        experimental_ivelocity = 20
        search_step = 10

        if bool(true_distance):
            true_distance = float(true_distance)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(experimental_ivelocity, true_iheight, true_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_distance = max(list_distance)

                #iterative search, alter experimental launch parameter based on relation between true result and calculated result
                if trial_distance > true_distance:
                    experimental_ivelocity -= search_step
                elif trial_distance < true_distance:
                    experimental_ivelocity += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_distance - true_distance) / true_distance

        if bool(true_maxheight):
            true_maxheight = float(true_maxheight)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(experimental_ivelocity, true_iheight, true_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_maxheight = max(list_height)
                if trial_maxheight > true_maxheight:
                    experimental_ivelocity -= search_step
                elif trial_maxheight < true_maxheight:
                    experimental_ivelocity += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_maxheight - true_maxheight) / true_maxheight

        elif bool(true_time):
            true_time = float(true_time)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(experimental_ivelocity, true_iheight, true_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_time = list_time[-1]
                if trial_time > true_time:
                    experimental_ivelocity -= search_step
                elif trial_time < true_time:
                    experimental_ivelocity += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_time - true_time) / true_time

        elif bool(true_fvelocity):
            true_fvelocity = float(true_fvelocity)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(experimental_ivelocity, true_iheight, true_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_fvelocity = list_velocity[-1]
                if trial_fvelocity > true_fvelocity:
                    experimental_ivelocity -= search_step
                elif trial_fvelocity < true_fvelocity:
                    experimental_ivelocity += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_fvelocity - true_fvelocity) / true_fvelocity

        result_ivelocity = experimental_ivelocity
        result_iheight   = true_iheight
        result_iangle    = true_iangle
        result_gravity   = true_gravity

    elif true_iheight == "":
        experimental_iheight = 100
        search_step = 50

        if bool(true_distance):
            true_distance = float(true_distance)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, experimental_iheight, true_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_distance = max(list_distance)
                if trial_distance > true_distance:
                    experimental_iheight -= search_step
                elif trial_distance < true_distance:
                    experimental_iheight += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_distance - true_distance) / true_distance

        elif bool(true_maxheight):
            true_maxheight = float(true_maxheight)
            experimental_iheight = 100
            search_step = 50
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, experimental_iheight, true_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_maxheight = max(list_height)
                if trial_maxheight > true_maxheight:
                    experimental_iheight -= search_step
                elif trial_maxheight < true_maxheight:
                    experimental_iheight += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_maxheight - true_maxheight) / true_maxheight

        elif bool(true_time):
            true_time = float(true_time)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, experimental_iheight, true_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_time = list_time[-1]
                if trial_time > true_time:
                    experimental_iheight -= search_step
                elif trial_time < true_time:
                    experimental_iheight += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_time - true_time) / true_time

        elif bool(true_fvelocity):
            true_fvelocity = float(true_fvelocity)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, experimental_iheight, true_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_fvelocity = list_velocity[-1]
                if trial_fvelocity > true_fvelocity:
                    experimental_iheight -= search_step
                elif trial_fvelocity < true_fvelocity:
                    experimental_iheight += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_fvelocity - true_fvelocity) / true_fvelocity

        result_ivelocity = true_ivelocity
        result_iheight   = experimental_iheight
        result_iangle    = true_iangle
        result_gravity   = true_gravity

    elif true_iangle == "":
        experimental_iangle = 0
        search_step = 45

        if bool(true_distance):
            true_distance = float(true_distance)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, true_iheight, experimental_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_distance = list_distance[-1]
                if trial_distance > true_distance:
                    experimental_iangle -= search_step
                elif trial_distance < true_distance:
                    experimental_iangle += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_distance - true_distance) / true_distance

        elif bool(true_maxheight):
            true_maxheight = float(true_maxheight)
            while abs(uncertainty) > 0.01 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, true_iheight, experimental_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_maxheight = max(list_height)
                if trial_maxheight > true_maxheight:
                    experimental_iangle -= search_step
                elif trial_maxheight < true_maxheight:
                    experimental_iangle += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_maxheight - true_maxheight) / true_maxheight

        elif bool(true_time):
            true_time = float(true_time)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, true_iheight, experimental_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_time = list_time[-1]
                if trial_time > true_time:
                    experimental_iangle -= search_step
                elif trial_time < true_time:
                    experimental_iangle += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_time - true_time) / true_time

        elif bool(true_fvelocity):
            true_fvelocity = float(true_fvelocity)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, true_iheight, experimental_iangle, true_gravity, true_mass, true_density, true_cd, true_area)
                trial_fvelocity = list_velocity[-1]
                if trial_fvelocity > true_fvelocity:
                    experimental_iangle -= search_step
                elif trial_fvelocity < true_fvelocity:
                    experimental_iangle += search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_fvelocity - true_fvelocity) / true_fvelocity

        result_ivelocity = true_ivelocity
        result_iheight   = true_iheight
        result_iangle    = experimental_iangle
        result_gravity   = true_gravity

    elif true_gravity == "":
        experimental_gravity = 25
        search_step = 12.5

        if bool(true_distance):
            true_distance = float(true_distance)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, true_iheight, true_iangle, experimental_gravity, true_mass, true_density, true_cd, true_area)
                trial_distance = list_distance[-1]
                if trial_distance > true_distance:
                    experimental_gravity += search_step
                elif trial_distance < true_distance:
                    experimental_gravity -= search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_distance - true_distance) / true_distance

        elif bool(true_maxheight):
            true_maxheight = float(true_maxheight)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, true_iheight, true_iangle, experimental_gravity, true_mass, true_density, true_cd, true_area)
                trial_maxheight = max(list_height)
                if trial_maxheight > true_maxheight:
                    experimental_gravity += search_step
                elif trial_maxheight < true_maxheight:
                    experimental_gravity -= search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_maxheight - true_maxheight) / true_maxheight

        elif bool(true_time):
            true_time = float(true_time)
            while abs(uncertainty) > 0.001 and iterations < 100:
                list_height, list_distance, list_time, list_velocity, list_angle = simulation(true_ivelocity, true_iheight, true_iangle, experimental_gravity, true_mass, true_density, true_cd, true_area)
                trial_time = list_time[-1]
                if trial_time > true_time:
                    experimental_gravity += search_step
                elif trial_time < true_time:
                    experimental_gravity -= search_step
                search_step /= 2
                iterations  += 1
                uncertainty  = (trial_time - true_time) / true_time

        result_ivelocity = true_ivelocity
        result_iheight   = true_iheight
        result_iangle    = true_iangle
        result_gravity   = experimental_gravity

    return result_ivelocity, result_iheight, result_iangle, result_gravity, uncertainty, iterations