#--------------------------------------------------------------------
#  19th March, 2014; 12:05 GMT
#  Script by Michael A. Cooper
#  to produce composite images of LandSat 5 scenes en masse.
#--------------------------------------------------------------------

### Header
scriptname = "LandSat 5 Composite Stack"
print "Running script: " + scriptname + "."

# Import python modules
import arcpy
import os, shutil

# Check out licenses
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")

# Overwrite files?
arcpy.env.overwriteOutput = True

print "Existing files will be over written."

### Define input variables

inRegion = "D:/thesis/data/landsat_data/"
regionContents = os.listdir(inRegion)

for r in regionContents:

    inRoot = inRegion + r + "/"
    rootContents = os.listdir(inRoot)
    rootContents.remove("zip")

    outFolder = "D:/thesis/data/landsat_stack/" + r + "/"

    print "\nLoading " + r[0:3] + " data."

    for fname in rootContents:

        # Arcpy Tool 1: Composite Bands

        inFolder = inRoot + fname + "/"

        # Local variables

        inBand1 = inFolder + fname + "_B1.TIF"
        inBand2 = inFolder + fname + "_B2.TIF"
        inBand3 = inFolder + fname + "_B3.TIF"
        inBand4 = inFolder + fname + "_B4.TIF"
        inBand5 = inFolder + fname + "_B5.TIF"
        inBand6 = inFolder + fname + "_B6.TIF"
        inBand7 = inFolder + fname + "_B7.TIF"
        outComposite = outFolder + fname + ".tif"
        print "\nProcess: 'Composite Bands' running for image... " + r[0:3] + " d:" + fname[9:13] + " p:" + fname[3:6] + " r:" + fname[6:9] + "."

        # Process: Composite Bands
        arcpy.CompositeBands_management(inBand1 + ";" + inBand2 + ";" + inBand3
                                        + ";" + inBand4 + ";" + inBand5 + ";" +
                                        inBand6 + ";" + inBand7, outComposite)

        print "Process successfully completed for image... " + r[0:3] + " region" + " y:" + fname[9:13] + " p:" + fname[3:6] + " r:" + fname[6:9] + "."

print "\nScript: " + scriptname + " successfully completed."


