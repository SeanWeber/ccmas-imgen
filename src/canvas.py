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

        pl.imshow(img, interpolation='None')
        pl.show()

        return

    def add_stroke(self, stroke, position):
        x_offset = position[0]
        y_offset = position[1]
        for x in range(len(stroke)):
            for y in range(len(stroke[x])):
                self.paint_over(x + x_offset, y + y_offset, stroke[x][y])
                
    def prev_stroke(self, stroke, position):
        x_off = position[0]
        y_off = position[1]

        tmp_canvas = np.copy(self._canvas)

        for x in range(len(stroke)):
            for y in range(len(stroke[x])):
                tmp_canvas[x + x_off][y + y_off] = self.paint_over(x + x_off, y + y_off, stroke[x][y], tmp_canvas)

        pl.imshow(tmp_canvas, interpolation='None')
        pl.show()

        return tmp_canvas[x_off:(x_off + len(stroke)), y_off:(y_off + len(stroke[0]))]

    def paint_over(self, x, y, stroke, canvas=None):
        RED   = 0
        GRN   = 1
        BLU   = 2
        ALPHA = 3

        if canvas == None:
            canvas = self._canvas

        canvas[x][y][RED] = stroke[RED] * stroke[ALPHA] + (1 - stroke[ALPHA]) * canvas[x][y][RED]
        canvas[x][y][GRN] = stroke[GRN] * stroke[ALPHA] + (1 - stroke[ALPHA]) * canvas[x][y][GRN]
        canvas[x][y][BLU] = stroke[BLU] * stroke[ALPHA] + (1 - stroke[ALPHA]) * canvas[x][y][BLU]

        # Sanity check
        canvas[x][y][RED] = min(canvas[x][y][RED], 1.0)
        canvas[x][y][GRN] = min(canvas[x][y][GRN], 1.0)
        canvas[x][y][BLU] = min(canvas[x][y][BLU], 1.0)

        canvas[x][y][RED] = max(canvas[x][y][RED], 0.0)
        canvas[x][y][GRN] = max(canvas[x][y][GRN], 0.0)
        canvas[x][y][BLU] = max(canvas[x][y][BLU], 0.0)

        return canvas[x][y]

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
