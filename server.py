from flask import Flask, request, jsonify, send_from_directory
import subprocess, json, os, sys, random, math, base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

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

def pick_parameters():
    true_iheight = round(random.uniform(0, 20), 1)
    true_gravity = 9.81 if random.random() < 0.80 else round(random.uniform(1, 20), 2)
    if true_iheight > 0:
        true_iangle = round(random.uniform(-90, 90), 0)
    else:
        true_iangle = round(random.uniform(0, 90), 0)
    true_ivelocity = round(random.uniform(5, 40), 1)
    return true_ivelocity, true_iheight, true_iangle, true_gravity

def run_sim(ivelocity, iheight, iangle, gravity, mass, density, cd, area):
    sim_input = json.dumps({
        "ivelocity": str(ivelocity),
        "iheight":   str(float(iheight) + 0.0001),
        "iangle":    str(iangle),
        "gravity":   str(gravity),
        "mass":      str(mass),
        "cd":        str(cd),
        "area":      str(area),
        "density":   str(density)
    })
    result = subprocess.run(
        [sys.executable, "backend/game_sim.py"],
        input = sim_input,
        capture_output = True, text = True
    )
    return json.loads(result.stdout)

def build_graph(gametype, target, list_height = None, list_distance = None):
    fig, ax = plt.subplots(figsize = (6, 4))
    deviation = target * 0.01
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

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("frontend", path)

@app.route("/run", methods = ["POST"])
def run():
    data = request.get_json()
    result = subprocess.run(
        [sys.executable, "backend/main.py"],
        input = json.dumps(data),
        capture_output = True, text = True
    )
    print("STDOUT:", repr(result.stdout))
    print("STDERR:", repr(result.stderr))
    if not result.stdout.strip():
        return jsonify({"error": result.stderr or "No output", "prints": [], "graph1": "", "graph2": ""})
    return jsonify(json.loads(result.stdout))

@app.route("/game_setup", methods = ["POST"])
def game_setup():
    body = request.get_json()
    previous_attempt = body.get("previous_attempt", None)
    previous_state   = body.get("previous_state", None)
    if previous_state:
        aero_chosen   = previous_state["aeropreset"]
        den_chosen    = previous_state["denpreset"]
        indep_unknown = previous_state["indep_unknown"]
    else:
        aero_chosen   = pick_aero()
        den_chosen    = pick_den()
        indep_unknown = random.choice(["ivelocity", "iheight", "iangle", "gravity"])
    aero = AERO_PRESETS[aero_chosen]
    den  = DEN_PRESETS[den_chosen]
    true_ivelocity, true_iheight, true_iangle, true_gravity = pick_parameters()
    sim = run_sim(
        true_ivelocity, true_iheight, true_iangle, true_gravity,
        aero["mass"], den["density"], aero["cd"], aero["area"]
    )
    gametype = random.choice(["distance", "maxheight"])
    target   = sim["distance"] if gametype == "distance" else sim["maxheight"]
    indep_given = {
        "ivelocity": true_ivelocity,
        "iheight":   true_iheight,
        "iangle":    true_iangle,
        "gravity":   true_gravity
    }
    graph = build_graph(gametype, target)
    deviation = target * 0.02
    return jsonify({
        "graph":      graph,
        "indep_unknown": indep_unknown,
        "indep_given": indep_given,
        "target":     target,
        "target_min": round(target - deviation, 3),
        "target_max": round(target + deviation, 3),
        "gametype":   gametype,
        "aeropreset": aero_chosen,
        "denpreset":  den_chosen,
        "mass":       aero["mass"],
        "cd":         aero["cd"],
        "area":       aero["area"],
        "density":    den["density"]
    })

@app.route("/game_run", methods = ["POST"])
def game_run():
    body       = request.get_json()
    indep_unknown = body["indep_unknown"]
    attempt    = float(body["attempt_value"])
    indep_given = body["indep_given"]
    target     = body["target"]
    gametype   = body["gametype"]
    aero       = AERO_PRESETS[body["aeropreset"]]
    den        = DEN_PRESETS[body["denpreset"]]
    vars_full  = dict(indep_given)
    vars_full[indep_unknown] = attempt
    sim = run_sim(
        vars_full["ivelocity"], vars_full["iheight"],
        vars_full["iangle"],    vars_full["gravity"],
        aero["mass"], den["density"], aero["cd"], aero["area"]
    )
    result    = sim["distance"] if gametype == "distance" else sim["maxheight"]
    deviation = abs((result - target) / target) * 100
    success   = deviation <= 2.0
    graph = build_graph(
        gametype, target,
        sim["list_height"], sim["list_distance"]
    )
    return jsonify({
        "graph":     graph,
        "success":   success,
        "deviation": deviation
    })

if __name__ == "__main__":
    app.run(debug = True)