import matplotlib.pyplot as plt
import numpy as np
from simulation.py import simul

def graph_energy(list_time,list_velocity,list_height,true_mass,true_gravity):
    #defining composite variable
    i = 0
    ekinetic = 1/2 * true_mass * list_velocity[0] ** 2
    list_ekinetic = [ekinetic]
    epotential = true_mass * true_gravity * list_height[i]
    list_epotential = [epotential]
    while i <= len(list_time):
        ekinetic = 1/2 *true_mass * list_velocity[i] ** 2
        list_ekinetic.append(ekinetic)
        epotential = true_mass * true_gravity * list_height[i]
        list_epotential.append(epotential)
    
    x = list_time
    y = list_ekinetic
    ax.twinx = list_epotential

    plt.show()