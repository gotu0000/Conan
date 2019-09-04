import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd

import os

#config parser
import configparser

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('/home/jcharla/LiporLab/Conan/MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

print("Starting Yearly Heat Map Generation")

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

increStep = (float)(0.1)
incrRes = (int)(1)

heatMapGrid = generate_grid(lonMin, lonMax, latMin, latMax, increStep, incrRes)

boundaryArray = heatMapGrid[2]
horizontalAxis = heatMapGrid[0]
verticalAxis = heatMapGrid[1]

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
		print("Done Computing")
		print(i)
	opFile = "/home/jcharla/LiporLab/Conan/YearlyHM.npy"
	np.save(opFile, npHeatMap)

fileList = ["/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_01_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_02_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_03_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_04_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_05_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_06_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_07_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_08_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_09_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_10_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_11_LAP_DrSorted.csv" \
			,"/home/jcharla/LiporLab/Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_12_LAP_DrSorted.csv" \
			]

yearlyDF = pd.DataFrame()

for file in fileList:
	tempData,_ = aISDM.load_data_from_csv(file)
	yearlyDF = yearlyDF.append(tempData, ignore_index = True)

compute_heat_map(yearlyDF)