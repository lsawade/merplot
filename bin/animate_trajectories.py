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

    # Legend title

    # wms setup
    wms = False
    wms_url = 'https://ahocevar.com/geoserver/wms'
    wms_layer = 'ne:NE1_HR_LC_SR_W_DR'

    # Run
    ML = MermaidLocations.from_vit_file(args.filelist, minlat=-45,
                                        legend_cols=1, legend_title="SPPIM",
                                        trajectory_width=6,
                                        wms=wms, wms_url=wms_url,
                                        wms_layer=wms_layer,
                                        figsize=(30, 8), fontsize=14)

    # Get paths to auxiliary data
    pp_path = os.path.join(data_path, "Papeete-Papeete.kml")
    pn_path = os.path.join(data_path, "Papeete-Noumea.kml")
    np_path = os.path.join(data_path, "Noumea-Papeete.kml")

    # Get tracks from kml paths
    pp_lat, pp_lon = get_coordinates_from_kml_path(pp_path)
    pn_lat, pn_lon = get_coordinates_from_kml_path(pn_path)
    np_lat, np_lon = get_coordinates_from_kml_path(np_path)

    # Add ship paths
    ML.add_aux_data(np_lon, np_lat, color="y", linewidth=2.5,
                    label="Nouméa-Pape'ete - Jun/Jul '18")
    ML.add_aux_data(pp_lon, pp_lat, color="r", linewidth=2.5,
                    label="Pape'ete-Pape'ete - Aug '18")
    ML.add_aux_data(pn_lon, pn_lat, color="g", linewidth=2.5,
                    label="Pape'ete-Nouméa - Aug '19")

    # Pape'ete
    p_lon = -149.5585
    p_lat = -17.5516

    # Nouméa
    n_lon = 166.4416
    n_lat = -22.2711

    # Shimizu
    s_lon = 138.50
    s_lat = 35.00

    # Valparaíso
    v_lon = -71.63
    v_lat = -33.37

    # Add Noumea marker
    ML.add_aux_data(p_lon, p_lat, linestyle="None", marker="o", markersize=7,
                    markeredgecolor='k', markerfacecolor='r', zorder=200)
    # Add Papeete marker
    ML.add_aux_data(n_lon, n_lat, linestyle="None", marker="o", markersize=7,
                    markeredgecolor='k', markerfacecolor='r', zorder=200)
    # Shimizu marker
    ML.add_aux_data(s_lon, s_lat, linestyle="None", marker="o", markersize=7,
                    markeredgecolor='k', markerfacecolor='r', zorder=200)
    # Valparaíso marker
    ML.add_aux_data(v_lon, v_lat, linestyle="None", marker="o", markersize=7,
                    markeredgecolor='k', markerfacecolor='r', zorder=200)

    # Shimizu - Valparaíso Dec ’18 - Jan ‘19 ship track
    ML.add_aux_data([s_lon, v_lon], [s_lat, v_lat], color="b", linewidth=2.5,
                    label="Shimizu-Valparaíso - Dec/Jan ’18/‘19")

    # Plot
    ML.animate()
