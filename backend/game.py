import sys, json, random, base64
sys.path.append("backend")
from io import BytesIO
from simulation import simulation
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

AERO_PRESETS = {
    "aeropreset_baseball":   {"mass": 0.145,  "cd": 0.35,  "area": 0.0042},
    "aeropreset_football":   {"mass": 0.415,  "cd": 0.06,  "area": 0.0365},
    "aeropreset_ppball":     {"mass": 0.0027, "cd": 0.445, "area": 0.00126},
    "aeropreset_soccerball": {"mass": 0.415,  "cd": 0.25,  "area": 0.0375},
    "aeropreset_tennisball": {"mass": 0.057,  "cd": 0.6,   "area": 0.0035},
    "aeropreset_paperplane": {"mass": 0.004,  "cd": 0.005, "area": 0.002},
    "aeropreset_paperball":  {"mass": 0.04,   "cd": 0.55,  "area": 0.0028}
}

DEN_PRESETS = {
    "denpreset_air":    {"density": 1.225},
    "denpreset_vacuum": {"density": 0.0001},
    "denpreset_water":  {"density": 1000},
    "denpreset_oil":    {"density": 870}
}

def pick_aero():
    return random.choice(list(AERO_PRESETS.keys()))

def pick_den():
    return random.choices(
        ["denpreset_air", "denpreset_vacuum", "denpreset_water", "denpreset_oil"],
        weights = [90, 5, 3, 2]
    )[0]

def pick_params():
    true_iheight  = round(random.uniform(0, 20), 1)
    true_gravity  = 9.81 if random.random() < 0.80 else round(random.uniform(1, 20), 2)
    if true_iheight > 0:
        true_iangle = round(random.uniform(-90, 90), 0)
    else:
        true_iangle = round(random.uniform(0, 90), 0)
    true_ivelocity = round(random.uniform(5, 40), 1)
    return true_ivelocity, true_iheight, true_iangle, true_gravity

def run_sim(ivelocity, iheight, iangle, gravity, mass, density, cd, area):
    list_height, list_distance, list_time, list_velocity, list_angle = simulation(
        ivelocity, float(iheight) + 0.0001, iangle, gravity, mass, density, cd, area
    )
    return list_height, list_distance

def build_graph(gametype, target, list_height = None, list_distance = None):
    fig, ax = plt.subplots(figsize = (6, 4))
    deviation = target * 0.02
    if gametype == "distance":
        ax.axvspan(target - deviation, target + deviation,
                   ymin = 0, ymax = 0.06,
                   color = "#0b5190", alpha = 0.25, label = "Target Zone (±2%)")
        ax.axvline(target, color = "#0b5190", linewidth = 1.5, linestyle = "--", alpha = 0.5)
    elif gametype == "maxheight":
        ax.axhspan(target - deviation, target + deviation,
                   color = "#0b5190", alpha = 0.25, label = "Target Zone (±2%)")
        ax.axhline(target, color = "#0b5190", linewidth = 1.5, linestyle = "--", alpha = 0.5)
    if list_height is not None and list_distance is not None:
        ax.plot(list_distance, list_height,
                color = "#e05c2a", linewidth = 2, label = "Your Trajectory")
    ax.set_xlim(left = 0)
    if gametype == "maxheight":
        ax.set_ylim(bottom = 0, top = target * 1.4)
    else:
        ax.set_ylim(bottom = 0)
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Projectile Trajectory")
    ax.legend(fontsize = 8)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format = "png", dpi = 120)
    buf.seek(0)
    graph = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return graph

def game_setup(body):
    previous_state = body.get("previous_state", None)
    if previous_state:
        aero_key   = previous_state["aeropreset"]
        den_key    = previous_state["denpreset"]
        hidden_var = previous_state["hidden_var"]
    else:
        aero_key   = pick_aero()
        den_key    = pick_den()
        hidden_var = random.choice(["ivelocity", "iheight", "iangle", "gravity"])
    aero = AERO_PRESETS[aero_key]
    den  = DEN_PRESETS[den_key]
    true_ivelocity, true_iheight, true_iangle, true_gravity = pick_params()
    list_height, list_distance = run_sim(
        true_ivelocity, true_iheight, true_iangle, true_gravity,
        aero["mass"], den["density"], aero["cd"], aero["area"]
    )
    gametype = random.choice(["distance", "maxheight"])
    target   = list_distance[-1] if gametype == "distance" else max(list_height)
    known_vars = {
        "ivelocity": true_ivelocity,
        "iheight":   true_iheight,
        "iangle":    true_iangle,
        "gravity":   true_gravity
    }
    graph = build_graph(gametype, target)
    deviation = target * 0.02
    print(json.dumps({
        "graph":      graph,
        "hidden_var": hidden_var,
        "known_vars": known_vars,
        "target":     target,
        "target_min": round(target - deviation, 3),
        "target_max": round(target + deviation, 3),
        "gametype":   gametype,
        "aeropreset": aero_key,
        "denpreset":  den_key,
        "mass":       aero["mass"],
        "cd":         aero["cd"],
        "area":       aero["area"],
        "density":    den["density"]
    }))

def game_run(body):
    hidden_var = body["hidden_var"]
    attempt    = float(body["attempt_value"])
    known_vars = body["known_vars"]
    target     = body["target"]
    gametype   = body["gametype"]
    aero       = AERO_PRESETS[body["aeropreset"]]
    den        = DEN_PRESETS[body["denpreset"]]
    vars_full  = dict(known_vars)
    vars_full[hidden_var] = attempt
    list_height, list_distance = run_sim(
        vars_full["ivelocity"], vars_full["iheight"],
        vars_full["iangle"],    vars_full["gravity"],
        aero["mass"], den["density"], aero["cd"], aero["area"]
    )
    result    = list_distance[-1] if gametype == "distance" else max(list_height)
    deviation = abs((result - target) / target) * 100
    success   = deviation <= 2.0
    graph = build_graph(gametype, target, list_height, list_distance)
    print(json.dumps({
        "graph":     graph,
        "success":   success,
        "deviation": deviation
    }))

data = json.loads(sys.stdin.read())
if data["mode"] == "setup":
    game_setup(data)
elif data["mode"] == "run":
    game_run(data)