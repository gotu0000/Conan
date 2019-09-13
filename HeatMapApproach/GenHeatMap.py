import sys
sys.path.insert(0, '../Common/')

import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd

import os

#config parser
import configparser

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
# config.read('/home/jcharla/LiporLab/Conan/MyConfig.INI')
config.read('../MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

print("Starting Hourly Heat Map Generation")

def generate_grid(xMin,xMax,yMin,yMax,step,precision):
	xGrid = np.arange(xMin,xMax,step)
	xGrid = np.around(xGrid,precision)
	yGrid = np.arange(yMin,yMax,step)
	yGrid = np.around(yGrid,precision)

	xYMinMax = []
	gridCounter = 0
	for i in range(0,yGrid.shape[0]):
	    for j in range(0,xGrid.shape[0]):
	        if(i < (yGrid.shape[0]-1)):
	            if(j < (xGrid.shape[0]-1)):
	                localXMin = xGrid[j]
	                localXMax = xGrid[j+1]
	                localYMin = yGrid[i]
	                localYMax = yGrid[i+1]
	            else:
	                localXMin = xGrid[j]
	                localXMax = np.around(xGrid[j]+step,precision)
	                localYMin = yGrid[i]
	                localYMax = yGrid[i+1]
	        else:
	            if(j < (xGrid.shape[0]-1)):
	                localXMin = xGrid[j]
	                localXMax = xGrid[j+1]
	                localYMin = yGrid[i]
	                localYMax = np.around(yGrid[i]+step,precision)
	            else:
	                localXMin = xGrid[j]
	                localXMax = np.around(xGrid[j]+step,precision)
	                localYMin = yGrid[i]
	                localYMax = np.around(yGrid[i]+step,precision)        
	        xYMinMax.append([localXMin,localXMax,localYMin,localYMax,gridCounter])
	        gridCounter = gridCounter + 1
	return xGrid, yGrid, xYMinMax


# lonMin = (float)(config['REGEION']['LON_MIN'])
# lonMax = (float)(config['REGEION']['LON_MAX'])

# latMin = (float)(config['REGEION']['LAT_MIN'])
# latMax = (float)(config['REGEION']['LAT_MAX'])

lonMin = -120.0
lonMax = -119.0

latMin = 33.5
latMax = 34.5

print(lonMin,latMin)
print(lonMax,latMax)

# increStep = (float)(config['HOURLY_HEATMAP']['INCR_STEP'])
# incrRes = (int)(config['HOURLY_HEATMAP']['INCR_RES'])

increStep = (float)(0.05)
incrRes = (int)(2)

heatMapGrid = generate_grid(lonMin, lonMax, latMin, latMax, increStep, incrRes)

boundaryArray = heatMapGrid[2]
horizontalAxis = heatMapGrid[0]
verticalAxis = heatMapGrid[1]

# print(horizontalAxis)
# print(horizontalAxis.shape)
# print(verticalAxis)
# print(verticalAxis.shape)
# for boundary in boundaryArray:
# 	print(boundary)

def compute_heat_map(ipFile,opFile):
	npHeatMap = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	#FIXME 
	#exception in case of empty data frame
	try:
		localDf , retVal = aISDM.load_data_from_csv(ipFile) 
		if(retVal == c.errNO['SUCCESS']):
			#assumption is len(boundaryArray)
			#and shape[0] of npHeatMap is same
			for i in range(len(boundaryArray)):
				boundedDF = aISDM.filter_based_on_lon_lat(localDf,boundaryArray[i][0]\
															,boundaryArray[i][1]\
															,boundaryArray[i][2]\
															,boundaryArray[i][3]\
															)
				vesselList = aISDM.get_list_of_unique_mmsi(boundedDF)
				npHeatMap[i] = len(vesselList)

			np.save(opFile, npHeatMap)
		else:
			print("Something wrong with loading")
	except:

		#just store the empty file
		np.save(opFile, npHeatMap)
	return npHeatMap

#FIXME get this from config file
# iPDirectory = "../Data/AIS/LAPort/Hourly/"
# iPDirectory = "../Data/AIS/MMSI/Hourly/"
# iPDirectory = "../Data/AIS/LAPort/HourlyInterval/"
# iPDirectory = "../Data/AIS/LAPort/DailyInterval/"
# iPDirectory = "../Data/AIS_0117_0317_30_M124_35_M118/Hourly/"
# iPDirectory = "../Data/AIS_0117_0317_30_M124_35_M118/HourlyInterval/"
# iPDirectory = "../Data/AIS_0117_0317_30_M124_35_M118/SixHourly/"
# iPDirectory = "../Data/AIS_0117_0317_31_M120_345_M117/Hourly/"
# iPDirectory = "../Data/AIS_0117_0317_31_M120_345_M117/HourlyIntvl/"
# iPDirectory = "../Data/AIS_0117_0317_31_M120_345_M117/DailyIntvl/"
# iPDirectory = "../Data/AIS_0117_0317_31_M120_345_M117/SixHourly/"

# iPDirectory = "../Data/AIS_0117_1217_31_M120_345_M117/Monthly/"
# iPDirectory = "../Data/AIS_0117_1217_31_M120_345_M117/Hourly/"
# iPDirectory = "../Data/AIS_0117_1217_31_M120_345_M117/HourlyOnce/"
# iPDirectory = "../Data/AIS_0117_1217_31_M120_345_M117/Weekly/"
# iPDirectory = "../Data/AIS_SB/Hourly/"
iPDirectory = "../Data/AIS_SB/Tenly/"

# oPDirectory = "../Data/AIS/LAPort/HourlyHeatMap/"
# oPDirectory = "../Data/AIS/MMSI/HourlyHeatMap/"
# oPDirectory = "../Data/AIS/LAPort/HourlyIntvlHM/"
# oPDirectory = "../Data/AIS/LAPort/DailyIntvlHM/"
# oPDirectory = "../Data/AIS_0117_0317_30_M124_35_M118/HourlyHM/"
# oPDirectory = "../Data/AIS_0117_0317_30_M124_35_M118/HourlyIntvlHM/"
# oPDirectory = "../Data/AIS_0117_0317_30_M124_35_M118/SixHourlyHM/"
# oPDirectory = "../Data/AIS_0117_0317_31_M120_345_M117/HourlyHM/"
# oPDirectory = "../Data/AIS_0117_0317_31_M120_345_M117/HourlyIntvlHM/"
# oPDirectory = "../Data/AIS_0117_0317_31_M120_345_M117/DailyIntvlHM/"

# oPDirectory = "../Data/AIS_0117_1217_31_M120_345_M117/MonthlyHM/"
# oPDirectory = "../Data/AIS_0117_1217_31_M120_345_M117/HourlyHM/"
# oPDirectory = "../Data/AIS_0117_1217_31_M120_345_M117/HourlyHM/"
# oPDirectory = "../Data/AIS_0117_1217_31_M120_345_M117/HourlyOnceHM/"
# oPDirectory = "../Data/AIS_0117_1217_31_M120_345_M117/WeeklyHM/"
# oPDirectory = "../Data/AIS_SB/HourlyHM/"
oPDirectory = "../Data/AIS_SB/TenlyHM/"

ipOpFileList = []

# startNum = (int)(config['HOURLY_HEATMAP']['START_NUM'])
# endNum = (int)(config['HOURLY_HEATMAP']['END_NUM'])
startNum = 0
endNum = 8760*6

for i in range(startNum,endNum):
	ipName = iPDirectory + str(i) + '.csv'
	opName = oPDirectory + str(i) + '.npy'
	ipOpFileList.append([ipName,opName])

numCores = multiprocessing.cpu_count()
print(numCores)

# for iPOP in ipOpFileList:
# 	compute_heat_map(iPOP[0],iPOP[1])
# Parallel(n_jobs=numCores, verbose=10)(delayed(compute_heat_map)(iPOP[0],iPOP[1]) for iPOP in ipOpFileList)
Parallel(n_jobs=7, verbose=10)(delayed(compute_heat_map)(iPOP[0],iPOP[1]) for iPOP in ipOpFileList)