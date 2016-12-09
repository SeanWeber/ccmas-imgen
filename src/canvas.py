from creamas.core import Environment
from PIL import Image
import numpy as np

import matplotlib.image as mpimg
import matplotlib.pyplot as pl

import random
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class CanvasEnvironment(Environment):
    '''Extended version of the `~creamas.core.environment.Environment`'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._canvas = []
        self._layers = []
        self._target_img = None

    @property
    def canvas(self):
        '''Array representation of the image that will be created by agents.'''
        return self._canvas

    @property
    def layers(self):
        '''Array containing knowledge of layers over each pixel in canvas.'''
        return self._layers

    def init_canvas(self, target=None, shape=None):
        """Funtion that initializes `~src.canvas.CanvasEnvironment`
        with approriate attribute values. This function should be run
        after create().

        :param tuple shape: Same shape as the target (height, width,
        :RGB/RGBA) returs: A white canvas
        """
        if target:
            img = mpimg.imread(target)

            # Normalization of data to decimal (0.0 - 1.0) representation
            img = img.astype('float16')
            if img.max() > 1.0:
                img /= 255.0

            self._target_img = img
            self._canvas = np.empty(img.shape)

        else:
            self._canvas = np.empty(shape)
            self._canvas.fill(1.0)

        # Counts each time each pixel in the canvas has been drawn over
        self._layers = np.zeros(shape[:2])
        return self._canvas

    def view_canvas(self):

        img = Image.fromarray(self._canvas, 'RGBA')
        img.save('../output/result.png')

        pl.imshow(self._canvas, interpolation='None')
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

            self.add_stroke(stroke=accepted.obj, position=accepted.position)

            # pl.imshow(self._canvas, interpolation='None')
            # pl.show()

            logger.info("Vote winner by {}: {} (val={})"
                        .format(accepted.creator, "-", value))
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
