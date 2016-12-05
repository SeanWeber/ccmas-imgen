import agent
import canvas
import os
import random

if __name__ == "__main__":
    # initializes a white canvas
    env = canvas.CanvasEnvironment.create(("localhost", 5555))
    env.init_canvas((64, 64, 4))

    # Initialize the agents
    for i in range(5):
        reference_image = "../media/" + random.choice(os.listdir("../media/"))
        fool = agent.FoolPainterAgent(env, reference=reference_image)

        # Run the agents
        artifact = fool.generate()

        # TODO move this to the agent class
        position = [random.randint(0, 59), random.randint(0, 59)]
        env.add_stroke(artifact._obj, position)

    # View the canvas
    env.viewCanvas()
