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

lonMin = (float)(config['REGION']['LON_MIN'])
lonMax = (float)(config['REGION']['LON_MAX'])

latMin = (float)(config['REGION']['LAT_MIN'])
latMax = (float)(config['REGION']['LAT_MAX'])

print("(lonMin , latMin) = (%f,%f)"%(lonMin,latMin))
print("(lonMax , latMax) = (%f,%f)"%(lonMax,latMax))

print("Starting Yearly Heat Map Generation")

increStep = (float)(config['HEATMAP']['INCR_STEP'])
incrRes = (int)(config['HEATMAP']['INCR_RES'])

heatMapGrid = hMUtil.generate_grid(lonMin, lonMax, latMin, latMax, increStep, incrRes)
boundaryArray = heatMapGrid[2]
horizontalAxis = heatMapGrid[0]
verticalAxis = heatMapGrid[1]

# for boundary in boundaryArray:
#     print(boundary)    
# print(horizontalAxis)
# print(horizontalAxis.shape)
# print(verticalAxis)
# print(verticalAxis.shape)

opFile = "../Data/M120_00_M190_80_34_16_24_26/YearlyHM.npy"

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

fileList = [ \
            "../Data/M120_00_M190_80_34_16_24_26/17_01_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_02_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_03_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_04_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_05_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_06_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_07_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_08_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_09_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_10_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_11_Dropped.csv" \
            ,"../Data/M120_00_M190_80_34_16_24_26/17_12_Dropped.csv" \
            ]

yearlyDF = pd.DataFrame()

for file in fileList:
    tempData,_ = aISDM.load_data_from_csv(file)
    yearlyDF = yearlyDF.append(tempData, ignore_index = True)

compute_heat_map(yearlyDF)
print("Done Generating Yearly Heat Map")