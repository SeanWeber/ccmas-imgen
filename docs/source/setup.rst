Set-up guide
============

This section guides throught the process of installing and setting up the project.

Requirements
------------
* Python 3.5.2
* Creamas 0.1.1
* NumPy-mkl 1.12.0b1
* matplotlib 1.5.3
* SciPy 0.18.1

Installation Guide
------------------
First clone the project from its GitHub repository.

.. code-block:: bash

	$ git clone https://github.com/ccmas-imgen/ccmas-imgen.git

Activate virtual environemnt

.. code-block:: bash

	$ source venv/bin/active

Access the project folder and install all the requirements using pip

.. code-block:: bash
	
	(venv) ~$ cd ccmas-imgen
	(venv) ~/ccmas-imgen$ pip install -r requirements.txt

Running the Application
-----------------------

The application is started by running `main.py` that can be found in the `src` folder. It supports the following command line arguments:

* --target `path/to/target/image.png`
* --inspire `path/to/inspiration/folder`
* --output `folder/for/output`
* --port `port/for/creamas`
* --agents `Number of agents`
* --steps `Number of steps in simulation`

.. code-block:: bash

	(venv) ~/ccmas-imgen$ cd src
	(venv) ~/ccmas-imgen/src$ python main.py \ 
		/../media/starring-night.png \
		/../inspiration \
		/../output \
		5555 \
		5 \
		10000


After executing the code above, the simulation is started. Each agent is given a random image from the inspiring folder. When the simulation is finished, the final generated image is stored in the output folder.
