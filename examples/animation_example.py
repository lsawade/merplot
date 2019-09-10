import os
import sys
import glob

# Add path so mermaid_plot can be read
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from merplot.mermaid_plot import MermaidLocations
from merplot.mermaid_plot import get_coordinates_from_kml_path


# Add data path
data_path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), "data")
sys.path.append(data_path)

# File list
file_list = glob.glob(os.path.join(data_path, "*.vit"))

# WMS setup: Set to true of you have internet and want a high res map
wms = False
wms_url = 'https://ahocevar.com/geoserver/wms'
wms_layer = 'ne:NE1_HR_LC_SR_W_DR'

# Filter file
filter_file = os.path.join(data_path, "mermaid_filter.yml")

# Run
ML = MermaidLocations.from_vit_file(file_list,
                                    filter_dict=filter_file,
                                    minlat=-45,
                                    legend_cols=1, legend_title="SPPIM",
                                    trajectory_width=6,
                                    wms=wms, wms_url=wms_url,
                                    wms_layer=wms_layer,
                                    frames=500,
                                    movie_dpi=200,
                                    frames_per_sec=24,
                                    figsize=(15, 8), fontsize=14)

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


# Plot the animation
ML.animate()


# Write mp4
# ML.animate(f="mermaid.mp4")
