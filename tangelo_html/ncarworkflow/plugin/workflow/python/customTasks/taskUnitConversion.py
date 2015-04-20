import subprocess
import pyutilib.workflow
import os

class taskUnitConversion(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('variable')
        self.inputs.declare('outunit')
        self.outputs.declare('result')

    def execute(self):
            sFilename = "filename=\"{0}\"".format(self.filename)
            sVariable = "variable=\"{0}\"".format(self.variable)
            sOutunit = "outunit=\"{0}\"".format(self.outunit)
            wid = "wid=\"{0}\"".format(self.workflowID)
            tid = "tid=\"{0}\"".format(self.uid)
            
            args = ['ncl', '-n', '-Q', wid, tid, sFilename, sVariable, sOutunit, 'ncl/unit_conversion.ncl']
            args = filter(None,args)
            sysError = False
            nclError = False

            try:
                    status = subprocess.call(args)
            except:
                    sysError = True
                    error = "System Error: Please contact site administrator."
            if not sysError:
                if status:
                    if status == 2:
                        error = "NCL Error: Missing input parameter"
                    elif status == 3:
                        error = "NCL Error: Lat/Lon values out of range"
                    elif status == 4:
                        error = "NCL Error: Date value out of range"
                    elif status == 5:
                        error = "NCL Error: Invalid parameter value"
                    elif status == 6:
                        error = "NCL Error: Conversion error"
                    else:
                        error = "NCL Error: Error with NCL script"
                    nclError = True
            result = "/data/{0}/{1}_unitconv.nc".format(self.workflowID,self.uid)
            if not sysError or not nclError:
                if not os.path.isfile(result):
                    error = "NCL Error: Please check input parameters."
                    nclError = True
            if nclError or sysError:
                    self.result = error 
            else:
                    self.result = result