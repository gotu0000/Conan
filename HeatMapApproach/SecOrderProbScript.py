import sys
import os
import numpy as np
import pandas as pd
import pickle

import scipy.sparse
from scipy.sparse import csc_matrix
from scipy.sparse import lil_matrix
from scipy.sparse import coo_matrix

#config parser
import configparser

sys.path.insert(0, '../Common/')
from AISDataManager import AISDataManager
import Constants as c
import HMUtils as hMUtil
import TimeUtils as timeUtils

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing
aISDM = AISDataManager()
numCores = multiprocessing.cpu_count()

lonMin = (float)(config['TP_SEC_ORDER_SCRIPT']['LON_MIN'])
lonMax = (float)(config['TP_SEC_ORDER_SCRIPT']['LON_MAX'])

latMin = (float)(config['TP_SEC_ORDER_SCRIPT']['LAT_MIN'])
latMax = (float)(config['TP_SEC_ORDER_SCRIPT']['LAT_MAX'])

print(lonMin,latMin)
print(lonMax,latMax)

increStep = (float)(config['TP_SEC_ORDER_SCRIPT']['INCR_STEP'])
incrRes = (int)(config['TP_SEC_ORDER_SCRIPT']['INCR_RES'])

fileDir = config['TP_SEC_ORDER_SCRIPT']['SOURCE_DIR']
dirToStore = config['TP_SEC_ORDER_SCRIPT']['DEST_DIR']
trainData = (int)(config['TP_SEC_ORDER_SCRIPT']['TRAIN_NUMBER'])

#generate grid
heatMapGrid = hMUtil.generate_grid(lonMin, lonMax, latMin, latMax, increStep, incrRes)

boundaryArray = heatMapGrid[2]
horizontalAxis = heatMapGrid[0]
verticalAxis = heatMapGrid[1]
totalStates = horizontalAxis.shape[0] * verticalAxis.shape[0]

#lets make list of dictinary
#whose key will be corresponding to one of the row of state trantition matrix
#value will be count for that row in next one hour
neighTPCount = []
#for total 
for i in range(totalStates):
    neighTPCount.append({})


#get index from lon and lat position
#needs boundary array to get the index
def get_index_from_lon_lat(lon,lat):
    retVal = -1
    for boundary in boundaryArray: 
        if(lon >= boundary[0]) and (lon < boundary[1]) \
            and (lat >= boundary[2]) and (lat < boundary[3]):
            retVal = boundary[4]
            break 
    return retVal

def clear_tm_matrix():
    global neighTPCount
    for i in range(totalStates):
        neighTPCount[i] = {}
        
def update_transition_prob(fileNum):
	global neighTPCount
	#load the file
	fileName = fileDir + str(fileNum) + '.csv'
	print(fileName)
	#load the trajectory data
	trajDF,_ = aISDM.load_data_from_csv(fileName)
	#get indexes of LON and LAT
	lonIDX = trajDF.columns.get_loc("LON")
	latIDX = trajDF.columns.get_loc("LAT")
	#iterate through trajectory
	#second order thats why -2
	for row in range((trajDF.shape[0]-2)):
		# print(trajDF.iloc[row,lonIDX],trajDF.iloc[row,latIDX])
		#get previous state
		vesselPrevIndex = get_index_from_lon_lat(trajDF.iloc[row,lonIDX],trajDF.iloc[row,latIDX])
		if(vesselPrevIndex == -1):
			print("Something is wrong")
			break
		#get current state
		vesselCurrIndex = get_index_from_lon_lat(trajDF.iloc[row+1,lonIDX],trajDF.iloc[row+1,latIDX])
		if(vesselCurrIndex == -1):
			print("Something is wrong")
			break
		#get next state
		vesselNextIndex = get_index_from_lon_lat(trajDF.iloc[row+2,lonIDX],trajDF.iloc[row+2,latIDX])
		vesselPrevCurrIndex = (vesselPrevIndex * totalStates) + vesselCurrIndex

		#if prev,curr is in the dixtionary
		if(vesselPrevCurrIndex in neighTPCount[vesselNextIndex].keys()):
			neighTPCount[vesselNextIndex][vesselPrevCurrIndex] = \
				neighTPCount[vesselNextIndex][vesselPrevCurrIndex] + 1
		else:
			neighTPCount[vesselNextIndex].update({vesselPrevCurrIndex:1})

clear_tm_matrix()
for trajNum in range(trainData):
	update_transition_prob(trajNum)

#store everything in destination directory
for neighb in range(totalStates):
	opFile = dirToStore + str(neighb)+'.pickle'
	with open(opFile, 'wb') as handle:
		pickle.dump(neighTPCount[neighb], handle)


#find all the keys in the dictionary
#make separate dictionary of it
sumCount = {}
for neighb in range(totalStates):
	#iterate through keys of each dictionary
	for prevCurrent, count in neighTPCount[neighb].items():
		#check whether it exists for sumCount
		#this will help in creating union
		if(prevCurrent in sumCount.keys()):         
			pass
		else:
			sumCount.update({prevCurrent:0})

print(sumCount)
print(len(sumCount))

#now compute the actual values
for prevCurrent, vesselCount in sumCount.items():
	for neighb in range(totalStates):
		#check for the key in the current dictionary
		#if its there then add the value to that cell
		if prevCurrent in neighTPCount[neighb].keys():
			sumCount[prevCurrent] = sumCount[prevCurrent] + neighTPCount[neighb][prevCurrent]

print(sumCount)
print(len(sumCount))

# opFile = dirToStore +'SumCount_.pickle'
opFile = dirToStore +'SumCount.pickle'
with open(opFile, 'wb') as handle:
	pickle.dump(sumCount, handle)