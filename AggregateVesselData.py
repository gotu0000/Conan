import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd

import os

import configparser

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

dirToRead = ["./Data/AIS_2017_LA/MMSI/2015_01/"\
				,"./Data/AIS_2017_LA/MMSI/2015_02/"\
				,"./Data/AIS_2017_LA/MMSI/2015_03/"\
				,"./Data/AIS_2017_LA/MMSI/2015_04/"\
				,"./Data/AIS_2017_LA/MMSI/2015_05/"\
				,"./Data/AIS_2017_LA/MMSI/2015_06/"\
				,"./Data/AIS_2017_LA/MMSI/2015_07/"\
				,"./Data/AIS_2017_LA/MMSI/2015_08/"\
				,"./Data/AIS_2017_LA/MMSI/2015_09/"\
				,"./Data/AIS_2017_LA/MMSI/2015_10/"\
				,"./Data/AIS_2017_LA/MMSI/2015_11/"\
				,"./Data/AIS_2017_LA/MMSI/2015_12/"\
				,"./Data/AIS_2017_LA/MMSI/2016_01/"\
				,"./Data/AIS_2017_LA/MMSI/2016_02/"\
				,"./Data/AIS_2017_LA/MMSI/2016_03/"\
				,"./Data/AIS_2017_LA/MMSI/2016_04/"\
				,"./Data/AIS_2017_LA/MMSI/2016_05/"\
				,"./Data/AIS_2017_LA/MMSI/2016_06/"\
				,"./Data/AIS_2017_LA/MMSI/2016_07/"\
				,"./Data/AIS_2017_LA/MMSI/2016_08/"\
				,"./Data/AIS_2017_LA/MMSI/2016_09/"\
				,"./Data/AIS_2017_LA/MMSI/2016_10/"\
				,"./Data/AIS_2017_LA/MMSI/2016_11/"\
				,"./Data/AIS_2017_LA/MMSI/2016_12/"\
				,"./Data/AIS_2017_LA/MMSI/2017_01/"\
				,"./Data/AIS_2017_LA/MMSI/2017_02/"\
				,"./Data/AIS_2017_LA/MMSI/2017_03/"\
				,"./Data/AIS_2017_LA/MMSI/2017_04/"\
				,"./Data/AIS_2017_LA/MMSI/2017_05/"\
				,"./Data/AIS_2017_LA/MMSI/2017_06/"\
				,"./Data/AIS_2017_LA/MMSI/2017_07/"\
				,"./Data/AIS_2017_LA/MMSI/2017_08/"\
				,"./Data/AIS_2017_LA/MMSI/2017_09/"\
				,"./Data/AIS_2017_LA/MMSI/2017_10/"\
				,"./Data/AIS_2017_LA/MMSI/2017_11/"\
				,"./Data/AIS_2017_LA/MMSI/2017_12/"\
				]


mMSIList = [line.rstrip('\n') for line in open('MMSIList_15_17.txt')]
# mMSIList = [line.rstrip('\n') for line in open('MMSIListTest.txt')]

opDir = "./Data/AIS_2017_LA/MMSI/Accumulated/"

def aggregate_vessel_data(vesselName):
	#based on vessel name open the file
	#iterate through every directory

	#initalise empty data farme
	tempDF = pd.DataFrame()
	for segDir in dirToRead:
		#generate name of CSV file
		fileToRead = segDir + vesselName + '.csv'
		data, retVal = aISDM.load_data_from_csv(fileToRead)

		if(retVal == c.errNO['SUCCESS']):
			tempDF = tempDF.append(data, ignore_index = True)
		else:
			print("Error in Loading")
			break
	#now lets store the file
	fileToStore = opDir + vesselName + '.csv'
	print(fileToStore)
	aISDM.save_data_to_csv(tempDF, fileToStore)
	#also sort the data
	sortedTempDF = aISDM.format_time(tempDF,'DateTime')
	sortedTempDF = sortedTempDF.sort_values(by='DateTime')
	fileToStore = opDir + vesselName + '_Sorted.csv'
	print(fileToStore)
	aISDM.save_data_to_csv(sortedTempDF, fileToStore)

numCores = multiprocessing.cpu_count()
print(numCores)

Parallel(n_jobs=numCores, verbose=10)(delayed(aggregate_vessel_data)(name) for name in mMSIList)