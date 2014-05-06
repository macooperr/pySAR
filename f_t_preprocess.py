#----------------------------------------------------------------------------
#  20th March, 2014; 12:50 GMT
#  Script by Michael A. Cooper
#  to take regional surface soil moisture and freeze/thaw timing remote
#  sensing products (Sabel, et al., 2012) and to carry out pre-processing
#  steps to allow further calculations.
#
#  Requirements: Spatial Analyst Extension
#
#  References:
#  Sabel, Daniel; Park, Sang-Eun; Bartsch, Annett; Schlaffer, Stefan; Klein,
#  Jean-Pierre; Wagner, Wolfgang (2012): Regional surface soil moisture and
#  freeze/thaw timing remote sensing products with links to geotiff images.
#  doi:10.1594/PANGAEA.779658
#----------------------------------------------------------------------------

### Header
scriptname = "ASAR GM Freeze/thaw product (Sabel, et al., 2012) -- Pre-processing"
print "\nRunning script: " + scriptname + "."

# Import python modules
import arcpy
import os, sys, shutil

# Check out licenses
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("spatial")

# Overwrite existing files
arcpy.env.overwriteOutput = True

### Define input variables
# Define drive letter
inDrive = raw_input('Please define drive letter (e.g. D, C, etc.): ')

# Gather freeze/thaw raw product
inRegion = inDrive + ":/thesis/data/f_t_data/"
regionContents = os.listdir(inRegion)

# Gather freeze/thaw product per region (e.g. Laptev Sea, etc.)
for r in regionContents:
    dirContents = inRegion + r + "/"
    tiffList0 = os.listdir(dirContents)
    tiffList1 = []
    print "\nLoading data for " + r[21:24] + " region."
# Create list of freeze (fre) and thaw (tha) TIFFs per region
    for tiffName in tiffList0:
        tiffName_front, tiffName_end = os.path.splitext(tiffName)
        if tiffName_end == ".tif" and tiffName_front[-3:] != "num": # will only add TIFFs and ignore quality (num) TIFF files
            tiffList1.append(tiffName) # will only add freeze and thaw TIFF files to dirlist1

# Arcpy Tool: SetNull
# Process: Set Null (values of -1)
    for tiffName in tiffList1:
        outFolder = inDrive + ":/thesis/data/f_t_process/" +  r[21:24] + "_seasons/raw_null/"
        whereClause = "VALUE = -1"
        inTiff = dirContents + tiffName
        inFalseTiff = dirContents + tiffName
        freezeSetNull = SetNull(inTiff, inFalseTiff, whereClause)
        freezeSetNull.save(outFolder + "null_" + tiffName_front + ".tif")
    print "Pre-processing step: Set Null complete."

print "\nScript: " + scriptname + " completed."