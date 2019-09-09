# Mermaid plot utility

Hi! This is a simple and more or less short module to plot Mermaid float 
locations and trajectories on a map.

## Installation

As of now, you need obspy because its UTCDateTime class which is very 
convenient, but I am looking into `matplotlib`'s datetime utilities which I 
think can avoid the need for `obspy` and make the code simpler, in fact.
Other than that `numpy`, `matplotlib` and `cartopy` are required to run the 
plotting scripts.

The following series of commands should make it possible to install necessary
software (no actual installation is necessary for this plotting utility).

```bash
conda create -n merplot python=3.7
```

Here, I set the name of the environment to merplot. Of course, you can change
the name, but make sure you change it in the following steps as well. 
Especially advanced Users may jump over this point.
This creates a conda environment which will be convenient to work in as the 
rest of the computer is not "disturbed".

Next, the we have to activate the environment and download dependencies.

Activation:
```bash
conda activate merplot
```

to install everything you need, simply enter...
```bash
# CHange directory to the merplot directory:
conda install --file requirements.txt

# Followed by
pip install -e .
```

Then, everything should be installed and working.

## Usage

There are two ways of using the module. You can either use the python 
"binaries" in the `bin` directory or you may use the module by itself -- 
meaning you will have to import stuff manually as follows.

```python
import glob
from merplot.mermaid_plot import MermaidLocations

# Find all vital files in a directory
vital_file_list = glob.glob("<path_to_your_dir>/*.vit")  

# Create ML plotting class
ML = MermaidLocations.from_vit_file(vital_file_list)

# Plot full map
ML.plot()
```

In the example directory, there are two very detailed examples that cover 
both the static map example as well as the animation.

There are more functions in the module, but describing every usage is a bit 
too extensive in a `README`. Check out the module itself, it is fairly well 
documented with some use cases of the simple functions. Also there is a tiny 
auto documentation.

Happy plotting!


PS: Let me know if there are issues!
