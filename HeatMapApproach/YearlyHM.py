import sys
import os
import numpy as np
import pandas as pd

import configparser
sys.path.insert(0, '../Common/')

from AISDataManager import AISDataManager
import Constants as c
import HMUtils as hMUtil
import TimeUtils as timeUtils
import SimpleUtils as sU

runInCOEUS = 0

config = configparser.ConfigParser()

if(runInCOEUS == 0):
    config.read('../MyConfig.INI')
else:
    config.read('/home/jcharla/LiporLab/Conan/MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

aISDM = AISDataManager()
numCores = multiprocessing.cpu_count()

lonMin = (float)(config['HEATMAP']['LON_MIN'])
lonMax = (float)(config['HEATMAP']['LON_MAX'])

latMin = (float)(config['HEATMAP']['LAT_MIN'])
latMax = (float)(config['HEATMAP']['LAT_MAX'])

print("(lonMin , latMin) = (%f,%f)"%(lonMin,latMin))
print("(lonMax , latMax) = (%f,%f)"%(lonMax,latMax))

print("Starting Yearly Heat Map Generation")

increStep = (float)(config['HEATMAP']['INCR_STEP'])
incrRes = (int)(config['HEATMAP']['INCR_RES'])
fileSuffix = (config['HEATMAP']['FILE_SUFFIX'])
opFile = (config['HEATMAP']['OUTPUT_FILE'])

yearsToConsider = [int(year) for year in (config['HEATMAP']['YEARS_TO_CONSIDER'].split(','))]


heatMapGrid = hMUtil.generate_grid(lonMin, lonMax, latMin, latMax, increStep, incrRes)
boundaryArray = heatMapGrid[2]
horizontalAxis = heatMapGrid[0]
verticalAxis = heatMapGrid[1]

print(horizontalAxis.shape)
print(verticalAxis.shape)

SOURCE_DIR = sU.convert_boundary_to_string(lonMin \
                                        , lonMax \
                                        , latMin \
                                        , latMax \
                                        )

fileNameList = []
for year in yearsToConsider:
    for monthNum in range(1,13):
        fileName = "../Data/"+SOURCE_DIR+"/"+"%02d"%(year)+"_"+"%02d"%(monthNum)+fileSuffix+".csv"
        fileNameList.append(fileName)


def compute_heat_map(localDf):
	npHeatMap = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	for i in range(len(boundaryArray)):
		boundedDF = aISDM.filter_based_on_lon_lat(localDf,boundaryArray[i][0]\
													,boundaryArray[i][1]\
													,boundaryArray[i][2]\
													,boundaryArray[i][3]\
													)
		vesselList = aISDM.get_list_of_unique_mmsi(boundedDF)
		npHeatMap[i] = len(vesselList)
		print("Done Computing %d"%(i))
	np.save(opFile, npHeatMap)

yearlyDF = pd.DataFrame()

for file in fileNameList:
    tempData,_ = aISDM.load_data_from_csv(file)
    yearlyDF = yearlyDF.append(tempData, ignore_index = True)

compute_heat_map(yearlyDF)
print("Done Generating Yearly Heat Map")