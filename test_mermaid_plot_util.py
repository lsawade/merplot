

import os
import pytest
import unittest
from obspy import UTCDateTime
from mermaid_plot import min_UTC
from mermaid_plot import max_UTC

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
