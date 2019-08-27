#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Utilities to create a simple map of the Mermaid float locations.

:author:
    Lucas Sawade (lsawade@princeton.edu), 2019

:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lgpl.html):

Last Update:
    August 2019

"""

import re
import os

# I think there is probably a matplotlib function with date time, if I can
# find out about that, I can write a simple vincenty formula for
# locations2degree. If I just prepend it to the code and call it the same the
# code will not even change.
# Then it's only basic python code + matplotlib + numpy + cartopy
from obspy import UTCDateTime
from obspy.geodetics.base import locations2degrees
import argparse
import codecs
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt


#--------- This is necessary for round caps in the line collection-------------
"""
This might sound arbitrary, but the LineCollection plots very sharps lines 
that end at the actually point. This means that if there is a turn in 
Mermaids trajectory, the line becomes super-jagged; we don't want that. The 
work around is the following, which enables `round` line caps.
"""
import types
from matplotlib.backend_bases import GraphicsContextBase, RendererBase

class GC(GraphicsContextBase):
    def __init__(self):
        super().__init__()
        self._capstyle = 'round'

def custom_new_gc(self):
    return GC()

RendererBase.new_gc = types.MethodType(custom_new_gc, RendererBase)
#------------------------------------------------------------------------------


def max_UTC(UTC_list, ind=False):
    """ Get first, latest time in a list of UTC

    :param UTC_list: list of UTCDateTime stamps
    :param ind: boolean defining whether the index in list is supposed to be
                output. Default False
    :return: latest UTCDateTime stamp. If ind is True, tuple of (latest time
             stamp, index) is output.

    """

    counter = 0
    index = 0
    max_timestamp = UTC_list[0]

    for time in UTC_list:
        if time > max_timestamp:
            max_timestamp = time
            index = counter
        counter +=1

    if ind:
        return max_timestamp, index
    else:
        return max_timestamp


def min_UTC(UTC_list, ind=False):
    """ Get first, earliest time in a list of UTC

    :param UTC_list: list of UTCDateTime stamps
    :param ind: boolean defining whether the index in list is supposed to be
                output. Default False
    :return: earliest UTCDateTime stamp. If ind is True, tuple of (earliest time
             stamp, index) is output.

    """

    counter = 0
    index = 0
    min_timestamp = UTC_list[0]

    for time in UTC_list:
        if time < min_timestamp:
            min_timestamp = time
            index = counter
        counter +=1

    if ind:
        return min_timestamp, index
    else:
        return min_timestamp


def get_coordinates_from_kml_path(kml_file):
    """Reads .kml file and returns corresponding latitude and longitude
    lists. WARNING!!! Only works for kmls with a single path!"""

    # Read kml file
    kml = open(kml_file, 'r').read()

    # Catch coordinate
    coord_catch = re.findall("(.+)<coordinates>(.+)</coordinates>("
                             ".+)", kml,
                             re.DOTALL | re.MULTILINE)

    coord_list = coord_catch[0][1].split(",")

    new_list = []
    for coord in coord_list:

        coord_new = coord.strip()
        if "0 " == coord_new[:2]:
            new_list.append(coord_new[2:])
        else:
            new_list.append(coord_new)

    if new_list[-1] == '0':
        new_list.pop(-1)

    if (len(new_list) % 2) != 0:
        raise ValueError("Uneven number of coordinates. .kml read failed.\n"
                         "Coordinates: %d" % len(new_list))

    latitudes = []
    longitudes = []


    for _i, coord in enumerate(new_list):
        # print(coord)
        # print(_i % 2)
        if (_i % 2) == 0:
            longitudes.append(float(coord))

        else:
            latitudes.append(float(coord))

    return latitudes, longitudes


def get_positions(vital_file, begin, end):
    """ Reads vital file and the gps coordinates in it.

    :param vital_file: path/to/your_float.vit
    :param begin: UTCDatetime with start of gps positions
    :param end: UTCDatetime with end of gps positions

    :return: tuple of three lists (dates, latitudes, longitudes)

    """

    # Read file
    with codecs.open(vital_file, encoding='utf-8') as f:
        content = f.read()

    # Find battery values
    gps_catch = re.findall(
        "(.+): (.{3,5})deg(.+)mn, (.+)deg(.+)mn", content)

    date = [UTCDateTime(0).strptime(i[0], "%Y%m%d-%Hh%Mmn%S") for i in gps_catch]
    latitude = [float(s[1].strip()[1:]) + float(s[2]) / 60
                if s[1].strip()[0] == "N" else - float(s[1].strip()[1:])
                                               - float(s[2]) / 60
                for s in gps_catch]

    longitude = [float(s[3].strip()[1:]) + float(s[4]) / 60
                 if s[3].strip()[0] == "E" else - float(s[3].strip()[1:])
                                                - float(s[4]) / 60
                 for s in gps_catch]

    if len(date) < 1:
        return

    # Get values between the appropriate date
    i = 0
    while date[i] < begin and i < len(date)-1:
        i += 1
    j = 0
    while date[j] < end and j < len(date)-1:
        j += 1

    date = date[i:j]
    latitude = latitude[i:j]
    longitude = longitude[i:j]

    # Fix for missing GPS data.
    counter = 0
    counter_list = []
    N = len(latitude)

    date_fix = []
    latitude_fix = []
    longitude_fix = []

    for lat, lon in zip(latitude, longitude):

        # distance to papeete
        p_dist = locations2degrees(lat, lon, -17.2, -149.2)
        n_dist = locations2degrees(lat, lon, -22.3, 166.2)

        #

        # Get speed
        if counter != N-1:

            # Distance of mermaid between to successive dives
            mdist = 111.11 * locations2degrees(lat, lon, latitude[counter + 1],
                                       longitude[counter + 1])
            # Speed of the Mermaid between two successive points.
            speed = mdist / ((date[counter + 1] - date[counter]) / 3600)


        else:

            # Distance of mermaid between to successive dives
            mdist = 111.11 * locations2degrees(lat, lon, latitude[counter - 1],
                                       longitude[counter - 1])
            # Speed of the Mermaid between two successive points.
            speed = mdist / ((date[counter] - date[counter - 1]) / 3600)


        # Get coordinates under certain conditions
        if lat != 0 \
                and lon != 0 \
                and lat < 20 \
                and (lon <= -100 or lon > 100)\
                and speed < 2.0\
                and p_dist > 1.5\
                and n_dist > 1.5\
                and mdist < 1111:
            date_fix.append(date[counter])
            longitude_fix.append(lon)
            latitude_fix.append(lat)


        counter += 1

    # Get the name of the Mermaid
    mermaid_name_tmp = os.path.basename(vital_file).split(".")[1]\
                           .split("-")[1:]
    mermaid_name = mermaid_name_tmp[1].lstrip("0")

    return mermaid_name, date_fix, latitude_fix, longitude_fix


def get_last_positions(vital_file_list):
    """ Get all last positions of a list of vital files.

    :param vital_file_list:
    :return: prints list of last positions on the screen

    """

    if type(vital_file_list) is not list:
        vital_file_list = [vital_file_list]

    # print descriptor
    print("label, time, latitude, longitude")


    for vit in vital_file_list:


        # Get last position:
        mermaid_number, t, lat, lon = get_positions(vit,
                                    begin=UTCDateTime("2000-01-01T00:00:00"),
                                    end=UTCDateTime("2100-01-01T00:00:00"))

        # Check if there are no times for a Mermaid in the time window.
        if len(t) != 0:
            # Print shit
            print("%s, %s, %.5f, %.5f" % (mermaid_number, t[-1],
                                          lat[-1], lon[-1]))


def plot_path(lon, lat, **kwargs):
    """ Plots line on map.

    :param lat: list of latitudes
    :param lon: list of logitudes
    :param kwargs: keyword arguments for plotting function

    """

    # Plot track
    plt.plot(lon, lat, transform=ccrs.Geodetic(), **kwargs)


def plot_point(lon, lat, size=2,  **kwargs):
    """ Plots line on map.

    :param lat: one latitude degree
    :param lon: one longitude degree 
    :param kwargs: keyword arguments for plotting function

    """

    # Plot track
    plt.plot(lon, lat, transform=ccrs.Geodetic(), **kwargs)


def plot_text(text, lon, lat, lat_offset=0, lon_offset=0, **kwargs):
    """ Plots line on map.

    :param text: String with text input
    :param lat: one latitude degree
    :param lon: one longitude degree
    :param lat_offset: offset from latitude
    :param lon_offset: offset from longitude 
    :param kwargs: keyword arguments for plotting function

    """

    # Plot track
    plt.text(lon + lon_offset, lat + lat_offset, text,
             transform=ccrs.Geodetic(), **kwargs)


class MermaidLocations(object):
    """Class that handles plotting of MERMAIDS using the vital file input.
    The underlying mapping tool box is Cartopy which is very powerful,
    but not yet fully grown. As a result Only the PlateCarree projection can
    be used as of now; hence, no option to vary this parameter in terms of
    plotting.

    Usage:

        .. code-block:: python

            # Create ML plotting class
            ML = MermaidLocation.from_vit_file(vital_file_list)

            # Plot full map
            ML.plot()


    """

    def __init__(self, latitudes, longitudes, times=None, mermaid_names=None,
                lon_ticks=[160.0, 180.0, -180.0, -160.0, -140.0, -120.0,
                           -100.0],
                lat_ticks=[-40.0, -20.0, 0.0, 20.0],
                minlon=160.0, maxlon=255.0, minlat=-37.5, maxlat=5.0,
                central_longitude=180.0,
                mermaid_markersize=25, markerfontsize=None,
                plot_labels=True,
                trajectories=True,
                trajectory_width=4,
                trajectory_cmp="gist_heat",
                wms=False, wms_url=None, wms_layer=None,
                figsize=(15, 8)):
        """

        :param latitudes: 2D list with 1 row for each mermaid
        :type latitudes: list
        :param longitudes: 2D list with 1 row for each mermaid
        :type longitudes: list
        :param times: 2D list with 1 row for each mermaid
        :type times: list
        :param mermaid_names: List with 1 name for each mermaid
        :type mermaid_names: list
        :param lon_ticks: List of map longitude ticks for plotting. Make sure
                          you have one more index than necessary.
                          #justpythonthings
        :type lon_ticks: list
        :param lat_ticks: List of map latitude ticks for plotting. Make sure
                          you have one more index than necessary.
                          #justpythonthings
        :type lat_ticks: list
        :param minlon: Minimum map longitude
        :type minlon: float or int
        :param maxlon: Maximum map longitude
        :type maxlon: float or int
        :param minlat: Minimum map latitude
        :type minlat: float or int
        :param maxlat: Maximum map latitude
        :type maxlat: float or int
        :param central_longitude: Set the central longitude of the map.
                                  Important for plotting of the pacific for
                                  example.
        :type central_longitude: float or int
        :param begin: Datetime of float operation
        :type begin: UTCDateTime
        :param end: Datetime stamp of float operation
        :type end: UTCDateTime
        :param mermaid_markersize: Markersize for the Mermaid markers
        :type mermaid_markersize: float or int
        :param plot_labels: Plot labels of the mermaid number onto the
                               markers
        :type plot_labels: bool
        :param markerfontsize: Fontsize for Label on Mermaid marker
        :type markerfontsize: float or int
        :param trajectories: Plot trajectories of the mermaids. Default
                            `True`, but :attr:`times` has to be defined.
        :type trajectories: bool
        :param trajectory_width: Width of the trajectories' line plots
        :type trajectory_width: float or int
        :param trajectory_cmp: Colormap of the trajectories.
        :type trajectory_cmp: str
        :param wms: Get WMS map from a server.
        :type wms: bool
        :param wms_url: WMS request URL
        :type wms_url: str
        :param wms_layer: Name of the requested layer.
        :type wms_layer: str
        :param figsize: Define the figure size (Width, Height)
        :type figsize: tuple
        :return: MermaidLocation object.
        """


        # Main Data
        self.latitudes = latitudes
        self.longitudes = longitudes
        self.times = times
        self.mermaid_names = mermaid_names

        """ input data notes:
        - markerfontsize only use as fix if autoscaling doesnt work
        - 
        """
        ### Plot paramaters

        # Figure size
        self.figsize = figsize

        # MapBorders
        self.central_longitude = central_longitude
        self.bounds = [minlon, maxlon, minlat, maxlat]
        self.lon_ticks = lon_ticks
        self.lat_ticks = lat_ticks

        # Markers
        self.mermaid_markersize = mermaid_markersize
        self.plot_labels = plot_labels
        if markerfontsize == None:
            self.markerfontsize = 5/25 * self.mermaid_markersize
        else:
            self.markerfontsize = markerfontsize

        # Trajectories
        self.trajectories = trajectories
        self.trajectory_width = trajectory_width
        self.trajectory_cmap = trajectory_cmp

        # WMS settings
        self.wms = wms
        self.wms_url = wms_url
        self.wms_layer = wms_layer

        # Empty data container for extra data such as ship tracks.
        self.auxiliary_data = None
        """Will be stored in form of dictionaries 
        xdata:, ydata:, kwarg_dict"""


    @classmethod
    def from_vit_file(cls, vital_file_list,
                      begin=UTCDateTime("2000-01-01T00:00:00"),
                      end=UTCDateTime("2100-01-01T00:00:00"),
                      **kwargs):
        """Gets the content of the vital and parses it to the class. Parameters
        are the same as for the `__init__` except the `latitude`, `longitude`,
        times, and mermaid_names
        """

        # Create empty lists
        times = []
        latitudes = []
        longitudes = []
        mermaid_names = []

        for mermaid in vital_file_list:

            # Get locations and times
            mermaid_name, t, lat, lon = \
                get_positions(mermaid,
                              begin=begin,
                              end=end)

            # Check if there are no times for a Mermaid in the time window.
            if len(t) != 0:
                # Add to lists
                mermaid_names.append(mermaid_name)
                times.append(t)
                latitudes.append(lat)
                longitudes.append(lon)

        return cls(latitudes, longitudes, times=times,
                   mermaid_names=mermaid_names,
                   **kwargs)

    def compute_second_record(self):
        """Takes in all times and creates smallest and largest number from
        max and min UTCDatetimes."""
        pass

        # Create empty lists.
        first_times = []
        last_times = []

        for t in self.times:
            # Get Mermaid start and endtimes
            first_times.append(t[0])
            last_times.append(t[-1])

        # Set oldest and youngest date
        self.first_time = min_UTC(first_times)
        self.last_time = max_UTC(last_times)

        # Get a history of the time in seconds.
        self.times_s = []

        # Make seconds out of UTCDateTimes
        for _i, rows in enumerate(self.times):
            new_row = []
            for _j, column in enumerate(rows):
                new_row.append(self.last_time - column)
            self.times_s.append(new_row)

    def add_aux_data(self, lon, lat, **kwargs):
        """ Adding auxiliary data. """

        if self.auxiliary_data is None:
            self.auxiliary_data = []

        # Create empty dictionary
        data_dict = dict()


        data_dict["lon"] = lon
        data_dict["lat"] = lat
        data_dict["kwargs"] = kwargs

        # Add data to data list
        self.auxiliary_data.append(data_dict)

    def plot(self):
        """Plots everything"""

        # Plot background map
        self.plot_map()

        # Plot Trajectories
        self.plot_trajectories()

        # Plot Mermaid markers
        self.plot_markers()

        # Plot auxiliary data
        self.plot_aux_data()

        # Plot colorbar
        self.activate_colorbar()

        # Show stuff
        plt.show(block=True)

    def plot_map(self):
        """Plots the background map for float visualization and sets the
        axis and figure properties."""

        # Set projection.
        proj = ccrs.PlateCarree(self.central_longitude)

        self.fig = plt.figure(figsize=self.figsize)
        self.ax = plt.axes(projection=proj)
        # ax.set_global()
        self.ax.frameon = False
        # ax.outline_patch.set_visible(False)

        # Set gridlines. NO LABELS HERE, there is a bug in the gridlines
        # function around 180deg
        gl = self.ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                               linewidth=1, color='lightgray', alpha=0.5,
                               linestyle='-')
        gl.xlabels_top = False
        gl.ylabels_left = False
        gl.xlines = True
        gl.xlocator = mticker.FixedLocator(self.lon_ticks)
        gl.ylocator = mticker.FixedLocator(self.lat_ticks)

        # Set ticklabels
        self.ax.set_xticks(self.lon_ticks, crs=ccrs.PlateCarree())
        self.ax.set_yticks(self.lat_ticks, crs=ccrs.PlateCarree())
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        self.ax.xaxis.set_major_formatter(lon_formatter)
        self.ax.yaxis.set_major_formatter(lat_formatter)

        # Set Map boundary
        self.ax.set_extent(self.bounds, crs=ccrs.PlateCarree())

        # Get WMS map if wanted
        if self.wms:
            self.ax.add_wms(self.wms_url, self.wms_layer)
        else:
            self.ax.stock_img()
            self.ax.add_feature(cfeature.LAND, zorder=10)
            self.ax.add_feature(cfeature.COASTLINE, zorder=10)

    def plot_trajectories(self):
        """This function uses the the complete data of latitude, longitude
        and times to plot the trajectories.

        .. warning::
            This method only works if you have defined the times!
            """

        if self.times is None:
            raise ValueError("You can only plot trajectories if the time "
                             "stamps are defined! Trajectories without times "
                             "make no sense, you see ... ?")

        else:
            self.compute_second_record()

        # Create empty list for trajectories that are too long. Meaning a
        # list of End points for split trajectories.
        self.end_points = []

        # Loop over mermaids
        for _i, (lat, lon, t) in enumerate(zip(self.latitudes, self.longitudes,
                                               self.times_s)):

            # Calling function to plot one trajectory.
            lc = self._plot_1_traj( _i, lat, lon, t,
                                    self.first_time,
                                    self.last_time,
                                    self.end_points,
                                    self.trajectory_width,
                                    self.trajectory_cmap)

            self.ax.add_collection(lc)

    @staticmethod
    def _plot_1_traj(_i, lat, lon, t, first_time, last_time,
                     end_points, line_width, cmap):
        """This function computes one trajectory for a given set of lats,
        lons. and times, as well as the first and last time of all
        trajectories in seconds, line width, cmap.

        :param _i: integer in list of mermaids
        :type _i: int
        :param lat: List of latitudes corresponfing to Mermaid track
        :type lat: list
        :param lon: List of longitudes corresponfing to Mermaid track
        :type lon: list
        :param t: List of times corresponfing to Mermaid track
        :param first_time: first timestamp in list of mermaids
        :type first_time: float
        :param last_time: last timestamp in list of floats
        :type last_time: float
        :param end_points: list that collects disconnecting points so that
        markers can be plotted.
        :type: list
        :param line_width: Width of plotted trajectory
        :type line_width: float or int
        :param cmap: color map to plot trajectory
        :type cmap: str
        :return: LineCollection to be plotted

        """

        # Transform arrays to numpy arrays for LineCollection
        lat = np.array(lat)
        lon = np.array(lon)
        t = np.array(t)

        # Create empty lists
        indeces = []
        segments = []

        # For each point pair in the trajectory of the Mermaid the loop
        # creates Line segements if the distance is smaller the 0.55deg
        for _j, (lat1, lon1, lat2, lon2) in enumerate(
                zip(lat[:-1], lon[:-1],
                    lat[1:], lon[1:])):

            # Compute distance between points
            dist = locations2degrees(lat1, lon1, lat2, lon2)

            # Only create segment if
            # Segment if distance is smaller than 5 degrees.
            if dist < 0.55:
                segments.append([(lon1, lat1), (lon2, lat2)])
                indeces.append(_j)
            else:
                end_points.append((_i, lat1, lon1, dist))

        # Create LineCollection from points
        lc = LineCollection(segments,
                            cmap=plt.get_cmap(cmap),
                            norm=plt.Normalize(0, last_time - first_time),
                            zorder=100)

        lc.set_transform(ccrs.Geodetic())
        lc.set_array(t[indeces])
        lc.set_linewidth(line_width)

        return lc

    def plot_markers(self):
        """This function uses the data included in :class:`MermaidLocations`
        to plot the last positions of each Mermaid. The external function
        :func:`plot_point` is used to achieve that.
        """

        # Mermaid marker
        mermaid_verts = [(0.1, -.9), (0.1, -0.3), (0.25, -0.3), (0.4, 0),
                         # right
                         (0.25, 0.3), (0.1, 0.3), (0.1, 0.35), (0.05, 0.35),
                         (0.05, 0.9),
                         (-0.05, 0.9), (-0.05, 0.35), (-0.1, 0.35),  # left
                         (-0.1, 0.3), (-0.25, 0.3), (-0.4, 0), (-0.25, -0.3),
                         (-0.1, -0.3), (-0.1, -1), (0.1, -.9)]

        # Plot Mermaid Locations
        for _i, (lat, lon) in enumerate(zip(self.latitudes, self.longitudes)):

            # Mermaid Marker
            plot_point(lon[-1], lat[-1], markersize=self.mermaid_markersize,
                       marker=mermaid_verts,
                       markeredgecolor='k', markerfacecolor='orange',
                       zorder=150)

            if self.plot_labels:
                plot_text(self.mermaid_names[_i], lon[-1], lat[-1],
                          lon_offset=0, lat_offset=-0.05, zorder=200,
                          horizontalalignment="center",
                          verticalalignment='center',
                          multialignment="center",
                          fontsize=self.markerfontsize, fontweight="bold")
            else:
                plot_point(lon[-1], lat[-1], marker="_", markeredgecolor='k',
                           markersize=10/25 * self.mermaid_markersize,
                           markerfacecolor='k', zorder=151)

    def plot_aux_data(self):
        """Plot data that is added to the class prior to plotting."""

        if self.auxiliary_data is not None:
            for d in self.auxiliary_data:
                # Plot track
                plot_path(d["lon"], d["lat"], **d["kwargs"])


    def activate_colorbar(self):
        """This activates the colorbar. """\

        # Calling function to plot one trajectory.
        lc = self._plot_1_traj(0, self.latitudes[0], self.longitudes[0],
                               self.times_s[0],
                               self.first_time,
                               self.last_time,
                               self.end_points,
                               self.trajectory_width,
                               self.trajectory_cmap)

        axcb = self.fig.colorbar(lc)
        axcb.set_label('seconds (s)')



if __name__ == "__main__":
    print("This function is only called by python binaries.")

