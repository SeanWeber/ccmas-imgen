"""
.. py:module:: mas_memory
    :platform: Unix
An example of an agent's memory model and how an agent can learn (learn here is
used in a very weak sense) new artifacts to it from domain.
"""

from creamas.core import CreativeAgent, Environment, Simulation, Artifact

from model import *
from brush import *

import logging
import random

import matplotlib.image as im
import matplotlib.pyplot as pl

# Logging setup. This is simplified setup as all agents use the same logger.
# It _will_ cause some problems in asynchronous settings, especially if you
# are logging to a file.
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


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

        self.mem = ListMemory(20)
        self.n = 1

        self.color_reference     = create_model(reference)
        self.color_palette_size  = 30
        self.color_palette       = np.array(self.pick_colors(self.color_palette_size))

        self.brush_size          = random.randint(3,5) # Grid of NxN ; N = random value from 3 to 5.
        self.brush               = Brush(self.brush_size, reference)

        plt.imshow(self.color_palette, interpolation='None')

        plt.imshow(self.brush.pattern, interpolation='None', cmap='gray')

        logger.debug("Agent started: {}".format(reference))

    def pick_colors (self, n):
        # Return n most frequent colors from the color_palette.
        return np.array([sorted(self.color_reference, key=self.color_reference.get)[:n]])

    def evaluate(self, artifact):
        """Evaluate given artifact with respect to the agent's  memory
        and how useful it if for the assigned job.
        :param artifact: :class:`~creamas.core.Artifact` to be evaluated
        :returns:
            (evaluation, framing)-tuple, the framing is the combined framing of
            both the value and novelty.
        """

        value, value_framing     = self.value(artifact)
        novelty, novelty_framing = self.novelty(artifact)
        surpris, surpris_framing = self.surprisingness(artifact)

        framing = {'value': value_framing, 'novelty':novelty_framing, 'suprisingness' : surpris_framing}
        evaluation = (value + novelty + surpris) / 3
        return evaluation, framing

    def value(self, artifact):
        """Compute the value of a given artifact with respect to the stroke the
        agent has in its vocabulary.

        :param artifact: :class:`~creamas.core.Artifact` to be evaluated
        :returns:
            (evaluation, stroke)-tuple, containing both the evaluation and the
            stroke giving the maximum evaluation
        """

        value, matching_stroke = 0, None;
        return value, matching_stroke

    def novelty(self, artifact):
        """Compute the novelty of a given artifact with respect to the artifacts
        in the agent's memory.
        :param artifact: :class:`~creamas.core.Artifact` to be evaluated
        :returns:
            (novelty, word)-tuple, containing both the novelty value and the
            word giving the minimum novelty.
        """

        novelty, matching_stroke = 0, None;
        return novelty, matching_stroke

    def surprisingness(self, artifact):
        """Compute the surprisingness of a given artifact with respect to the artifacts
        in the agent's memory.
        :param artifact: :class:`~creamas.core.Artifact` to be evaluated
        :returns:
            (novelty, word)-tuple, containing both the surprisingness value and the
            stroke giving the minimum surprisingness.
        """

        surpris, matching_stroke = 0, None;
        return surpris, matching_stroke

    def generate(self):
        """Generate a new stroke.
        Stroke are generated mixing data memorized of patterns and colors.
        :returns: a stroke wrapped as :class:`~creamas.core.artifact.Artifact`
        """
        random_color = random.choice(self.color_palette[0])
        stroke = np.empty((self.brush_size, self.brush_size, 4))
        for row_idx in range(len(self.brush.pattern)):
            for col_idx in range(len(self.brush.pattern[row_idx])):
                for rgb_ch in range(0, 3):
                    stroke[row_idx][col_idx][rgb_ch] = random_color[rgb_ch]
                stroke[row_idx][col_idx][3] = self.brush.pattern[row_idx][col_idx]    
        # Dbg
        plt.imshow(stroke, interpolation='None')

        return Artifact(self, stroke, domain=str)

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
        logger.debug("{} invented word: {} (eval={}, framing={})"
                     .format(self.name, best_artifact.obj, max_evaluation,
                             framing))
        # Add evaluation and framing to the artifact
        best_artifact.add_eval(self, max_evaluation, fr=framing)
        return best_artifact

    async def act(self):
        """Agent acts by inventing new strokes.
        """
        artifact = self.invent(self.n)
        self.mem.memorize(artifact)
        logger.debug([a.obj for a in self.mem.artifacts])
        self.env.add_candidate(artifact)


if __name__ == "__main__":
    env = Environment.create(('localhost', 5555))
    agent = FoolPainterAgent(env, reference="../media/starring-night.jpg")
    agent.generate()
