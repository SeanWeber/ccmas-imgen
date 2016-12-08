import agent
import canvas
import os
import random

from creamas.core import Simulation

if __name__ == "__main__":
    # initializes a white canvas
    env = canvas.CanvasEnvironment.create(("localhost", 5555))
    env.init_canvas((64, 64, 4))

    # Initialize the agents
    for i in range(3):
        reference_image = "../inspiration/" + random.choice(os.listdir("../inspiration/"))
        fool = agent.FoolPainterAgent(env, reference=reference_image)

    # Run the simulation
    sim = Simulation(env, log_folder='./logs', callback=env.vote)
    sim.async_steps(5)
    sim.end()

    # View the canvas
    env.view_canvas()
