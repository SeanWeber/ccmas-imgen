*************
Project goals
*************

The main goal of our project is to create a creative multi-agent system that paints images.

Each agent receives an image from the inspiring set. Based on the image, an agent generates a palette of colors and a set of brushes.

Agents share a common canvas. In every iteration, each agent draws a stroke in the canvas using one of its brushes and a color from its palette. Every agent's goal is to propagate the style of 'his' image into the final painting.

The system uses two-level evaluation. Firstly, each agent is able to evaluate value, novelty and surprisingness of a stroke. Secondly, the environment is able to estimate the quality of the agents' painting. This allows us to compare results from different sets of agents (and different runs).

This process is visualised in the diagram.

.. image:: ./img/diagram.png

Why is the system creative?
===========================

Even though each agent tries to recreate its image which could be considered as a mere generation, we can say that the system as a whole is creative. 

Firstly, each agent tries to generalise the information that is contained in its image data. Agent extracts the most frequent colours in the image. Also, new strokes aren't just parts of the original image but instead they are expressed as brushes of various shapes.

Secondly, the target image is painted by a set of agents. These agents have different opinions on how the image should look like, but at the same time, they share a common evaluation function. This function ensures that the new image is valuable. Also as there are multiple agents in the system, a newly produced image should show novelty.

Elements of the system
======================

Agent
-----
* "Fool with brush".
* The process performed by an agent is visualised in the diagram below.

.. image:: ./img/agent.png

Artefact (= Stroke)
-------------------
* Modification of the shared canvas.
* A stroke is created by combining a brush with a colour from agent's palette.

.. image:: ./img/stroke.png

Environment (= Canvas)
----------------------
* A shared canvas. Agents paint their strokes on the canvas.
* An agent tries to modify the canvas in a valuable and novel way. That means it tries to choose a spot on canvas that hasn't been used many times before. 

Memory model
------------
* The system uses a simple ListMemory model.
* An agent remembers last n strokes and try to avoid repetition of the same strokes.
* This is another source of novelty in the system.

Interactions
------------
* The system contains a communication schema that allows agents to communicate with each other.
* An agent can request other agent's opinion about its stroke.

Inspiring set
-------------
* A predefined set of images. An agent defines its brushes and palette based on an image from this set.
