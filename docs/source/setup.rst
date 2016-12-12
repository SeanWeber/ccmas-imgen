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

The application is started by running `main.py` that can be found in the `src` folder. Currently, it does not need any arguments because all the settings are being set in the code.

.. code-block:: bash

	(venv) ~/ccmas-imgen$ cd src
	(venv) ~/ccmas-imgen/src$ python main.py

After executing the code above, the simulation is started. When it is finished, the final generated image is displayed.
