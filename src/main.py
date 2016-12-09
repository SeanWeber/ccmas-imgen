import agent
import canvas
import os
import random

from creamas.core import Simulation

if __name__ == "__main__":

    # Selects target image.
    target_image = "../target/mona_lisa.jpg"

    # initializes a white canvas
    env = canvas.CanvasEnvironment.create(("localhost", 5555))
    env.init_canvas(target=target_image)

    # Initialize the agents
    for i in range(20):
        reference_image = "../media/" + random.choice(os.listdir("../media/"))
        fool = agent.FoolPainterAgent(env, reference=reference_image)

    # Run the simulation
    sim = Simulation(env, log_folder='./logs', callback=env.vote)
    sim.async_steps(100)
    sim.end()

    # View the canvas
    env.view_canvas()
