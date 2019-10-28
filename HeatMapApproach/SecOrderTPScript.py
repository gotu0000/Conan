import sys
import os
import numpy as np
import pandas as pd
import scipy.sparse
from scipy.sparse import csc_matrix
from scipy.sparse import lil_matrix
import pickle

#config parser
import configparser

sys.path.insert(0, '../Common/')
from AISDataManager import AISDataManager
import Constants as c
import HMUtils as hMUtil
import TimeUtils as timeUtils
import GeoCompute as gC

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing
aISDM = AISDataManager()
numCores = multiprocessing.cpu_count()

lonMin = (float)(config['TP_SEC_ORDER']['LON_MIN'])
lonMax = (float)(config['TP_SEC_ORDER']['LON_MAX'])

latMin = (float)(config['TP_SEC_ORDER']['LAT_MIN'])
latMax = (float)(config['TP_SEC_ORDER']['LAT_MAX'])

print(lonMin,latMin)
print(lonMax,latMax)

increStep = (float)(config['TP_SEC_ORDER']['INCR_STEP'])
incrRes = (int)(config['TP_SEC_ORDER']['INCR_RES'])

fileDir = config['TP_SEC_ORDER']['SOURCE_DIR']
dirToStore = config['TP_SEC_ORDER']['DEST_DIR']

print("SOURCE_DIR = %s"%fileDir)
print("DEST_DIR = %s"%dirToStore)

heatMapGrid = hMUtil.generate_grid(lonMin, lonMax, latMin, latMax, increStep, incrRes)

boundaryArray = heatMapGrid[2]
horizontalAxis = heatMapGrid[0]
verticalAxis = heatMapGrid[1]
totalStates = horizontalAxis.shape[0] * verticalAxis.shape[0]
numpyStyle = 0

tPM = lil_matrix((totalStates*totalStates,totalStates))
print(tPM.shape)
fileToRead = dirToStore + 'SumCount.pickle'
with open(fileToRead, 'rb') as handle:
    sumCount = pickle.load(handle)


tempArrayList = []
for i in range(totalStates):
    fileToRead = dirToStore + str(i) + '.pickle'
    with open(fileToRead, 'rb') as handle:
        tempArrayList.append(pickle.load(handle))

def get_value_from_dict_data(row,col):
    if row in tempArrayList[col].keys():
        ret = tempArrayList[col][row]/sumCount[row]
        return ret
    else:
        return 0

for i in range(tPM.shape[0]):
    if(i in sumCount.keys()):
        for j in range(tPM.shape[1]):
            tempRet = get_value_from_dict_data(i,j)
            tPM[i,j] = tempRet
    # else:
    #     tPM[i,(i % totalStates)] = 1

#convert into column representation
tPM = tPM.tocsc()

fileToWrite = dirToStore + 'TPM.npz'
scipy.sparse.save_npz(fileToWrite, tPM)