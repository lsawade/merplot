

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
        self.assertTrue(d[1]["time_filter"],
                        [["2000-01-01T00:00:01" , "2018-12-27T01:37:34"]])


    def test_kml_read(self):
        """Tests kml reading."""
        pass

    def test_read_mermaid_locations(self):
        """Test read mermaid locations from vit file."""
        pass

    def test_read_locations_with_filter(self):
        """Testing the filter function."""
        pass

