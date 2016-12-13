import matplotlib.image as mpimg

from scipy import ndimage, misc

import numpy as np
import random


def rgb2gray(rgb):
    """Maps RGB value to grayscale.

    :param list rgb: A definiton of RGB color.
    :returns: A luminance in grayscale.
    """
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

        self._pattern = self.generate_pattern(self._reference, self._size)

    @property
    def pattern(self):
        """A pattern the brush produces.
        """
        return self._pattern

    def generate_pattern(self, reference, size):
        """Extracts a pattern from the reference image.

        Firstly, the image is transformed to grayscale. A random square from image
        is picked. A pattern is extracted using the edge detection (Sobel's filter).

        :param reference: Reference image.
        :param int size: Size of a pattern (length of its edge).
        :returns:
            A pattern extracted from the image.
        """
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

        # # Detects border to generate the pattern of the brush
        dx = ndimage.sobel(slice, 0)  # horizontal derivative
        dy = ndimage.sobel(slice, 1)  # vertical derivative
        pattern = np.hypot(dx, dy)    # grayscale slice with border detection

        # Normalize pattern
        if pattern.max() > 1.0:
            return pattern / pattern.max()

        return pattern



    # Test
if __name__ == "__main__":
    brush = Brush(20, "../media/starring-night.jpg")