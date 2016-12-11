**************
Implementation
**************

This section briefly describes the project from a programmatic point view.

Used Libraries
==============
In order to keep the implementation on a reasonable level of complexity, we have used several libraries. They are listed below.

* `Creamas <http://assamite.github.io/creamas/>`_ library defines a multi-agent system model, voting and evaluation scheme and also an interaction model.
* `NumPy <http://www.numpy.org/>`_ library provides an efficient implementation of various data structures that can be employed in the image processing.
* `SciPy <https://www.scipy.org/>`_ implements many image processing algorithms.
* `matplotlib <http://matplotlib.org/>`_ allows our system to display newly created images and thus provide a certain level of interactivity.


Structure of implementation
===========================
The system is run by the main method in the :doc:`main`. An instance of :doc:`canvas` is created with a set of agents (a canvas is empty after initialization). The simulation is started then.

The simulation is run in iterations. In every iteration, each agent invents a new stroke and add it as a candidate to the environment. A candidate stroke is invented by generating a set of strokes and submitting the one with the maximum evaluation score. The score constists of three components - surprisingness, novelty and value. A candidate stroke is then added to an agent's memory. 

Agents vote for the best stroke which is then added to the canvas. A single stroke is added in each iteration.

After the last simulation step, the result is displayed to the user.