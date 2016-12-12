import agent
import canvas
import numpy as np
import random
import os

import matplotlib.pyplot as pl

from creamas.core import Simulation

if __name__ == "__main__":

    np.set_printoptions(threshold=np.nan)

    # Selects target image.
    target_image = "../media/mona_lisa.jpg"

    # initializes a white canvas
    env = canvas.CanvasEnvironment.create(("localhost", 5555))
    env.init_canvas(target=target_image)

    # Initialize the agents
    for i in range(3):
        reference_image = "../media/starring-night.jpg"
        # reference_image = "../low_inspiration/" + random.choice(os.listdir("../low_inspiration/"))
        fool = agent.FoolPainterAgent(env, reference=reference_image)

    # Run the simulation
    sim = Simulation(env, log_folder='./logs', callback=env.vote)
    sim.async_steps(10000)
    sim.end()

    # View the canvas
    env.view_canvas()

    str = fool.generate()

    pl.imshow(env._layers, interpolation='None')
    pl.show()
