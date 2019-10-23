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

mMSITypeFile = (config['UPDATE_TYPE_CARGO']['MMSI_TYPE_SRC_FILE'])
mMSITypeCmpFile = (config['UPDATE_TYPE_CARGO']['MMSI_TYPE_CMP_FILE'])

print(mMSITypeFile)
print(mMSITypeCmpFile)

mMSITypeDF,_ = aISDM.load_data_from_csv(mMSITypeFile)
mMSITypeDF['VesselTypeSpec'] = 'Not Container'

mMSITypeCmpDF,_ = aISDM.load_data_from_csv(mMSITypeCmpFile)
mMSITypeCmpDF = mMSITypeCmpDF.set_index('MMSI')

#index with MMSI
#easier to access the VesseleType
for i in range(mMSITypeDF.shape[0]):
	currVessel = mMSITypeDF.iloc[i,0]
	mMSITypeDF.iloc[i,2] = mMSITypeCmpDF.loc[currVessel,"VesselTypeSpec"]

aISDM.save_data_to_csv(mMSITypeDF, mMSITypeFile)