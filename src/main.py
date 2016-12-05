import agent
import canvas
import numpy as np

if __name__ == "__main__":
    # initializes a white canvas with size 512x512
    env = canvas.CanvasEnvironment.create(("localhost", 5555))
    env.init_canvas((64, 64, 4))

    # Initialize the agents
    fool_agent = agent.FoolPainterAgent(env, reference="../media/starring-night.jpg")

    # Run the agents
    artifact = fool_agent.generate()

    position = [20, 50]
    env.add_stroke(artifact._obj, position)

    # View the canvas
    print(env._canvas)
    env.viewCanvas()