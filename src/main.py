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

    # Selects target image.
    target_image = PROJECT_ROOT + "/media/mona_lisa.jpg"
    inspiration_folder = PROJECT_ROOT + "/media/"
    output_folder = PROJECT_ROOT + "/output/result.png"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["target=", "inspire=", "output="])
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

    # initializes a canvas
    env = canvas.CanvasEnvironment.create(("localhost", 5555))
    env.init_canvas(target=target_image)

    # Initialize the agents
    for i in range(3):
        reference_image = inspiration_folder + random.choice(os.listdir(inspiration_folder))
        fool = agent.FoolPainterAgent(env, reference=reference_image)

    # Run the simulation
    sim = Simulation(env, log_folder='./logs', callback=env.vote)
    sim.async_steps(10)
    sim.end()

    # View the canvas
    env.view_canvas(output_folder)

    str = fool.generate()

    # Final previews

    #pl.imshow(env._canvas, interpolation='None')
    #pl.show()

    #pl.imshow(env._layers, interpolation='None')
    #pl.show()
