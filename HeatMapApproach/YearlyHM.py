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

lonMin = (float)(config['REGION']['LON_MIN'])
lonMax = (float)(config['REGION']['LON_MAX'])

latMin = (float)(config['REGION']['LAT_MIN'])
latMax = (float)(config['REGION']['LAT_MAX'])

print("(lonMin , latMin) = (%f,%f)"%(lonMin,latMin))
print("(lonMax , latMax) = (%f,%f)"%(lonMax,latMax))

print("Starting Yearly Heat Map Generation")

increStep = (float)(config['HEATMAP']['INCR_STEP'])
incrRes = (int)(config['HEATMAP']['INCR_RES'])
fileSuffix = (config['HEATMAP']['FILE_SUFFIX'])

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

opFile = "../Data/"+SOURCE_DIR+"/YearlyHM"+fileSuffix+".npy"

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
            "../Data/"+SOURCE_DIR+"/17_01"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_02"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_03"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_04"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_05"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_06"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_07"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_08"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_09"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_10"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_11"+fileSuffix+".csv" \
            ,"../Data/"+SOURCE_DIR+"/17_12"+fileSuffix+".csv" \
            ]

yearlyDF = pd.DataFrame()

for file in fileList:
    tempData,_ = aISDM.load_data_from_csv(file)
    yearlyDF = yearlyDF.append(tempData, ignore_index = True)

compute_heat_map(yearlyDF)
print("Done Generating Yearly Heat Map")