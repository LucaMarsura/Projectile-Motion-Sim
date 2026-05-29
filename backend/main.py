import sys, json, base64
from io import BytesIO
from simulation import simulation
from solver import iterative_solve
from energyanalysis import energy
from trajectorygraphing import graph_trajectory


def main():

    data = json.loads(sys.stdin.read())

    true_ivelocity = float(data["ivelocity"]) if data["ivelocity"] != "" else ""
    true_iheight   = (float(data["iheight"]) + 0.0001) if data["iheight"] != "" else ""
    true_iangle    = float(data["iangle"]) if data["iangle"] != "" else ""
    true_gravity   = float(data["gravity"]) if data["gravity"] != "" else ""
    true_distance  = float(data["distance"]) if data["distance"] != "" else ""
    true_maxheight = float(data["maxheight"]) if data["maxheight"] != "" else ""
    true_time      = float(data["time"]) if data["time"] != "" else ""
    true_fvelocity = float(data["fvelocity"]) if data["fvelocity"] != "" else ""

    drag_presets = {
        "aeropreset_baseball":    {"mass": 0.145,  "cd": 0.35,  "area": 0.0042},
        "aeropreset_football":    {"mass": 0.415,  "cd": 0.06,  "area": 0.0365},
        "aeropreset_ppball":      {"mass": 0.0027, "cd": 0.445, "area": 0.00126},
        "aeropreset_soccerball":  {"mass": 0.415,  "cd": 0.25,  "area": 0.0375},
        "aeropreset_tennisball":  {"mass": 0.057,  "cd": 0.6,   "area": 0.0035},
        "aeropreset_paperplane":  {"mass": 0.004,  "cd": 0.005, "area": 0.002},
        "aeropreset_paperball":   {"mass": 0.04,   "cd": 0.55,  "area": 0.0028},
        "aeropreset_golfball":    {"mass": 0.046,  "cd": 0.24,  "area": 0.00143},
        "aeropreset_basketball":  {"mass": 0.623,  "cd": 0.47,  "area": 0.0456},
        "aeropreset_bowlingball": {"mass": 7.0,    "cd": 0.47,  "area": 0.0366},
        "aeropreset_frisbee":     {"mass": 0.175,  "cd": 0.08,  "area": 0.0707},
        "aeropreset_arrow":       {"mass": 0.025,  "cd": 0.004, "area": 0.00005},
        "aeropreset_spear":       {"mass": 0.4,    "cd": 0.04,  "area": 0.00008},
        "aeropreset_shuttlecock": {"mass": 0.005,  "cd": 0.60,  "area": 0.0029}
    }

    density_presets = {
        "denpreset_air":         {"density": 1.225},
        "denpreset_vacuum":      {"density": 0.0001},
        "denpreset_water":       {"density": 1000},
        "denpreset_oil":         {"density": 870},
        "denpreset_highaltair":  {"density": 0.4},
        "denpreset_syrup":       {"density": 1380},
        "denpreset_moltenmetal": {"density": 6980}
    }

    drag_selected    = data.get("aeropreset", "")
    density_selected = data.get("denpreset", "")

    if drag_selected in drag_presets:
        true_mass = drag_presets[drag_selected]["mass"]
        true_cd   = drag_presets[drag_selected]["cd"]
        true_area = drag_presets[drag_selected]["area"]
    else:
        true_mass = float(data["mass"])
        true_cd   = float(data["cd"])
        true_area = float(data["area"])

    if density_selected in density_presets:
        true_density = density_presets[density_selected]["density"]
    else:
        true_density = float(data["density"])

    depvariable = "none"
    uncertainty = 0
    iterations  = 0
    nindep      = 0
    ndep        = 0

    if bool(true_ivelocity): nindep += 1
    if bool(true_iheight):   nindep += 1
    if bool(true_iangle):    nindep += 1
    if bool(true_gravity):   nindep += 1

    if bool(true_distance):  ndep += 1; depvariable = "distance"
    if bool(true_maxheight): ndep += 1; depvariable = "maxheight"
    if bool(true_time):      ndep += 1; depvariable = "time"
    if bool(true_fvelocity): ndep += 1; depvariable = "fvelocity"

    if nindep < 3:
        print(json.dumps({"error": "Insufficient data: provide at least 3 independent variables.", "prints": [], "graph1": "", "graph2": ""}))
        return
    elif nindep == 3 and ndep == 0:
        print(json.dumps({"error": "Insufficient data: provide at least 1 dependent variable.", "prints": [], "graph1": "", "graph2": ""}))
        return
    elif ndep == 1 and not bool(true_gravity) and bool(true_fvelocity):
        print(json.dumps({"error": "Specific case: missing variables cannot be inferred.", "prints": [], "graph1": "", "graph2": ""}))
        return
    elif bool(true_fvelocity) and bool(true_ivelocity):
        if true_fvelocity > true_ivelocity:
            print(json.dumps({"error": "Impossible scenario: total velocity cannot increase during projectile motion.", "prints": [], "graph1": "", "graph2": ""}))
            return

    if nindep == 4:
        result_ivelocity = true_ivelocity
        result_iheight   = true_iheight
        result_iangle    = true_iangle
        result_gravity   = true_gravity
    else:
        result_ivelocity, result_iheight, result_iangle, result_gravity, uncertainty, iterations = iterative_solve(true_ivelocity, true_iheight, true_iangle, true_gravity, true_distance, true_maxheight, true_time, true_fvelocity, true_mass, true_density, true_cd, true_area, False, depvariable)

    list_height, list_distance, list_time, list_velocity, list_angle = simulation(result_ivelocity, result_iheight, result_iangle, result_gravity, true_mass, true_density, true_cd, true_area)

    result_distance  = list_distance[-1]
    result_maxheight = max(list_height)
    result_time      = list_time[-1]
    result_fvelocity = list_velocity[-1]
    result_fangle    = list_angle[-1]

    traj_graph           = graph_trajectory(list_distance, list_height)
    txt_energy, graph_energy = energy(list_time, list_distance, list_height, list_velocity, true_mass, result_gravity)

    txt_main = [
        "Trajectory Data:",
        f"Distance Travelled: {round(result_distance, 3)} meters",
        f"Peak Height Reached: {round(result_maxheight, 3)} meters",
        f"Total Time: {round(result_time, 3)} seconds",
        f"Final Speed: {round(result_fvelocity, 3)} meters/second",
        f"Impact Angle: {round(result_fangle, 3)} degrees",
        f"Iterative Relative Uncertainty (0-1): {round(abs(uncertainty), 8)}",
        f"Iterations Completed: {iterations}",
        "",
        "Parameters:",
        f"Initial Velocity: {round(result_ivelocity, 3)} meters/second",
        f"Initial Height: {round(result_iheight, 3)} meters",
        f"Launch Angle: {round(result_iangle, 3)} degrees",
        f"Ambient Gravity: {round(result_gravity, 3)} meters/second squared",
    ]

    print(json.dumps({"prints": txt_main + txt_energy, "graph1": traj_graph, "graph2": graph_energy}))


if __name__ == "__main__":
    main()
