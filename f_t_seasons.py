#---------------------------------------------------------------------------
#  24th March, 2014; 17:22 GMT
#  Script by Michael A. Cooper
#  to take regional surface soil moisture and freeze/thaw timing remote
#  sensing products (Sabel, et al., 2012) and calculate season length
#  and descriptive statistics.
#
#  Requirements: Spatial Analyst Extension
#
#  References:
#  Sabel, Daniel; Park, Sang-Eun; Bartsch, Annett; Schlaffer, Stefan; Klein,
#  Jean-Pierre; Wagner, Wolfgang (2012): Regional surface soil moisture and
#  freeze/thaw timing remote sensing products with links to geotiff images.
#  doi:10.1594/PANGAEA.779658
#---------------------------------------------------------------------------

### Header
scriptname = "ASAR GM Freeze/thaw product (Sabel, et al., 2012) -- Season Length and Descriptive Statistics"
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

# Gather freeze/thaw raw product
inRegion = inDrive + ":/thesis/data/f_t_process/"
regionContents = os.listdir(inRegion)

# Gather pre-processed TIFFs per region (e.g. Laptev Sea, etc.)
for r in regionContents:
    dirContents = inRegion + r + "/raw_null/"
    tiffList0 = os.listdir(dirContents)
    tiffList1 = [] # List for Freeze (fre) TIFFs
    tiffList2 = [] # List for Thaw (tha) TIFFs
    print "\nLoading pre-processed data for " + r[0:3] + " region."
    for tiffName in tiffList0:
        tiffName_front, tiffName_end = os.path.splitext(tiffName)
        if tiffName_end == ".tif" and tiffName_front[-3:] == "fre":
            tiffList1.append(tiffName) # will add only freeze TIFF files to tiffList1
        elif tiffName_end == ".tif" and tiffName_front[-3:] == "tha":
            tiffList2.append(tiffName) # will add only thaw TIFF files to tiffList2
    print " " # for aesthetics only
    
# Arcpy Tool 1: Map Algebra
# Process: Calculate summer and winter lengths
    for freName in tiffList1:
        seasonLength = inRegion + r + "/season_length/" # output folder
        freY = int(freName[27:31]) # identifies the year (YYYY) from fre TIFF filename and creates integer.
        for thaName in tiffList2:
            thaX = int(thaName[27:31]) # identifies the year (YYYY) from tha TIFF filename and creates integer.          
            if thaX == freY: # will only calculate Summer length if fre and tha TIFF are from the same year (1 season)
                freIn = dirContents + freName 
                thaIn = dirContents + thaName 
                summerYear = Raster(freIn) - Raster(thaIn) # calulates length of Summer (days)
                summerYear.save(seasonLength + r[0:3] + "_summer_" + str(freY) + ".tif")
                print "Length of Summer (days) has been calculated for: " + r[0:3] + " region " + str(freY) + "."
            elif thaX == freY + 1: # will only calculate Winter length if tha TIFF is from following year (1 season)
                freIn = dirContents + freName
                thaIn2 = dirContents + thaName
                winterYear = (365 - Raster(freIn)) + Raster(thaIn2) # calculates length of Winter (days)
                winterYear.save(seasonLength + r[0:3] + "_winter_" + str(freY) + "_" + str(thaX)[2:5] + ".tif")
                print "Length of Winter (days) has been calculated for: " + r[0:3] + " region " + str(freY) + "/" + str(thaX)[2:5] + "."

