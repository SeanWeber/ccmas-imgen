from creamas.core import Artifact

class StrokeArtifact(Artifact):
    '''Extended version of the `~creamas.core.artifact.Artifact`'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = []

    @property
    def position(self):
        '''Position of the `~src.stroke.StrokeArtifact` on the `~src.canvas.CanvasEnvironment`.'''
        return self._position

    def add_position(self, position):
        '''Add position information for the `~src.stroke.StrokeArtifact`

        :param list position: xy-coordinates of the position.
        '''
        self._position = position

