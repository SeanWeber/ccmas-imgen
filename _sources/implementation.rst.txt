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
The system is run by the main method in the :doc:`main`. An instance of :doc:`canvas` is created with a set of agents. The simulation is started then.

The simulation is run in iterations. In every iteration, each agent proposes a new stroke...

(this part of the documentation is to be finished as we finalise the evaluation scheme)