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

mMSITypeFile = (config['GEN_VESSEL_LIST_OF_TYPE']['MMSI_TYPE_FILE'])
mMSITypeDestFile = (config['GEN_VESSEL_LIST_OF_TYPE']['MMSI_SPEC_DEST_FILE'])
allowedTypes = (config['GEN_VESSEL_LIST_OF_TYPE']['ALLOWED_TYPES']).split(',')

print(mMSITypeFile)
print(mMSITypeDestFile)
print(allowedTypes)

mMSITypeDF,_ = aISDM.load_data_from_csv(mMSITypeFile)
vesselTypeCounter = 0
desiredMMSI = []
for i in range(mMSITypeDF.shape[0]):
	currVessel = mMSITypeDF.iloc[i,0]
	currType = mMSITypeDF.iloc[i,1]
	currVesselSub = mMSITypeDF.iloc[i,2]
	if(currVesselSub in allowedTypes):
		desiredMMSI.append(currVessel)
		print(currVessel, currVesselSub)
		vesselTypeCounter = vesselTypeCounter + 1
print(vesselTypeCounter)


#save to file 
with open(mMSITypeDestFile, 'w') as f:
    for mMSI in desiredMMSI:
        f.write("%s\n" % mMSI)