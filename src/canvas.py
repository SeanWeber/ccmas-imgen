from creamas.core import Environment
import numpy as np
import matplotlib.pyplot as pl

class CanvasEnvironment(Environment):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._canvas = []

    @property
    def canvas(self):
        return self._canvas

    def init_canvas(self, shape):
        '''
        :param tuple shape: Same shape as the target (height, width, RGB/RGBA)
        :returs: A white canvas
        '''
        self._canvas = np.empty(shape)
        self._canvas.fill(1.0)

        # Changing opacity to 1
        if shape[2] == 4:
            self._canvas.T[3].fill(1.0)
        return self._canvas

    def viewCanvas(self):
        pl.imshow(self._canvas)
        pl.show()
        return

    def add_stroke(self, stroke, position):
        x_offset = position[0]
        y_offset = position[1]

        for x in range(len(stroke)):
            for y in range(len(stroke[x])):
                self._canvas[x + x_offset][y + y_offset] = stroke[x][y]

# Example usage
if __name__ == "__main__":
    env = CanvasEnvironment.create(("localhost", 5555))
    # initializes a white canvas with size 512x512
    env.init_canvas((512,512,4))
    print(env._canvas)
    env.viewCanvas()

