Filter
======

To accommodate Mermaid testing values in the `.vit` file, we need to filter
out certain times. This is easily done by using a `.yml` file. `.yml` files
ar easy to read and easy to modify.

The standard setup of the time_filter is the following:

.. code-block:: yaml

    # Mermaid number
    1:
      # Time filter:
      # structure of the time filter is a list of lists with UTCDateTime stamps.
      #  [ [starttime , endtime],
      #    [starttime , endtime],
      #     ...                   ]
      # The location within the time window will not be considered when reading
      # the mermaid data.
      time_filter: [["2000-01-01T00:00:01" , "2018-12-27T01:37:34"]]
    2:
      time_filter: [["2000-01-01T00:00:01", "2018-12-28T16:55:32"]]
    3:
      time_filter: [["2000-01-01T00:00:01", "2019-01-01T21:13:03"],
                    ["2019-01-02T00:44:03", "2030-01-02T00:14:03"]]
    ...

For each Mermaid there is a `time_filter`, and each `time_filter`, there can
be a list of values, such that multiple windows can be filtered out. The
filter is loaded as a part of the file loading process. I decided for this
type of setup, because it is very simple to possible add other filters in the
future that can also be specified in the same `.yml` file.

The filter is called by :func:`merplot.mermaid_plot.MermaidLocations
.from_vit_file` and the filter is used to exclude certain dates in the
mermaid tracks.

