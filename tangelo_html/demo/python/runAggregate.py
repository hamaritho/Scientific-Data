"""@package docstring
This script Aggregates data in from a given NetCDF file via a NCL script. The NCL script
takes in an input file, output file, the variable on which to aggregate, the method to use (mean, min, max),
the interval on which to aggregate (day, month, season, or year), and the outtime to set (the date/time of interval
to set the aggregate result). The output file is then a NetCDF with the aggregate data
"""

import subprocess
import sys

def run(filename, interval, method, outtime):
        infile = "infile=\"{0}\"".format(filename)
        sInterval = "interval=\"{0}\"".format(interval)
        if not method:
                sMethod = ""
        else:
                sMethod = "method=\"{0}\"".format(method)
        if not outtime:
                sOuttime = ""
        else:
                sOuttime = "outtime=\"{0}\"".format(outtime)
        outfile = "outfile=\"../tmin_aggregate_monthly.nc\""
        varname = "varname=\"tmin\""
        args = ['ncl', infile, outfile, varname, sInterval, sMethod, sOuttime, '../ncl/aggregate.ncl']
	status = subprocess.call(args)
      	if status < 0:
		print "Error aggregating data"
		return { "alert": "Error aggregating data" }
      	else:
       		return { "result":  "tmin_aggregate_monthly.nc" }
