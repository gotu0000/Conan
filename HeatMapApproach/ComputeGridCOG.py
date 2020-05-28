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

lonMin = (float)(config['COMPUTE_AVG_COG']['LON_MIN'])
lonMax = (float)(config['COMPUTE_AVG_COG']['LON_MAX'])

latMin = (float)(config['COMPUTE_AVG_COG']['LAT_MIN'])
latMax = (float)(config['COMPUTE_AVG_COG']['LAT_MAX'])

print("(lonMin , latMin) = (%f,%f)"%(lonMin,latMin))
print("(lonMax , latMax) = (%f,%f)"%(lonMax,latMax))

print("Starting Grid based SOG computation")

increStep = (float)(config['COMPUTE_AVG_COG']['INCR_STEP'])
incrRes = (int)(config['COMPUTE_AVG_COG']['INCR_RES'])
fileSuffix = (config['COMPUTE_AVG_COG']['FILE_SUFFIX'])
opFile = (config['COMPUTE_AVG_COG']['OUTPUT_FILE'])
opFileVar = (config['COMPUTE_AVG_COG']['VAR_OUTPUT_FILE'])
opFileMin = (config['COMPUTE_AVG_COG']['MIN_OUTPUT_FILE'])
opFileMax = (config['COMPUTE_AVG_COG']['MAX_OUTPUT_FILE'])
opFileMedian = (config['COMPUTE_AVG_COG']['MEDIAN_OUTPUT_FILE'])

yearsToConsider = [int(year) for year in (config['COMPUTE_AVG_COG']['YEARS_TO_CONSIDER'].split(','))]

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

cOGDF = pd.DataFrame()

def compute_avg_cog(localDf):
	npCOG = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	npCOGVar = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	npCOGMin = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	npCOGMax = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	npCOGMedian = np.zeros((horizontalAxis.shape[0]*verticalAxis.shape[0]))
	for i in range(len(boundaryArray)):
		boundedDF = aISDM.filter_based_on_lon_lat(localDf,boundaryArray[i][0]\
													,boundaryArray[i][1]\
													,boundaryArray[i][2]\
													,boundaryArray[i][3]\
													)
		if(boundedDF.shape[0] > 0):
			npCOG[i] = boundedDF['COG'].mean()
			npCOGVar[i] = boundedDF['COG'].var()
			npCOGMin[i] = boundedDF['COG'].min()
			npCOGMax[i] = boundedDF['COG'].max()
			npCOGMedian[i] = boundedDF['COG'].median()
			print(npCOG[i])
			print(npCOGVar[i])
			print(npCOGMin[i])
			print(npCOGMax[i])
			print(npCOGMedian[i])
		print("Done Computing %d"%(i))
	np.save(opFile, npCOG)
	np.save(opFileVar, npCOGVar)
	np.save(opFileMin, npCOGMin)
	np.save(opFileMax, npCOGMax)
	np.save(opFileMedian, npCOGMedian)

for file in fileNameList:
    tempData,_ = aISDM.load_data_from_csv(file)
    if('DateTime' in list(tempData.columns)):
   	    tempData = tempData.drop(columns = ['MMSI', 'BaseDateTime', 'DateTime', 'TypeBool'])
    else:
   	    tempData = tempData.drop(columns = ['MMSI', 'BaseDateTime', 'TypeBool'])
    cOGDF = cOGDF.append(tempData, ignore_index = True)

compute_avg_cog(cOGDF)
print("Done Computing Average COG")