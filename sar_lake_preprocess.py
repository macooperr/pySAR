#----------------------------------------------------------------------------
#  3rd April, 2014; 15:08 BST (GMT+1)
#  Script by Michael A. Cooper
#  to analyse regional regional water bodies remote sensing products
#  (Schlaffer, et al., 2012). This script carries out various pre-processing
#  steps to create a 'master' lake vector to allow for further calculations.
#
#  Requirements: Spatial Analyst Extension
#
#  References:
#  Schlaffer, Stefan; Sabel, Daniel; Bartsch, Annett; Wagner, Wolfgang (2012):
#  Regional water bodies remote sensing products with links to geotiff images.
#  doi:10.1594/PANGAEA.779754
#----------------------------------------------------------------------------

### Header
scriptname = "ASAR WS Regional water bodies product (Schlaffer, et al., 2012) -- pre-process"
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

# Gather raw product
inRegion = inDrive + ":/thesis/data/sar_lake_masked/"
regionContents = os.listdir(inRegion)
    
# Gather TIFFs per region (e.g. Laptev Sea, etc.)
for r in regionContents:
    dirContents = inRegion + r + "/"
    tiffList0 = os.listdir(dirContents)
    tiffList1 = [] # List for data TIFFs
    print "\nLoading data for " + r[0:3] + " region."
    for tiffName in tiffList0:
        tiffName_front, tiffName_end = os.path.splitext(tiffName)
        if tiffName_end == ".tif":
            tiffList1.append(tiffName) # will add only data TIFF files to tiffList1

# Arcpy Tool 1: Extract by Attributes
# Process: Extract lake pixels (1) only from TIFFs
    for year in tiffList1:
        preProcess = inDrive + ":/thesis/data/sar_lake_process/" + r[0:3] + "_lakes/pre_processed/" # output folder
        whereClause = "VALUE = 1" # extract lake values (1).
        inTiff = dirContents + year
        lakesExtract = ExtractByAttributes(inTiff, whereClause)
        lakesExtract.save(preProcess + "extract_" + year[:-4] + ".tif")
    print "Pre-processing step: Extract by Attributes complete."

# Arcpy Tool 2: Raster to Polygon
# Process: Vectorising/ polygonising raster layers (lakes)
    inRasters = preProcess # input folder
    rasterList0 = os.listdir(inRasters)
    rasterList1 = [] # List for data TIFFs
    for rasterName in rasterList0:
        rasterName_front, rasterName_end = os.path.splitext(rasterName)
        if rasterName_end == ".tif":
            rasterList1.append(rasterName) # will only add TIFF files to rasterList1
    for raster in rasterList1:        
        outShapes = inDrive + ":/thesis/data/sar_lake_process/" + r[0:3] + "_lakes/polygons/" # output folder
        inRaster = inRasters + raster
        outShape = outShapes + "shp_" + raster[:-4]
        arcpy.RasterToPolygon_conversion(inRaster, outShape, "NO_SIMPLIFY", "VALUE") # polygonises raster TIFFs
    print "Pre-processing step: Raster to Polygon complete."

# Arcpy Tool 4: Polygon Union Analysis
# Process: Creates master polygon shapefile for manual cleaning and identification
    inShapes = outShapes
    shapeList0 = os.listdir(inShapes)
    shapeList1 = [] # List for .shp files
    for shapeName in shapeList0:
        shapeName_front, shapeName_end = os.path.splitext(shapeName)
        if shapeName_end == ".shp":
            shapeList1.append(shapeName) # will only add .shp files to shapeList1
    shapeList1 =  [outShapes + i for i in shapeList1] # append file path to items in shapeList1 (for Union Analysis input)
    inUnion = shapeList1
    outUnion = inDrive + ":/thesis/data/sar_lake_process/" + r[0:3] + "_lakes/" + r[0:3] + "_union"
    arcpy.Union_analysis(inUnion, outUnion, "ONLY_FID", "", "GAPS")
    print "Pre-processing step: Polygon Union complete."

# Arcpy Tool 5: Dissolve
# Process: Dissolves
    outUnion = inDrive + ":/thesis/data/sar_lake_process/" + r[0:3] + "_lakes/lake_id/" + r[0:3] + "_union"
    inUnion = outUnion + ".shp"
    outDissolve = inDrive + ":/thesis/data/sar_lake_process/" + r[0:3] + "_lakes/" + r[0:3] + "_master_lake_union"
    arcpy.Dissolve_management(inUnion, outDissolve, "FID", "", "SINGLE_PART", "DISSOLVE_LINES")
    print "Pre-processing step: Dissolve complete."
    
print "\nScript: " + scriptname + " completed."
print "Please now manually edit each region's 'master_lake_union' file before proceeding."
