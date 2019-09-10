Tutorial
========

The tutorial is not much of a tutorial, but rather to example files with
results.

Static Map
----------

The first and maybe most important result is the static map, which can be
plotted using the following example (link to download script at the bottom.)

.. include:: ../../examples/static_example.py
    :code: python


:download:`this example script <../../examples/static_example.py>`


Animation
---------

The other interesting plotting tool is the animation creation tool, which
still is based on the same class, but as the name suggests animates the
trajectories of the mermaids. It basically works the exact same way, but the
plotting of the map is triggered by a different class method.

For the animation and especially to save the movies, certain packages must be
installed. If you are working on a Mac:

.. code-block:: bash

    # Install Imagemagick if you wanna make gifs
    brew install imagemagick

    # Install ffmpeg if you want to make mpeg's
    brew install ffmpeg

Afterwards, you can run the following example.

.. include:: ../../examples/static_example.py
    :code: python


See :download:`this example script <../../examples/animation_example.py>`


Binaries
--------

There are a few binaries that were created to make the