import sys, json, math
sys.path.append("backend")
from simulation import simulation

data = json.loads(sys.stdin.read())
true_ivelocity = float(data["ivelocity"])
true_iheight   = float(data["iheight"])
true_iangle    = float(data["iangle"])
true_gravity   = float(data["gravity"])
true_mass      = float(data["mass"])
true_cd        = float(data["cd"])
true_area      = float(data["area"])
true_density   = float(data["density"])
list_height, list_distance, list_time, list_velocity, list_angle = simulation(
    true_ivelocity, true_iheight, true_iangle, true_gravity,
    true_mass, true_density, true_cd, true_area
)
print(json.dumps({
    "distance":      list_distance[-1],
    "maxheight":     max(list_height),
    "list_distance": list_distance,
    "list_height":   list_height
}))