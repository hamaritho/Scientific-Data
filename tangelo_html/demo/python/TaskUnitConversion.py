"""@package docstring
This script Aggregates data in from a given NetCDF file via a NCL script. The NCL script
takes in an input file, output file, the variable on which to aggregate, the method to use (mean, min, max),
the interval on which to aggregate (day, month, season, or year), and the outtime to set (the date/time of interval
to set the aggregate result). The output file is then a NetCDF with the aggregate data
"""

import subprocess
import sys
import re
import pyutilib.workflow

class TaskUnitConversion(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('variable')
        self.inputs.declare('outunit')

    def execute(self):
            sFilename = "filename=\"{0}\"".format(self.filename)
            sVariable = "varname=\"{0}\"".format(self.variable)
            sOutunit = "outunit=\"{0}\"".format(self.outunit)
            args = ['ncl', '-n', '-Q', sFilename, sVariable, sOutunit, 'ncl/unit_conversion.ncl']
            args = filter(None,args)

            sysError = False
            nclError = False
            try:
                    status = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            except:
                    sysError = True
                    error = "System error, please contact site administrator."
        
            nclError = False
            if not sysError:
                    for line in status.stdout:
                            if line.find("fatal") != -1:
                                nclError = True
                                error = re.sub('\[.*?\]:',' ',line)
                                break
                            if line.find("Invalid") != -1:
                                nclError = True
                                error = re.sub('.*?Invalid','Invalid',line)
                                break
            if nclError or sysError:
                    self.result = { "error": error }
            else:
                    self.result = { "result":  "conversion_subset.nc" }