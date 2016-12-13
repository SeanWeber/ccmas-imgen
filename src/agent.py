"""
.. py:module:: mas_memory
    :platform: Unix

An example of an agent's memory model and how an agent can learn (learn here is
used in a very weak sense) new artifacts to it from domain.
"""

from creamas.core import CreativeAgent, Environment, Simulation, Artifact

from model import *
from brush import *
from stroke import *


import logging
import random
import os

from PIL import Image

import matplotlib.image as im
import matplotlib.pyplot as pl

# Logging setup. This is simplified setup as all agents use the same logger.
# It _will_ cause some problems in asynchronous settings, especially if you
# are logging to a file.
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

#Debug
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
palette_gradient = []


class ListMemory:
    """Simple list memory which stores all seen artifacts as is into a list.
    """
    def __init__(self, capacity):
        """
        :param int capacity: The maximum number of artifacts in the memory.
        """
        self._capacity = capacity
        self._artifacts = []

    @property
    def capacity(self):
        """The maximum number of artifacts in the memory.
        """
        return self._capacity

    @property
    def artifacts(self):
        """The artifacts currently in the memory.
        """
        return self._artifacts

    def memorize(self, artifact):
        """Memorize an artifact into the memory.
        If the artifact is already in the memory, does nothing. If memory
        is full and a new artifact is memorized, forgets the oldest artifact.
        
        :param artifact: Artifact to be learned.
        :type artifact: :class:`~creamas.core.artifact.Artifact`
        """
        if artifact in self._artifacts:
            return

        self._artifacts.insert(0, artifact)
        if len(self._artifacts) > self.capacity:
            self._artifacts = self._artifacts[:self.capacity]


