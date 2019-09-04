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

from mermaid_plot import get_coordinates_from_kml_path

if __name__ == "__main__":
    """
    .. warning::
    
        Important for this is that the kml file can only contain a single 
        path.
    
    """

    # Get arguments which is a single list
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='.kml file containing a path (will fail '
                                     'if not)',
                        type=str)
    args = parser.parse_args()

    # Run
    lat, lon = get_coordinates_from_kml_path(args.file)

    # Print lats and lons

    for la, lo in zip(lat, lon):
        print("%f,%f" % (la,lo))