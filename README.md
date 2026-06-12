# PMADS - Projectile Motion and Drag Simulator

PMADS is a web application modelling projectile motion under various aerodynamic conditions. Twelve variables can be tweaked through user-controlled sliders to view custom trajectories,

## What it does

**Simulation** Four Launch Parameters, initial velocity, height, angle, and gravity, can be controlled to set a custom trajectory. The engine integrates forces at 1000 Hz and outputs trajectory data, as well as a three-point energy analysis. The iterative properties of the simulator allow a launch parameter to be inferred under certain conditions when a dependent value (distance, maximum height, time, and final velocity) is given by the user.

**Game** A challenge is randomly generated with three parameters locked and one hidden. A target zone is shown on the graph. The variable slider can be adjusted to aim change trajectory towards the target. Once the trajectory reaches the target zone within ±2%, the challenge is completed.

## Structure

server.py
requirements.txt
backend/
    simulation.py: Force Integration
    solver.py: Iterative solver
    energyanalysis.py: Energy Analysis
    trajectorygraphing.py: Trajectory graph creation and export
    main.py: Simulation request handler
    game.py: Challenge generation and regeneration
frontend/
    sim.html: Simulation interface
    game.html: Game interface
    index.html: Home
    gameindex.html: Game home page
    learn.html: Physics theory
    features.html: Feature list
    nav.css / stylesim.css / stylegame.css / ...: Various design files
    images/: Images within website

## Physics

Drag force at each 1 ms timestep:

Fd = 1/2 p A Cd v^2

Because drag force is dependent on instantaneous velocity, it must be calculated at a frequent rate to accurately model projectile motion.
