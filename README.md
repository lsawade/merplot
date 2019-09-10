# Mermaid plot utility

Hi! This is a simple and more or less short module to plot Mermaid float 
locations and trajectories on a map. The full documentation can be found is 
hosted by readthedocs ([merplot](http://merplot.rtfd.io/)).

## Installation

As of now, you need obspy because its UTCDateTime class which is very 
convenient, but I am looking into `matplotlib`'s datetime utilities which I 
think can avoid the need for `obspy` and make the code simpler, in fact.
Other than that `numpy`, `matplotlib` and `cartopy` are required to run the 
plotting scripts.

The following series of commands will create a conda environment, install the
dependencies, and finally install the package itself. 

Next, the we have to activate the environment and download dependencies.

Activation & Installation:

```bash
# Change directory to the merplot directory:
cd <merplot_dir>

# Create environment and installs dependencies
conda env create -f environment.yml

# Activate environment
conda activate merplot # the name is defined in the installation name

# Followed by
pip install -e .
```

Everything except the last line prepares your system for the installation, 
and the last line installs the package.

## Basic Usage

There are two ways of using the module. You can either use the module by 
itself or the python "binaries" in the `bin` directory -- for 
the former, you will have to import stuff manually as follows.

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

The usage of the binaries is the following:

### Simple Map
```bash
$ ./bin/plot_mermaid_locations.py <.vit files>
```

If you use the data from the data directory and are in the `merplot` directory:

```bash
$ ./bin/plot_mermaid_locations.py data/*.vit
```

### Animated Map

```bash
$ ./bin/animate_trajectories.py <.vit files>
```

If you use the data from the data directory and are in the `merplot` directory:

```bash
$ ./bin/animate_trajectories.py data/*.vit
```


## Remarks

There are more functions in the module, but describing every usage is a bit 
too extensive in a `README`. Check out the module itself, it is fairly well 
documented with some use cases of the simple functions. Also there is a tiny 
auto documentation.

Happy plotting!


PS: Let me know if there are issues!
