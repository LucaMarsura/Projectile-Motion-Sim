import matplotlib.pyplot as plt
import base64
from io import BytesIO


def graph_trajectory(list_distance, list_height):

    fig, ax = plt.subplots()

    ax.plot(list_distance, list_height)
    ax.set_title("Projectile Trajectory")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    graph = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return graph
