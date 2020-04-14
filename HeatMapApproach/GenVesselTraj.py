import sys
import os

import pandas as pd
import numpy as np
import datetime
import configparser

sys.path.insert(0, '../Common/')
from AISDataManager import AISDataManager
import Constants as c
import HMUtils as hMUtil
import TimeUtils as timeUtils

aISDM = AISDataManager()
MAX_TIME_INTERVAL_DIFF = (30*60)
MINIMUM_SHAPE = 150

def convert_to_seconds(timeDel):
	return datetime.timedelta.total_seconds(timeDel)

def seg_traj_data(sourceDir, vesselName, destDir):
	"""
	"""
	#read the data sorted data
	sourceFile = sourceDir + vesselName + '_Sorted.csv'
	sourceDF, retVal = aISDM.load_data_from_csv(sourceFile)
	# print(sourceDF)
	# print(sourceDF.dtypes)
	#formate the date time
	sourceDFFT = aISDM.formate_time(sourceDF,'DateTime')
	# print(sourceDFFT)

	#get rid of all the trajectories 
	#where it is not moving at all
	sourceDFFT = sourceDFFT[sourceDFFT['SOG'] > 2.0]
	# print(sourceDFFT)

	sourceDFFT = sourceDFFT.reset_index(drop=True)
	#Not too many instances
	if(sourceDFFT.shape[0] < 3):
		return -1
	#make copy of DateTime column
	#get the series of date time
	#remove first element
	#and append the time diff of time stamp
	#make it new column
	#compute diff
	dateTimeSeries = sourceDFFT['DateTime']
	# print(type(dateTimeSeries))
	# print(dateTimeSeries.dtypes)
	dateTimeSeriesNext = dateTimeSeries[1:].copy()
	dateTimeSeriesNext = dateTimeSeriesNext.reset_index(drop=True)
	dateTimeSeriesCurrent = dateTimeSeries[0:-1].copy()
	dateTimeSeriesCurrent = dateTimeSeriesCurrent.reset_index(drop=True)
	#last element of series
	dataeTimeDiff = (dateTimeSeriesNext - dateTimeSeriesCurrent)
	dataeTimeDiffSec = dataeTimeDiff.apply(convert_to_seconds) 
	# print(dataeTimeDiffSec.shape)
	slicIdx = dataeTimeDiffSec[(dataeTimeDiffSec > MAX_TIME_INTERVAL_DIFF)].index.tolist()
	# print(slicIdx)


	vesselTrajCounter = 0
	atleastOneFile = 0
	if(len(slicIdx) > 0):
		firstIndex = 0
		for i in range(0,len(slicIdx)):

			ret = sourceDFFT.iloc[firstIndex:slicIdx[i]+1,:].copy()
			ret = ret.reset_index(drop=True)
			print(ret.shape)
			if(ret.shape[0] > MINIMUM_SHAPE):
				opFile = destDir + vesselName + '_' + str(vesselTrajCounter) + '.csv'
				aISDM.save_data_to_csv(ret,opFile)
				vesselTrajCounter = vesselTrajCounter + 1
				atleastOneFile = 1

			firstIndex = slicIdx[i]+1

		firstIndex = slicIdx[-1]+1

		ret = sourceDFFT.iloc[firstIndex:,:].copy()
		ret = ret.reset_index(drop=True)
		print(ret.shape)
		if(ret.shape[0] > MINIMUM_SHAPE):
			opFile = destDir + vesselName + '_' + str(vesselTrajCounter) + '.csv'
			aISDM.save_data_to_csv(ret,opFile)
			vesselTrajCounter = vesselTrajCounter + 1
			atleastOneFile = 1

	#its all part of one sequence
	else:
		ret = sourceDFFT.copy()
		ret = ret.reset_index(drop=True)
		print(ret.shape)
		if(ret.shape[0] > MINIMUM_SHAPE):
			opFile = destDir + vesselName + '_' + str(vesselTrajCounter) + '.csv'
			aISDM.save_data_to_csv(ret,opFile)
			vesselTrajCounter = vesselTrajCounter + 1
			atleastOneFile = 1
	if(atleastOneFile == 1):
		return vesselTrajCounter
	else:
		return -1

        

def main():
	config = configparser.ConfigParser()
	config.read('../MyConfig.INI')

	print("Generating Vessel Trajectory")

	srcDir = (config['GEN_VESSEL_TRAJ']['SRC_DIR'])
	mMSIListFile = (config['GEN_VESSEL_TRAJ']['MMSI_FILE'])
	destDir = (config['GEN_VESSEL_TRAJ']['DEST_DIR'])
	print(srcDir)
	print(mMSIListFile)
	print(destDir)

	#Generate List from MMSI
	mMSIList = [line.rstrip('\n') for line in open(mMSIListFile)]
	#For testing purpose uncomment
	# mMSIList = [mMSIList[1]]
	vesselTrajCountList = []
	for mMSI in mMSIList:
		print(mMSI)
		trajCount = seg_traj_data(srcDir, mMSI, destDir)
		print(trajCount)
		if(trajCount > 0):
			vesselTrajCountStr = mMSI + '-' + str(trajCount)
			vesselTrajCountList.append(vesselTrajCountStr)

	#save to file 
	destFileName = destDir + 'VesselTrajCount.txt'
	with open(destFileName, 'w') as f:
	    for item in vesselTrajCountList:
	        f.write("%s\n" % item)

if __name__ == '__main__':
	main()