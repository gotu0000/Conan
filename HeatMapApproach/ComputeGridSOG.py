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

config = configparser.ConfigParser()
config.read('../MyConfig.INI')

aISDM = AISDataManager()

lonMin = (float)(config['COMPUTE_AVG_SOG']['LON_MIN'])
lonMax = (float)(config['COMPUTE_AVG_SOG']['LON_MAX'])

latMin = (float)(config['COMPUTE_AVG_SOG']['LAT_MIN'])
latMax = (float)(config['COMPUTE_AVG_SOG']['LAT_MAX'])

print("(lonMin , latMin) = (%f,%f)"%(lonMin,latMin))
print("(lonMax , latMax) = (%f,%f)"%(lonMax,latMax))

print("Starting Grid based SOG computation")

increStep = (float)(config['COMPUTE_AVG_SOG']['INCR_STEP'])
incrRes = (int)(config['COMPUTE_AVG_SOG']['INCR_RES'])
fileSuffix = (config['COMPUTE_AVG_SOG']['FILE_SUFFIX'])

opFile = (config['COMPUTE_AVG_SOG']['OUTPUT_FILE'])
opFileVar = (config['COMPUTE_AVG_SOG']['VAR_OUTPUT_FILE'])
opFileMedian = (config['COMPUTE_AVG_SOG']['MEDIAN_OUTPUT_FILE'])
opFileMin = (config['COMPUTE_AVG_SOG']['MIN_OUTPUT_FILE'])
opFileMax = (config['COMPUTE_AVG_SOG']['MAX_OUTPUT_FILE'])

yearsToConsider = [int(year) for year in (config['COMPUTE_AVG_SOG']['YEARS_TO_CONSIDER'].split(','))]

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
    # for monthNum in monthToConsider:
        fileName = "../Data/"+SOURCE_DIR+"/"+"%02d"%(year)+"_"+"%02d"%(monthNum)+fileSuffix+".csv"
        fileNameList.append(fileName)

print(fileNameList)

sOGDF = pd.DataFrame()

def compute_avg_sog(localDf):
	npSOG = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	npSOGVar = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	npSOGMedian = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	npSOGMin = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	npSOGMax = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	for i in range(len(boundaryArray)):
		boundedDF = aISDM.filter_based_on_lon_lat(localDf,boundaryArray[i][0]\
													,boundaryArray[i][1]\
													,boundaryArray[i][2]\
													,boundaryArray[i][3]\
													)
		if(boundedDF.shape[0] > 0):
			npSOG[i] = boundedDF['SOG'].mean()
			npSOGVar[i] = boundedDF['SOG'].var()
			npSOGMedian[i] = boundedDF['SOG'].median()
			npSOGMin[i] = boundedDF['SOG'].min()
			npSOGMax[i] = boundedDF['SOG'].max()
			print(npSOG[i])
			print(npSOGVar[i])
		print("Done Computing %d"%(i))
	np.save(opFile, npSOG)
	np.save(opFileVar, npSOGVar)
	np.save(opFileMedian, npSOGMedian)
	np.save(opFileMin, npSOGMin)
	np.save(opFileMax, npSOGMax)

for file in fileNameList:
    tempData,_ = aISDM.load_data_from_csv(file)
    if('DateTime' in list(tempData.columns)):
        tempData = tempData.drop(columns = ['MMSI', 'BaseDateTime', 'DateTime', 'TypeBool'])
    else:
        tempData = tempData.drop(columns = ['MMSI', 'BaseDateTime', 'TypeBool'])
    sOGDF = sOGDF.append(tempData, ignore_index = True)

compute_avg_sog(sOGDF)
print("Done Computing Average SOG")