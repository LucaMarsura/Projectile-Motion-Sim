import matplotlib.pyplot as plt
import numpy as np
from simulation.py import simul

def graph_trajectory(list_distance,list_height):
    x = list_distance
    y = list_height

    plt.xlabel("Distance")
    plt.ylabel("Height")

    plt.show

    plt.xlabel("Time")
    plt.ylabel("Energy")
    plt.grid(True)

    plt.show()


    
