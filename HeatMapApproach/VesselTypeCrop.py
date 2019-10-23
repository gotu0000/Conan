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

from joblib import Parallel, delayed
import multiprocessing

aISDM = AISDataManager()
numCores = multiprocessing.cpu_count()

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

mMSITypeFile = (config['VESSEL_TYPE_CROP']['MMSI_TYPE_FILE'])
mMSITypeDestFile = (config['VESSEL_TYPE_CROP']['MMSI_TYPE_DEST_FILE'])

print(mMSITypeFile)
print(mMSITypeDestFile)

allowedTypes = [1004.0, 1024.0]

#load original vessel type
mMSITypeDF,_ = aISDM.load_data_from_csv(mMSITypeFile)
vesselTypeCrDF = pd.DataFrame()
typeCounter = 0
print(mMSITypeDF.shape)
for i in range(mMSITypeDF.shape[0]):
	# print(mMSITypeDF.iloc[i,1])
	currType = mMSITypeDF.iloc[i,1]
	currVessel = mMSITypeDF.iloc[i,0]
	if(currType in allowedTypes):
		vesselTypeCrDF = vesselTypeCrDF.append(mMSITypeDF.iloc[i,:], ignore_index = True)
		typeCounter = typeCounter + 1

print(vesselTypeCrDF.shape)
aISDM.save_data_to_csv(vesselTypeCrDF, mMSITypeDestFile)