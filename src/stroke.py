from creamas.core import Artifact
import numpy as np

class StrokeArtifact(Artifact):
    '''Extended version of the `~creamas.core.artifact.Artifact`'''

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._position = []
        self._color = []
        self._brush = []

        # This works as long as value and novelty evaluation is agent-non-dependent
        self.value = None
        self.value_framing = None
        self.novelty = None
        self.novelty_framing = None

    @property
    def position(self):
        '''Position of the :any:`stroke.StrokeArtifact` on the :any:`canvas.CanvasEnvironment`.'''
        return self._position

    @property
    def color(self):
        '''Position of the :any:`stroke.StrokeArtifact` on the :any:`canvas.CanvasEnvironment`.'''
        return self._color

    @property
    def brush(self):
        '''Position of the :any:`stroke.StrokeArtifact` on the :any:`canvas.CanvasEnvironment`.'''
        return self._brush

    def add_position(self, position):
        '''Add position information for the :any:`stroke.StrokeArtifact`

        :param list position: xy-coordinates of the position.
        '''
        self._position = position

    def add_color(self, color):
        '''Add color information for the :any:`stroke.StrokeArtifact`

        :param list color: xy-coordinates of the color.
        '''
        self._color = color

    def add_brush(self, brush):
        '''Add brush information for the :any:`stroke.StrokeArtifact`

        :param list brush: xy-coordinates of the brush.
        '''
        self._brush = brush

