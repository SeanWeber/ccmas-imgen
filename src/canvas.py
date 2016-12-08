from creamas.core import Environment
from PIL import Image
import numpy as np
import matplotlib.pyplot as pl
import random
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
        integer_canvas = np.uint8(self._canvas*255)

        img = Image.fromarray(integer_canvas, 'RGBA')
        img.save('../output/result.png')

        return

    def add_stroke(self, stroke, position):
        x_offset = position[0]
        y_offset = position[1]
        for x in range(len(stroke)):
            for y in range(len(stroke[x])):
                self.paint_over(x + x_offset, y + y_offset, stroke[x][y])

    def paint_over(self, x, y, stroke):
        RED = 0
        GREEN = 1
        BLUE = 2
        ALPHA = 3

        self._canvas[x][y][RED]   += stroke[RED] * stroke[ALPHA]
        self._canvas[x][y][GREEN] += stroke[GREEN] * stroke[ALPHA]
        self._canvas[x][y][BLUE]  += stroke[BLUE] * stroke[ALPHA]

        self._canvas[x][y][RED]   = max(self._canvas[x][y][RED], 1.0)
        self._canvas[x][y][GREEN] = max(self._canvas[x][y][GREEN], 1.0)
        self._canvas[x][y][BLUE]  = max(self._canvas[x][y][BLUE], 1.0)

    def vote(self, age):
        artifacts = self.perform_voting(method='mean')
        if len(artifacts) > 0:
            accepted = artifacts[0][0]
            value = artifacts[0][1]
            self.add_artifact(accepted)

            # TODO random point of canvas, change this once stroke has knowledge of position
            max_brush_size = 5
            canvas_max = self._canvas.shape[0] - max_brush_size
            random_position = [random.randint(0, canvas_max), random.randint(0, canvas_max)]
            self.add_stroke(stroke=accepted.obj, position=random_position)

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
