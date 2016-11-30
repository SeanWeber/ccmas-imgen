class Brush():
	'''A brush used by agent to paint a picture.
	'''

	def __init__(self, radius = 5, shape = 'CIRCLE'):
		'''
		:param int radius: Size of a brush in pixels.
		:param string shape: Shape of a brush. Only supported value so far is 'CIRCLE'.
		'''
		self._radius = radius
		self._shape = shape

	@property
	def radius(self):
		return self._radius

	@property
	def shape(self):
	    return self._shape


# Test
if __name__ == "__main__":
	brush = Brush(radius = 12)
	print(str(brush.radius))
	print(str(brush.shape))