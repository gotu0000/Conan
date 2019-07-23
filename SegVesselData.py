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

fileNameList = ["./Data/AIS_2017_LA/LAPort/AIS_2015_01_LAP.csv"
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_02_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_03_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_04_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_05_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_06_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_07_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_08_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_09_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_10_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_11_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_12_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_01_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_02_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_03_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_04_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_05_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_06_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_07_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_08_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_09_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_10_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_11_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_12_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_01_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_02_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_03_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_04_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_05_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_06_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_07_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_08_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_09_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_10_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_11_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_12_LAP.csv"\
               ]

dirToStore = ["./Data/AIS_2017_LA/MMSI/2015_01/"\
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

combinedList = []

for i in range(len(fileNameList)):
	combinedList.append([fileNameList[i], dirToStore[i]])	

mMSIList = [line.rstrip('\n') for line in open('MMSIList_15_17.txt')]
# mMSIList = [line.rstrip('\n') for line in open('MMSIListTest.txt')]

numCores = multiprocessing.cpu_count()
print(numCores)

def segregate_vessel_data(cSVFile, opDirectory):
	#read the CSV file
	data, retVal = aISDM.load_data_from_csv(cSVFile)
	if(retVal == c.errNO['SUCCESS']):
		for vesselName in mMSIList:

			tempDF = pd.DataFrame()

			#filter based on MMSI
			vesselData = aISDM.filter_based_on_mmsi(data, int(vesselName))

			#get the inidividual vessel data
			tempDF = tempDF.append(vesselData, ignore_index = True)

			#get the name 
			fileName = opDirectory + vesselName + '.csv'

			print(fileName)
			aISDM.save_data_to_csv(tempDF,fileName)
	else:
		print("Error in Loading")

# Parallel(n_jobs=numCores, verbose=10)(delayed(segregate_vessel_data)(ipOP[0], ipOP[1]) for ipOP in combinedList)

for ipOP in combinedList:
	segregate_vessel_data(ipOP[0], ipOP[1])