#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Binary to get the latest positions of the Mermaids from a list of vital
files

:author:
    Lucas Sawade (lsawade@princeton.edu), 2019

:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lgpl.html):

Last Update:
    August 2019

"""

import argparse
import sys
import os

# Add module path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mermaid_plot import MermaidLocations
from mermaid_plot import get_coordinates_from_kml_path

# Add data path
data_path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), "data")
sys.path.append(data_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('filelist', help='vital file list',
                        type=str, nargs='+')
    args = parser.parse_args()

    # Run
    ML = MermaidLocations.from_vit_file(args.filelist)

    # Get paths to auxiliary data
    pp_path = os.path.join(data_path, "Papeete-Papeete.kml")
    pn_path = os.path.join(data_path, "Papeete-Noumea.kml")
    np_path = os.path.join(data_path, "Noumea-Papeete.kml")

    # Get tracks from kml paths
    pp_lat, pp_lon = get_coordinates_from_kml_path(pp_path)
    pn_lat, pn_lon = get_coordinates_from_kml_path(pn_path)
    np_lat, np_lon = get_coordinates_from_kml_path(np_path)

    # Add ship paths
    ML.add_aux_data(pp_lon, pp_lat, color="r", linewidth=2.5)
    ML.add_aux_data(pn_lon, pn_lat, color="g", linewidth=2.5)
    ML.add_aux_data(np_lon, np_lat, color="y", linewidth=2.5)

    # Plot
    ML.plot()