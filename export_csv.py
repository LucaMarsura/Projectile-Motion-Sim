import csv
import sys
sys.path.append("backend")
from simulation import simulation

# Same presets as backend/main.py so results match the website
DRAG_PRESETS = {
    "baseball": {"mass": 0.145, "cd": 0.35, "area": 0.0042},
    "football": {"mass": 0.415, "cd": 0.06, "area": 0.0365},
    "ppball": {"mass": 0.0027, "cd": 0.445, "area": 0.00126},
    "soccerball": {"mass": 0.415, "cd": 0.25, "area": 0.0375},
    "tennisball": {"mass": 0.057, "cd": 0.6, "area": 0.0035},
    "paperplane": {"mass": 0.004, "cd": 0.005, "area": 0.002},
    "paperball": {"mass": 0.04, "cd": 0.55, "area": 0.0028},
    "golfball": {"mass": 0.046, "cd": 0.24, "area": 0.00143},
    "basketball": {"mass": 0.623, "cd": 0.47, "area": 0.0456},
    "bowlingball": {"mass": 7.0, "cd": 0.47, "area": 0.0366},
    "frisbee": {"mass": 0.175, "cd": 0.08, "area": 0.0707},
    "arrow": {"mass": 0.025, "cd": 0.004, "area": 0.00005},
    "spear": {"mass": 0.4, "cd": 0.04, "area": 0.00008},
    "shuttlecock": {"mass": 0.005, "cd": 0.60, "area": 0.0029},
}

DENSITY_PRESETS = {
    "air": 1.225,
    "vacuum": 0.0001,
    "water": 1000,
    "oil": 870,
    "highaltair": 0.4,
    "syrup": 1380,
    "moltenmetal": 6980,
}


def prompt(label, default):
    val = input(f"{label} [{default}]: ").strip()
    return float(val) if val else float(default)


def prompt_choice(label, options, default):
    names = ", ".join(list(options) + ["custom"])
    while True:
        val = input(f"{label} ({names}) [{default}]: ").strip().lower() or default
        if val in options or val == "custom":
            return val
        print(f"  Unknown option '{val}'.")


print("=== PMADS CSV Export ===")
ivelocity = prompt("Initial velocity (m/s)", 8.3)
iheight   = prompt("Initial height (m)", 1.6)
iangle    = prompt("Launch angle (deg)", 55)
gravity   = prompt("Gravity (m/s²)", 9.81)

drag_choice = prompt_choice("Drag preset", DRAG_PRESETS, "soccerball")
if drag_choice == "custom":
    mass = prompt("Mass (kg)", 0.415)
    cd   = prompt("Drag coefficient", 0.25)
    area = prompt("Cross-sectional area (m²)", 0.0375)
else:
    mass, cd, area = (DRAG_PRESETS[drag_choice][k] for k in ("mass", "cd", "area"))

density_choice = prompt_choice("Density preset", DENSITY_PRESETS, "air")
if density_choice == "custom":
    density = prompt("Fluid density (kg/m³)", 1.225)
else:
    density = DENSITY_PRESETS[density_choice]

output_file = input("Output filename [trajectory.csv]: ").strip() or "trajectory.csv"

list_height, list_distance, *_ = simulation(
    ivelocity, iheight + 0.0001, iangle, gravity, mass, density, cd, area
)

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["x_m", "y_m"])
    for d, h in zip(list_distance, list_height):
        writer.writerow([round(d, 4), round(h, 4)])

print(f"Saved {len(list_distance)} rows to {output_file}")