class FoolPainterAgent(CreativeAgent):
    """A sample agent implementation.
    Agent invents new strokes by combination of brushes patterns and palette of colours that it has learned
    from a given artwork or randomly otherwise.
    """

    def __init__(self, env, reference):
        """
        :param env:
            subclass of :py:class:`~creamas.core.environment.Environment`
        """

        super().__init__(env)

        self.mem = ListMemory(10)
        self.n = 3

        self.innovation_freq = random.randint(1, 10) # How many steps goes after palette and brushes is updated.

        self.color_palette_size  = 25
        self.color_reference     = create_model(reference)
        self.color_palette       = np.array(self.pick_colors(self.color_palette_size))

        self.min_brush_size = 3
        self.max_brush_size = 30

        self.brushes_set_size = 20
        self.brushes = [Brush(random.randint(self.min_brush_size, self.max_brush_size), reference) for i in range(self.brushes_set_size)]

        self.reference = reference

        # plt.imshow(self.color_palette, interpolation='None')
        # plt.imshow(self.brush.pattern, interpolation='None', cmap='gray')

        logger.debug("Agent started: {}".format(reference))

    def pick_colors (self, n):
        """Finds n most frequent colors from the color_palette.

        :param n: Number of colors to be picked.
        :returns:
            Array of the most frequent colors in the reference image.
        """
        return np.array([sorted(self.color_reference, key=self.color_reference.get)[:n]])

    def update_agent_sets (self, stroke=None):
        '''Include the brush and color of the stroke in the agents brushes and colors set.

        :param stroke: A stroke from which the new color and brush will be read.
        '''
        if (stroke):
            color = stroke.color
            brush = stroke.brush
        else:
            color = random.choice(list(self.color_reference.keys()))
            brush = Brush(random.randint(self.min_brush_size, self.max_brush_size), self.reference)

        # Replace a random color with the stroke's color
        self.color_palette[0][random.randrange(0,len(self.color_palette[0]))] = color

        # Replace a random brush with the stroke's brush
        self.brushes[random.randrange(0,len(self.brushes))] = brush


    def evaluate(self, artifact):
        """Evaluate given artifact with respect to the agent's  memory
        and how useful it if for the assigned job.

        :param artifact: :class:`~creamas.core.Artifact` to be evaluated.
        :returns:
            (evaluation, framing)-tuple, the framing is the combined framing of
            both the value and novelty.
        """

        surpris, surpris_framing = self.surprisingness(artifact)

        # This works as long as value and novelty evaluation is agent-non-dependent
        if artifact.value == None:
            value, value_framing = self.value(artifact)
            artifact.value, artifact.value_framing = value, value_framing
        else:
            value = artifact.value
            value_framing = artifact.value_framing

        # This works as long as value and novelty evaluation is agent-non-dependent
        if artifact.novelty == None:
            novelty, novelty_framing = self.novelty(artifact)
            artifact.novelty, artifact.novelty_framing = novelty, novelty_framing
        else:
            novelty = artifact.novelty
            novelty_framing = artifact.novelty_framing

        framing = {'value': value_framing, 'novelty':novelty_framing, 'suprisingness' : surpris_framing}
        evaluation = (value + novelty + surpris) / 3
        return evaluation, framing

    def value(self, artifact):
        """Compute the value of a given artifact with respect to the stroke the
        agent has in its vocabulary.

        :param artifact: :class:`~creamas.core.Artifact` to be evaluated.
        :returns:
            (evaluation, stroke)-tuple, containing both the evaluation and the
            stroke giving the maximum evaluation
        """

        str = artifact.obj
        pos = artifact.position

        result = self.env.prev_stroke(artifact.obj, pos)
        target = self.env._target_img[pos[0]:(pos[0] + len(str)), pos[1]:(pos[1] + len(str))]

        # plt.imshow(result, interpolation='None')
        # plt.show()
        # plt.imshow(target, interpolation='None')
        # plt.show()

        value = self.similarity(result, target)

        value, matching_stroke = value, "{:.4f}".format(value)

        # print(value)
        return value, matching_stroke

    def novelty(self, artifact):
        """Compute the novelty of a given artifact with respect to the artifacts
        in the agent's memory.

        :param artifact: :class:`~creamas.core.Artifact` to be evaluated
        :returns:
            (novelty, word)-tuple, containing both the novelty value and the
            word giving the minimum novelty.
        """
        
        str = artifact.obj
        pos = artifact.position

        # Computes a value that increases depending on the layer of strokes in that position
        overpaint = self.env._layers[pos[0]: pos[0] + len(str), pos[1]: pos[1] + len(str)].mean() + 1

        novelty = 1/overpaint

        novelty, matching_stroke = novelty, "{:.4f}".format(novelty)
        return novelty, matching_stroke

    def surprisingness(self, artifact):
        """Compute the surprisingness of a given artifact with respect to the artifacts
        in the agent's memory.

        :param artifact: :class:`~creamas.core.Artifact` to be evaluated
        :returns:
            (novelty, word)-tuple, containing both the surprisingness value and the
            stroke giving the minimum surprisingness.
        """

        accum_dif = 0

        if len(self.mem.artifacts) > 0:

            for mem_artifact in self.mem.artifacts:

                # Accumulate the similarity of the memory elements and the stroke.
                color_dif = np.absolute((artifact.color - mem_artifact.color)).mean()
                accum_dif += color_dif

        surpris = accum_dif / (len(self.mem.artifacts) + 1)

        surpris, matching_stroke = surpris, "{:.4f}".format(surpris)
        return surpris, matching_stroke


    def similarity(self, imgA, imgB):
        """Given two images of the same size, this function compute the similarity of the pixel
        values. The function compute the differences of RGB values of a pixel and weight it with
        the alpha value.

        :param imgA: Image to be compared.
        :param imgB: Image to be compared.
        :returns:
            Similarity of two images. 
        """
        #
        # print(imgA)
        # print(imgB)

        delta_R = imgA[:,:,0] - imgB[:,:,0]
        delta_G = imgA[:,:,1] - imgB[:,:,1]
        delta_B = imgA[:,:,2] - imgB[:,:,2]

        delta = (np.absolute(delta_R) + np.absolute(delta_G) + np.absolute(delta_B)) / 3

        return (1 - np.mean(delta))

    def generate(self):
        """Generate a new stroke.

        Stroke are generated mixing data memorized of patterns and colors.

        :returns: a stroke wrapped as :class:`~creamas.core.artifact.Artifact`
        """
        random_color = random.choice(self.color_palette[0])
        brush = random.choice(self.brushes)

        stroke = []
        for row_idx in range(len(brush.pattern)):
            stroke_line = []
            for col_idx in range(len(brush.pattern[row_idx])):
                stroke_line.append(np.insert(random_color, 3, brush.pattern[row_idx][col_idx]))
            stroke.append(stroke_line)
        stroke = np.array(stroke)

        strokeArt = StrokeArtifact(self, stroke)

        canvas_max_x = self.env._canvas.shape[0] - len(stroke)
        canvas_max_y = self.env._canvas.shape[1] - len(stroke)

        random_position = [random.randint(0, canvas_max_x), random.randint(0, canvas_max_y)]

        strokeArt.add_position(random_position)
        strokeArt.add_color(random_color)
        strokeArt.add_brush(brush)

        # # Dbg
        # plt.imshow(stroke, interpolation='None')
        # plt.show()

        return strokeArt

    def invent(self, n=20):
        """Invent a new stroke.

        Generates multiple (n) strokes and selects the one with the highest
        evaluation.

        :param int n: Number of strokes to consider
        :returns:
            a stroke wrapped as :class:`~creamas.core.artifact.Artifact` and its
            evaluation.
        """
        best_artifact = self.generate()
        max_evaluation, framing = self.evaluate(best_artifact)
        for _ in range(n-1):
            artifact = self.generate()
            evaluation, fr = self.evaluate(artifact)
            if evaluation > max_evaluation:
                best_artifact = artifact
                max_evaluation = evaluation
                framing = fr
        logger.debug("{} invented stroke: {} (eval={}, framing={})"
                     .format(self.name, max_evaluation, "-",
                             framing))

        # Add evaluation and framing to the artifact.
        best_artifact.add_eval(self, max_evaluation, fr=framing)
        return best_artifact

    def render_palette(self):
        '''Auxiliar function for debugging the content of the agents palette.
        '''
        global palette_gradient

        integer_canvas = np.uint8(self.color_palette * 255)

        # Debug - Shows palette of agent 0.
        if (self.name[-1] == '0'):
            palette_gradient.append(self.color_palette[0].copy())
            plt.imshow(palette_gradient, animated=True, interpolation='None', hold=False)
            # plt.draw()
            # plt.pause(0.001)

            render_factor = 200

            if (self.env.age % render_factor == 0):
                plt.savefig(PROJECT_ROOT + '/output/palettes/palette_ag' + self.name[-1] + '_steps_' + str(self.env.age - render_factor) + '_'+ str(self.env.age) + '.png')
                palette_gradient = []

    async def act(self):
        """Agent acts by inventing new strokes.
        """

        # Update last votation winner brushes and palette with the winning stroke information.
        if (len(self.env.artifacts) > 0):
            if (self.env.artifacts[-1].creator == self.name):
                self.update_agent_sets(self.env.artifacts[-1])

        # After 'innovation_freq' steps, the agent learns a new color and brush.
        if (self.env.age % self.innovation_freq == 0):
            self.update_agent_sets()

        artifact = self.invent(self.n)

        # Memorize the last generated stroke
        self.mem.memorize(artifact)
        # logger.debug([a.obj for a in self.mem.artifacts])
        self.env.add_candidate(artifact)

        # Debug - Disable next line to not render palette images (output/palettes files)
        self.render_palette();


if __name__ == "__main__":
    env = Environment.create(('localhost', 5555))
    agent = FoolPainterAgent(env, reference="../media/starring-night.jpg")
    agent.generate()


