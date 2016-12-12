import agent
import canvas
import numpy as np
import random
import os

import matplotlib.pyplot as pl

from creamas.core import Simulation

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if __name__ == "__main__":

    np.set_printoptions(threshold=np.nan)

    # Selects target image.
    target_image = PROJECT_ROOT + "/media/mona_lisa.jpg"

    # initializes a white canvas
    env = canvas.CanvasEnvironment.create(("localhost", 5555))
    env.init_canvas(target=target_image)

    # Initialize the agents
    for i in range(3):
        reference_image = PROJECT_ROOT + "/media/starring-night.jpg"
        # reference_image = "../low_inspiration/" + random.choice(os.listdir("../low_inspiration/"))
        fool = agent.FoolPainterAgent(env, reference=reference_image)

    # Run the simulation
    sim = Simulation(env, log_folder='./logs', callback=env.vote)
    sim.async_steps(10000)
    sim.end()

    # View the canvas
    env.view_canvas()

    str = fool.generate()

    # Final previews

    pl.imshow(env._canvas, interpolation='None')
    pl.show()

    pl.imshow(env._layers, interpolation='None')
    pl.show()
