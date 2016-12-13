**********
Evaluation
**********


Examples of generated images
============================

This section presents a few images that were created using our system.

The reference and target images are the same
--------------------------------------------

In this run, each agent was given the same image 
`Vincent van Gogh - Starry Night <https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg>`_. The simulation was run with 5 agents for 10 000 steps. An agent picked a spot for its stroke randomly.

.. image:: ./img/img1.png

Different reference and target images
-------------------------------------

In this run, the agents received the image `Vincent van Gogh - Starry Night <https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg>`_.  The target image was `Leonardo da Vinci - Mona Lisa <http://www.louvre.fr/sites/default/files/imagecache/940x768/medias/medias_images/images/louvre-portrait-de-lisa-gherardini-epouse-de-francesco-del-giocondo-dite-monna-lisa-la-gioconda-ou-la-jocon.jpg>`_.

.. image:: ./img/img2.png

Multiple reference images
-------------------------
The simulation was run with 3 agents for 10 000 steps. Each agent received different reference image:

Carl from ATHF


.. image:: ./img/carl1.png

Carl from UP


.. image:: ./img/carl2.png

Carl Gustav


.. image:: ./img/carl3.png

The target image was the following one (Carl Sagan):

.. image:: ./img/carl4.png

The output is shown bellow.

.. image:: ./img/carl5.png

Conclusion
==========

We created a multi-agent system that is able to recreate images in a creative way. The example outputs show that generated images become more and more dissimilar to the target image as we use multiple reference images.

Also, generating images require quite heavy computational power. Even better results might be achieved, if we could afford running a simulation with a larger number of agents and more variable size of brushes.