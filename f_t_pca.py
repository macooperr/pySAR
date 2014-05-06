#---------------------------------------------------------------------------
#  21st April, 2014; 15:40 GMT
#  Script by Michael A. Cooper
#  to take season data created in 'f_t_seasons.py' and calculate Principle
#  Component Analysis.
#
#  Requirements: Spatial Analyst Extension
#---------------------------------------------------------------------------

### Header
scriptname = "ASAR GM Freeze/thaw product (Sabel, et al., 2012) -- Season Principal Component Analysis"
print "\nRunning Script: " + scriptname + "."

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

# Gather regional seasonality data
inRegion = inDrive + ":/thesis/data/f_t_process/"
regionContents = os.listdir(inRegion)

# Gather pre-processed season length TIFFs per region (e.g. Laptev Sea, etc.)
for r in regionContents:
    dirContents = inRegion + r + "/season_length/"
    tiffList0 = os.listdir(dirContents)
    tiffList1 = [] # List for Winter length TIFFs
    tiffList2 = [] # List for Summer length TIFFs
    print "\nLoading pre-processed data for " + r[0:3] + " region."
    for tiffName in tiffList0:
        tiffName_front, tiffName_end = os.path.splitext(tiffName)
        if tiffName_end == ".tif" and tiffName_front[4:7] == "win":
            tiffList1.append(tiffName) # will add only winter TIFF files to tiffList1
        elif tiffName_end == ".tif" and tiffName_front[4:7] == "sum":
            tiffList2.append(tiffName) # will add only summer TIFF files to tiffList2
    print " " # for aesthetics only
    
# Arcpy Tool 1: Principle Component Analysis
# Winter season
    # Set local variables
    tiffList1 = [dirContents + i for i in tiffList1] # append file path to items in tiffList1 (for PCA input)
    inWinterRasters = tiffList1 # PCA input
    outWinterDataFile = inRegion + r + "/season_pca/" + r + "_winter_pca_07_10.TXT" # Eigen values, etc. tabular output

    outWinterPCA = PrincipalComponents(inWinterRasters, 3, outWinterDataFile)
    outWinterPCA.save(inRegion + r + "/season_pca/" + r + "_winter_pca_07_10.tif") # multiband PCA raster image
    print "Principle Component Analysis has been successfully completed for the winter season."
# Summer season
    # Set local variables
    tiffList2 = [dirContents + i for i in tiffList2] # append file path to items in tiffList2 (for PCA input)
    inSummerRasters = tiffList2 # input
    outSummerDataFile = inRegion + r + "/season_pca/" + r + "_summer_pca_07_10.TXT" # Eigen values, etc. tabular output

    outSummerPCA = PrincipalComponents(inSummerRasters, 4, outSummerDataFile)
    outSummerPCA.save(inRegion + r + "/season_pca/" + r + "_summer_pca_07_10.tif") # multiband PCA raster image
    print "Principal Component Analysis has been successfully completed for the summer season."

print "\nScript: " + scriptname + " completed."