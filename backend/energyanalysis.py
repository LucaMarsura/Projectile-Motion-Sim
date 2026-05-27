import matplotlib.pyplot as plt
import base64
from io import BytesIO

def energy(list_time, list_distance, list_height, list_velocity, true_mass, result_gravity):
    list_ekinetic = []
    list_epotential = []
    list_etotal = []
    for i in range(len(list_time)):
        ekinetic = 1 / 2 * true_mass * list_velocity[i] ** 2
        epotential = true_mass * result_gravity * list_height[i]
        etotal = ekinetic + epotential
        list_ekinetic.append(ekinetic)
        list_epotential.append(epotential)
        list_etotal.append(etotal)
    peak_index = list_height.index(max(list_height))
    result_ikinetic = list_ekinetic[0]
    result_ipotential = list_epotential[0]
    result_itotal = list_etotal[0]
    result_ftotal = list_ekinetic[-1]
    result_pkinetic = list_ekinetic[peak_index]
    result_ppotential = list_epotential[peak_index]
    result_ptotal = result_pkinetic + result_ppotential
    plt.plot(list_time, list_ekinetic, label = "Kinetic Energy")
    plt.plot(list_time, list_epotential, label = "Potential Energy")
    plt.plot(list_time, list_etotal, label = "Total Energy")
    plt.title("Energy vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Energy (J)")
    plt.legend()
    buf = BytesIO()
    plt.savefig(buf, format = "png")
    buf.seek(0)
    graph_energy = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    txt_result = [
        "Energy Analysis:",
        f"Initial Total Energy: {round(result_itotal, 3)} Joules",
        f"(Kinetic Energy: {round(result_ikinetic, 3)} J / Gravitational Potential Energy: {round(result_ipotential, 3)} J)",
        "Total Energy Dissipated: 0 Joules",
        f"Total Energy at Peak Height: {round(result_ptotal, 3)} Joules",
        f"(Kinetic Energy: {round(result_pkinetic, 3)} J / Gravitational Potential Energy: {round(result_ppotential, 3)} J)",
        f"Total Energy Dissipated: {round(-(result_ptotal - result_itotal), 3)} Joules",
        f"Final Total Energy: {round(result_ftotal, 3)} Joules",
        f"(Kinetic Energy: {round(result_ftotal, 3)} J / Gravitational Potential Energy: 0 J)",
        f"Total Energy Dissipated: {round(-(result_ftotal - result_itotal), 3)} Joules"
    ]
    return txt_result, graph_energy