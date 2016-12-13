import agent
import canvas
import numpy as np
import random
import os
import sys
import getopt

import matplotlib.pyplot as pl

from creamas.core import Simulation

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if __name__ == "__main__":
    np.set_printoptions(threshold=np.nan)

    # Selects default settings
    target_image = PROJECT_ROOT + "/target/eye.jpg"
    inspiration_folder = PROJECT_ROOT + "/media/"
    output_folder = PROJECT_ROOT + "/output/result.png"
    port = 5555
    agents = 3
    steps = 10

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["target=", "inspire=", "output=", "port=", "agents=", "steps="])
    except getopt.GetoptError:
        print("Error: Bad arguments")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--target':
            target_image = arg
        elif opt == '--inspire':
            inspiration_folder = arg
        elif opt == '--output':
            output_folder = arg
        elif opt == '--port':
            port = int(arg)
        elif opt == '--agents':
            agents = int(arg)
        elif opt == '--steps':
            steps = int(arg)

    # initializes a canvas
    env = canvas.CanvasEnvironment.create(("localhost", port))
    env.init_canvas(target=target_image)

    # Initialize the agents
    for i in range(agents):
        reference_image = inspiration_folder + random.choice(os.listdir(inspiration_folder))
        fool = agent.FoolPainterAgent(env, reference=reference_image)

    # Run the simulation
    sim = Simulation(env, log_folder='./logs', callback=env.vote)
    sim.async_steps(steps)
    sim.end()

    # View the canvas
    env.view_canvas(output_folder)

    str = fool.generate()
