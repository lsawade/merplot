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

from merplot.mermaid_plot import get_last_positions


if __name__ == "__main__":

    # Get arguments which is a single list
    parser = argparse.ArgumentParser()
    parser.add_argument('filelist', help='vital file list',
                        type=str, nargs='+')
    args = parser.parse_args()

    # Run
    get_last_positions(args.filelist)
