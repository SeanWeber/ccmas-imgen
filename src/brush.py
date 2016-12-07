import matplotlib.image as mpimg

from scipy import ndimage, misc

import numpy as np
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


class Brush:
    """A brush used by agent to paint a picture.
    """

    def __init__(self, size=5, reference=None):
        """
        :param int size: Size of a brush in pixels.
        :param string pattern: Shape of a brush.
        """
        self._size 	= size
        self._reference = reference

        self.pattern = self.generate_pattern(self._reference, self._size)

    def generate_pattern(self, reference, size):
        # Import image from reference and convert it to grayscale.
        img = mpimg.imread(reference)
        gray = np.mean(img, -1)

        # Normalization of data to decimal (0.0 - 1.0) representation
        if gray.max() > 1.0:
            gray /= 255.0

        # Extract a random slice with the pixel size given as parameter
        slice_center_x = random.randint(0, len(img[0]) - size - 1)
        slice_center_y = random.randint(0, len(img) - size - 1)

        slice = gray[slice_center_y: slice_center_y + size, slice_center_x: slice_center_x + size]

        # Detects border to generate the pattern of the brush
        dx = ndimage.sobel(slice, 0)  # horizontal derivative
        dy = ndimage.sobel(slice, 1)  # vertical derivative
        pattern = np.hypot(dx, dy)    # grayscale slice with border detection

        return pattern


# Test
if __name__ == "__main__":
    brush = Brush(20, "../media/starring-night.jpg")