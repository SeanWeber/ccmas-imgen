*************
Project goals
*************

The main goal of our project is to create a creative multi-agent system that paints images.

Each agent receives an image from the inspiring set. Based on the image, an agent generates a palette of colors and a set of brushes.

Agents share a common canvas. In every iteration, each agent draws a stroke in the canvas using one of its brushes and a color from its palette. Every agent's goal is to propagate the style of 'his' image into the final painting.

The system uses two-level evaluation. Firstly, each agent is able to evaluate value, novelty and surprisingness of a stroke. Secondly, the environment is able to estimate the quality of the agents' painting. This allows us to compare results from different sets of agents (and different runs).

This process is visualised in the diagram.

TBA: how does an agent choose a position of its stroke in the canvas?
TBA: describe the evaluation process in detail

.. image:: ./img/diagram.png

Why is the system creative?
===========================

TBA

Elements of the system
======================

Agent
-----
* "Fool with brush".
* The process performed by an agent is visualised in the diagram below.

.. image:: ./img/agent.png

Artifact (= Stroke)
-------------------
* Modification of the shared canvas.
* A stroke is created by combining a brush with a color from agent's palette.

.. image:: ./img/stroke.png

Environment (= Canvas)
----------------------
* A shared canvas. Agents paint their strokes in the canvas.

Memory model
------------
* The system uses a simple ListMemory model.
* TBA

Interactions
------------
* TBA

Inspiring set
-------------
* A predefined set of images. An agent defines its brushes and palette based on an image from this set.

