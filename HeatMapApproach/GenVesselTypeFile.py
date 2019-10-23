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

srcDir = (config['GEN_VESSEL_TYPE']['SOURCE_DIR'])
mMSIFile = (config['GEN_VESSEL_TYPE']['MMSI_FILE'])
destFile = (config['GEN_VESSEL_TYPE']['DEST_FILE'])

#open list of MMSI file
#and put it into list
mMSIList = [line.rstrip('\n') for line in open(mMSIFile)]

vesselTypeDF = pd.DataFrame(columns=['MMSI','VesselType'])

for vesselName in mMSIList:
	#get the file name
	fileName = srcDir + vesselName + "_Sorted.csv"
	#load the data of one particular vessel
	mMSIDF,_ = aISDM.load_data_from_csv(fileName)
	#get the index of type
	typeIDX = mMSIDF.columns.get_loc("VesselType")
	#now append the MMSI and type in data farme
	vesselType = mMSIDF.iloc[0,typeIDX]
	print(vesselType)

	#https://thispointer.com/pandas-how-to-create-an-empty-dataframe-and-append-rows-columns-to-it-in-python/
	vesselTypeDF = vesselTypeDF.append({'MMSI':vesselName \
									,'VesselType':vesselType}
									, ignore_index= True)


#save the information
#further can be edited manuall
aISDM.save_data_to_csv(vesselTypeDF, destFile)
