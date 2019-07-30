# %matplotlib inline
# import matplotlib.pyplot as plt
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
config.read('MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

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


lonMin = (float)(config['REGEION']['LON_MIN'])
lonMax = (float)(config['REGEION']['LON_MAX'])

latMin = (float)(config['REGEION']['LAT_MIN'])
latMax = (float)(config['REGEION']['LAT_MAX'])

print(lonMin,latMin)
print(lonMax,latMax)

increStep = 0.01
incrRes = 2

heatMapGrid = generate_grid(lonMin, lonMax, latMin, latMax, increStep, incrRes)

boundaryArray = heatMapGrid[2]
horizontalAxis = heatMapGrid[0]
verticalAxis = heatMapGrid[1]

def compute_heat_map(ipFile,opFile):
	npHeatMap = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
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
	return npHeatMap

#FIXME get this from config file
iPDirectory = "/home/jcharla/PDX/LiporLab/Conan/Data/AIS_2017_LA/LAPort/Hourly/"
oPDirectory = "/home/jcharla/PDX/LiporLab/Conan/Data/AIS_2017_LA/LAPort/HourlyHeatMap/"
ipOpFileList = []

#FIXME get this from file
for i in range(0,8760):
	ipName = iPDirectory + str(i) + '.csv'
	opName = oPDirectory + str(i) + '.npy'
	ipOpFileList.append([ipName,opName])

numCores = multiprocessing.cpu_count()
print(numCores)

Parallel(n_jobs=numCores, verbose=10)(delayed(compute_heat_map)(iPOP[0],iPOP[1]) for iPOP in ipOpFileList)