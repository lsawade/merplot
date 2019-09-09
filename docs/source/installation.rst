Installation
============

The installation is extremely simple as long as you have anaconda downloaded
and installed, if not check their website and download the most recent version
(`Anaconda <Ehttps://docs.anaconda.com/anaconda/install/>`_).

First of all you should as with so many packages set up an environment.

.. code-block:: bash

    conda create -n merplot python=3.7

Here, I set the name of the environment to merplot. Of course, you can change
the name, but make sure you change it in the following steps as well.
Especially advanced Users may jump over this point.
This creates a conda environment which will be convenient to work in as the
rest of the computer is not "disturbed".

Next, the we have to activate the environment, and download and
install dependencies into the environment

Environment activation:

.. code-block:: bash

    conda activate merplot

Then, to install everything you need, simply enter...

.. code-block::

    # Change directory to the merplot directory:
    conda install --file requirements.txt

    # Followed by
    pip install -e .

Then, everything should be installed.
