import sys, json, random, base64
from io import BytesIO
from simulation import simulation
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.append("backend")

drag_presets = {
    "aeropreset_baseball": {"mass": 0.145, "cd": 0.35, "area": 0.0042},
    "aeropreset_football": {"mass": 0.415, "cd": 0.06, "area": 0.0365},
    "aeropreset_ppball": {"mass": 0.0027, "cd": 0.445, "area": 0.00126},
    "aeropreset_soccerball": {"mass": 0.415, "cd": 0.25, "area": 0.0375},
    "aeropreset_tennisball": {"mass": 0.057, "cd": 0.6, "area": 0.0035},
    "aeropreset_paperplane": {"mass": 0.004, "cd": 0.005, "area": 0.002},
    "aeropreset_paperball": {"mass": 0.04, "cd": 0.55, "area": 0.0028},
    "aeropreset_golfball": {"mass": 0.046, "cd": 0.24, "area": 0.00143},
    "aeropreset_basketball": {"mass": 0.623, "cd": 0.47, "area": 0.0456},
    "aeropreset_bowlingball": {"mass": 7.0, "cd": 0.47, "area": 0.0366},
    "aeropreset_frisbee": {"mass": 0.175, "cd": 0.08, "area": 0.0707},
    "aeropreset_arrow": {"mass": 0.025, "cd": 0.004, "area": 0.00005},
    "aeropreset_spear": {"mass": 0.4, "cd": 0.04, "area": 0.00008},
    "aeropreset_shuttlecock": {"mass": 0.005, "cd": 0.60, "area": 0.0029}
}

density_presets = {
    "denpreset_air": {"density": 1.225},
    "denpreset_vacuum": {"density": 0.0001},
    "denpreset_water": {"density": 1000},
    "denpreset_oil": {"density": 870},
    "denpreset_highaltair": {"density": 0.4},
    "denpreset_syrup": {"density": 1380},
    "denpreset_moltenmetal": {"density": 6980}
}

#parameter selection
def select_aero():
    return random.choices(
        ["aeropreset_baseball", "aeropreset_football", "aeropreset_ppball", "aeropreset_soccerball", "aeropreset_tennisball", "aeropreset_paperplane", "aeropreset_paperball", "aeropreset_golfball", "aeropreset_basketball", "aeropreset_bowlingball", "aeropreset_frisbee", "aeropreset_arrow", "aeropreset_spear", "aeropreset_shuttlecock"],
        weights=[12, 8, 6, 8, 8, 4, 4, 10, 8, 6, 8, 8, 6, 10]
    )[0]

def select_den():
    return random.choices(
        ["denpreset_air", "denpreset_vacuum", "denpreset_water", "denpreset_oil", "denpreset_highaltair", "denpreset_syrup", "denpreset_moltenmetal"],
        weights=[70, 10, 5, 5, 7, 2, 1]
    )[0]

def pick_variables():
    true_iheight = round(random.uniform(0, 20), 1)
    true_gravity = 9.81 if random.random() < 0.80 else round(random.uniform(1, 20), 2)
    true_iangle = round(random.uniform(10, 80), 0)
    true_ivelocity = round(random.uniform(5, 40), 1)
    return true_ivelocity, true_iheight, true_iangle, true_gravity

def create_graph(gametype, target, list_height=None, list_distance=None):
    fig, ax = plt.subplots(figsize=(6, 4))
    deviation = target * 0.02

    if gametype == "distance":
        ax.axvspan(target - deviation, target + deviation, ymin=0, ymax=0.06, color="#0b5190", alpha=0.25, label="Target Zone (±2%)")
        ax.axvline(target, color="#0b5190", linewidth=1.5, linestyle="--", alpha=0.5)
    elif gametype == "maxheight":
        ax.axhspan(target - deviation, target + deviation, color="#0b5190", alpha=0.25, label="Target Zone (±2%)")
        ax.axhline(target, color="#0b5190", linewidth=1.5, linestyle="--", alpha=0.5)

    if list_height is not None and list_distance is not None:
        ax.plot(list_distance, list_height, color="#e05c2a", linewidth=2, label="Your Trajectory")

    ax.set_xlim(left=0)
    if gametype == "maxheight":
        ax.set_ylim(bottom=0, top=target * 1.4)
    else:
        ax.set_ylim(bottom=0)

    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Projectile Trajectory")
    ax.legend(fontsize=8)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=120)
    buf.seek(0)
    graph = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return graph

def set_game(body):
    drag_selected = select_aero()
    density_selected = select_den()
    target_indep = random.choice(["ivelocity", "iheight", "iangle", "gravity"])

    drag = drag_presets[drag_selected]
    density = density_presets[density_selected]

    true_ivelocity, true_iheight, true_iangle, true_gravity = pick_variables()

    list_height, list_distance, *_ = simulation(true_ivelocity, float(true_iheight) + 0.0001, true_iangle, true_gravity, drag["mass"], density["density"], drag["cd"], drag["area"])

    gametype = random.choice(["distance", "maxheight"])
    target = list_distance[-1] if gametype == "distance" else max(list_height)

    if gametype == "maxheight" and (max(list_height) - true_iheight) < 2.0:
        gametype = "distance"
        target = list_distance[-1]

    if target < 2.0:
        true_ivelocity, true_iheight, true_iangle, true_gravity = pick_variables()
        list_height, list_distance, *_ = simulation(true_ivelocity, true_iheight, true_iangle, true_gravity, drag["mass"], density["density"], drag["cd"], drag["area"])
        gametype = "distance"
        target = list_distance[-1]

    given_indep = {
        "ivelocity": true_ivelocity,
        "iheight": true_iheight,
        "iangle": true_iangle,
        "gravity": true_gravity
    }

    graph = create_graph(gametype, target)
    deviation = target * 0.02

    print(json.dumps({
        "graph": graph,
        "hidden_var": target_indep,
        "known_vars": given_indep,
        "target": target,
        "target_min": round(target - deviation, 3),
        "target_max": round(target + deviation, 3),
        "gametype": gametype,
        "aeropreset": drag_selected,
        "denpreset": density_selected,
        "mass": drag["mass"],
        "cd": drag["cd"],
        "area": drag["area"],
        "density": density["density"]
    }))

def run_game(body):
    target_indep = body["hidden_var"]
    attempt = float(body["attempt_value"])
    given_indep = body["known_vars"]
    target = body["target"]
    gametype = body["gametype"]
    drag = drag_presets[body["aeropreset"]]
    density = density_presets[body["denpreset"]]

    full_indep = dict(given_indep)
    full_indep[target_indep] = attempt

    list_height, list_distance, *_ = simulation(full_indep["ivelocity"], full_indep["iheight"], full_indep["iangle"], full_indep["gravity"], drag["mass"], density["density"], drag["cd"], drag["area"])

    result = list_distance[-1] if gametype == "distance" else max(list_height)
    deviation = abs((result - target) / target) * 100
    success = deviation <= 2.0
    graph = create_graph(gametype, target, list_height, list_distance)

    print(json.dumps({"graph": graph, "success": success, "deviation": deviation}))

data = json.loads(sys.stdin.read())

if data["mode"] == "setup":
    set_game(data)
elif data["mode"] == "run":
    run_game(data)
