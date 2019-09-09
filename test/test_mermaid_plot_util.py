

import os
import sys
# Appending main path.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import unittest
from obspy import UTCDateTime
from mermaid_plot import min_UTC
from mermaid_plot import max_UTC
from mermaid_plot import read_yaml_file
from mermaid_plot import get_coordinates_from_kml_path
from mermaid_plot import get_positions

# Adding the test data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

class TestMermaidPlotting(unittest.TestCase):
    """Test class to test the MERMAID plotting utilities."""

    def test_min_UTC(self):
        """Testing the min_UTC function which finds the oldest UTCDatetime."""

        # Create set of three separat timestamps
        UTC_list = [UTCDateTime("2000-01-01T00:00:00"),
                    UTCDateTime("2010-01-01T00:00:00"),
                    UTCDateTime("1999-01-01T00:00:00")]

        # The solution should be the last entry
        UTC, ind = min_UTC(UTC_list, ind=True)

        self.assertTrue(UTC == UTC_list[2])
        self.assertTrue(ind == 2)


    def test_max_UTC(self):
        """Testing the max_UTC function which finds the youngest UTCDatetime."""

        # Create set of three separat timestamps
        UTC_list = [UTCDateTime("2000-01-01T00:00:00"),
                    UTCDateTime("2010-01-01T00:00:00"),
                    UTCDateTime("1999-01-01T00:00:00")]

        # The solution should be the last entry
        UTC, ind = max_UTC(UTC_list, ind=True)

        self.assertTrue(UTC == UTC_list[1])
        self.assertTrue(ind == 1)


    def test_read_filter(self):
        """Tests the yaml reader. """

        # Read yaml file
        d = read_yaml_file(os.path.join(DATA_DIR, "test_filter_file.yml"))

        # Check if entry correct
        self.assertEqual(d[10]["time_filter"],
                         [["2018-11-19T07:43:01", "2018-12-19T07:43:01"],
                          ["2018-12-27T18:10:34", "2018-12-27T19:37:34"]])

    def test_kml_read(self):
        """Tests kml reading."""

        # Read things from kml
        latitudes, longitudes = get_coordinates_from_kml_path(
            os.path.join(DATA_DIR, "test.kml"))

        # Check results
        self.assertEqual(latitudes, [-17.54206757345882, -11.502869742594])
        self.assertEqual(longitudes, [-149.5691247574971, -143.9807900719819])

    def test_read_mermaid_locations(self):
        """Test read mermaid locations from vit file."""

        # Vital file.
        vit_file = os.path.join(DATA_DIR, "452.020-P-10.vit")


        # Get positions from vital file.
        mermaid_name, dates, latitudes, longitudes = \
            get_positions(vit_file)

        # Test results
        self.assertEqual("10", mermaid_name)
        self.assertEqual(dates, [UTCDateTime(2018, 12, 19, 7, 42, 52),
                                 UTCDateTime(2018, 12, 27, 18, 4, 34),
                                 UTCDateTime(2018, 12, 27, 18, 18, 41)])
        self.assertEqual(latitudes, [-13.96415, -14.10135,  -14.1011])
        self.assertEqual(longitudes, [-164.25971666666666,
                                      -164.24073333333334,
                                      -164.24168333333333])

    def test_read_locations_with_filter(self):
        """Testing the filter function."""

        # Vital file.
        vit_file = os.path.join(DATA_DIR, "452.020-P-10.vit")

        # Filter dictionary
        d = read_yaml_file(os.path.join(DATA_DIR, "test_filter_file.yml"))


        # Get positions from vital file.
        mermaid_name, dates, latitudes, longitudes = \
            get_positions(vit_file, filter_dict=d)

        # Test results
        self.assertEqual("10", mermaid_name)
        self.assertEqual(dates, [UTCDateTime(2018, 12, 27, 18, 4, 34)])
        self.assertEqual(latitudes, [-14.10135])
        self.assertEqual(longitudes, [-164.24073333333334])