# Arpy Tool 2: Cell Statistics (1)
# Process: Calculate descriptive statistics for summer and winter
    # Set local variables
    seasonList0 = os.listdir(seasonLength)
    seasonList1 = [] # list of summer TIFFs
    seasonList2 = [] # list of winter TIFFs
    seasonList3 = [] # list of summer & winter TIFFs (for count mask)
    for season in seasonList0:
        season_front, season_end = os.path.splitext(season)
        if season_front[4:7] == "sum" and season_end == ".tif":
            seasonList1.append(season) # will add only summer TIFF files to seasonList1
            seasonList3.append(season) # will add these TIFF files to seasonList3
        elif season_front[4:7] == "win" and season_end == ".tif":
            seasonList2.append(season) # will add only winter TIFF files to seasonList2
            seasonList3.append(season) # will add these TIFF files to seasonList3
    seasonStats = inRegion + r + "/season_stats/"

    # Summer descriptive stats
    seasonList1 = [seasonLength + i for i in seasonList1] # append file path to items in seasonList1 (for CellStatistics input)
    inSummers = seasonList1 # CellStatistics input
    # Inc. NoData pixels
    summerMeanNull = CellStatistics(inSummers, "MEAN", "NODATA") # Calculate mean summer length, including NoData pixels
    summerMeanNull.save(seasonStats + r[0:3] + "_summer_mean.tif")
    summerSTDNull = CellStatistics(inSummers, "STD", "NODATA") # Calculate standard deviation in summer length, including NoData pixels
    summerSTDNull.save(seasonStats + r[0:3] + "_summer_std.tif")
    # Exc. NoData pixels
    summerMeanNull = CellStatistics(inSummers, "MEAN", "DATA") # as above, excluding NoData pixels
    summerMeanNull.save(seasonStats + r[0:3] + "_summer_mean_nodata.tif")
    summerSTDNull = CellStatistics(inSummers, "STD", "DATA") # as above, excluding NoData pixels
    summerSTDNull.save(seasonStats + r[0:3] + "_summer_std_nodata.tif")
    print "\nDescriptive statistics have been calculated for the summer season,"
    print "(including and excluding NoData regions.)"

    # Winter descriptive stats
    seasonList2 = [seasonLength + i for i in seasonList2] # append file path to items in seasonList2 (for CellStatistics input)
    inWinters = seasonList2 # CellStatistics input
    # Inc. NoData pixels
    winterMeanNull = CellStatistics(inWinters, "MEAN", "NODATA") # Calculate mean winter length, including NoData pixels
    winterMeanNull.save(seasonStats + r[0:3] + "_winter_mean.tif")
    winterSTDNull = CellStatistics(inWinters, "STD", "NODATA") # Calculate standard deviation in winter length, including NoData pixels
    winterSTDNull.save(seasonStats + r[0:3] + "_winter_std.tif")
    # Exc. NoData pixels
    winterMeanNull = CellStatistics(inWinters, "MEAN", "DATA") # as above, excluding NoData pixels
    winterMeanNull.save(seasonStats + r[0:3] + "_winter_mean_nodata.tif")
    winterSTDNull = CellStatistics(inWinters, "STD", "DATA") # as above, excluding NoData pixels
    winterSTDNull.save(seasonStats + r[0:3] + "_winter_std_nodata.tif")
    print "Descriptive statistics have been calculated for the winter season,"
    print "(including and excluding NoData regions.)"

# Arcpy Tool 3: Conditional
# Process: Calculate binary count masks, per season, per year.
    # Set local variables
    seasonCountMask = seasonStats + "season_count/"
    for seasonMask in seasonList3:
        inSeason = seasonLength + seasonMask
        outCountMask = Con(inSeason, 1, 0, "VALUE > 0") # will set all values greater than 0 to 1, otherwise to 0
        outCountMask.save(seasonCountMask + seasonMask[0:15] + "_countmask.tif")
    print "\nCount masks have been calculated for all data in " + r[0:3] + " region."

# Arcpy Tool 4: Cell Statistics (2)
# Process: Produce count image, per season. (using "SUM" in CellStatistics)
    # Set local variables
    maskList0 = os.listdir(seasonCountMask)
    maskList1 = [] # list of summer count mask TIFFs
    maskList2 = [] # list of winter count mask TIFFs
    for countMask in maskList0:
        countMask_front, countMask_end = os.path.splitext(countMask)
        if countMask_front[4:7] == "sum" and countMask_end == ".tif":
            maskList1.append(countMask) # will add only summer count TIFFs to maskList1
        elif countMask_front[4:7] == "win" and countMask_end == ".tif":
            maskList2.append(countMask) # will add only winter count TIFFs to maskList2
    
    # Summer count image
    maskList1 = [seasonCountMask + i for i in maskList1] # append file path to items in maskList1 (for CellStatistics input)
    inSummerMasks = maskList1
    summerCount = CellStatistics(inSummerMasks, "SUM", "DATA") # sum of binary count mask images for summer
    summerCount.save(seasonCountMask + r[0:3] + "_summer_count.tif")
    print "Count image for summer in " + r [0:3] + " has been calculated."
    # Winter count image
    maskList2 = [seasonCountMask + i for i in maskList2] # append file path to items in maskList2 (for CellStatistics input)
    inWinterMasks = maskList2
    winterCount = CellStatistics(inWinterMasks, "SUM", "DATA") # sum of binary count mask images for winter
    winterCount.save(seasonCountMask + r [0:3] + "_winter_count.tif")
    print "Count image for winter in " + r [0:3] + " has been calculated."
    

print "\nScript: " + scriptname + " completed."