from creamas.core import Environment
import numpy as np
import matplotlib.pyplot as pl

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class CanvasEnvironment(Environment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._canvas = []

    @property
    def canvas(self):
        return self._canvas

    def init_canvas(self, shape):
        """
        :param tuple shape: Same shape as the target (height, width,
        :RGB/RGBA) returs: A white canvas
        """
        self._canvas = np.empty(shape)
        self._canvas.fill(1.0)
        return self._canvas

    def view_canvas(self):
        pl.imshow(self._canvas)
        pl.show()
        return

    def add_stroke(self, stroke, position):
        x_offset = position[0]
        y_offset = position[1]
        for x in range(len(stroke)):
            for y in range(len(stroke[x])):
                self._canvas[x + x_offset][y + y_offset] = stroke[x][y]

    def vote(self, age):
        artifacts = self.perform_voting(method='mean')
        if len(artifacts) > 0:
            accepted = artifacts[0][0]
            value = artifacts[0][1]
            self.add_artifact(accepted)

            # center point of canvas, change this once stroke has knowledge of position
            i = round(self._canvas.shape[0]/2)
            self.add_stroke(stroke=accepted.obj, position=(i, i))

            logger.info("Vote winner by {}: {} (val={})"
                        .format(accepted.creator, accepted.obj, value))
        else:
            logger.info("No vote winner!")
        self.clear_candidates()

# Example usage
if __name__ == "__main__":
    env = CanvasEnvironment.create(("localhost", 5555))
    # initializes a white canvas with size 512x512
    env.init_canvas((512, 512, 4))
    print(env._canvas)
    env.view_canvas()
