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

mMSITypeFile = (config['GEN_VESSEL_LIST_OF_TYPE_FROM_RAW_TYPE']['MMSI_TYPE_FILE'])
mMSITypeDestFile = (config['GEN_VESSEL_LIST_OF_TYPE_FROM_RAW_TYPE']['MMSI_SPEC_TYPE_DEST_FILE'])
allowedType = (config['GEN_VESSEL_LIST_OF_TYPE_FROM_RAW_TYPE']['DESIRED_TYPE']).split(',')

print(mMSITypeFile)
print(mMSITypeDestFile)
print(allowedType)
mMSITypeDF,_ = aISDM.load_data_from_csv(mMSITypeFile)
vesselTypeCounter = 0

#empty list for desired type
desiredType = []

#iterate through every row
for i in range(mMSITypeDF.shape[0]):
	#get MMSI
	currVessel = mMSITypeDF.iloc[i,0]
	currType = mMSITypeDF.iloc[i,1]
	#get type
	# print(currType)
	# print(type(currType))
	# convert in into string for comparision
	currTypeStr = str(currType)
	# print(currTypeStr)
	# print(type(currTypeStr))
	#if found match
	if(currTypeStr in allowedType):
		#append the MMSI
		desiredType.append(currVessel)
		vesselTypeCounter = vesselTypeCounter + 1
	
print(vesselTypeCounter)
#save to file 
with open(mMSITypeDestFile, 'w') as f:
    for mMSI in desiredType:
        f.write("%s\n" % mMSI)