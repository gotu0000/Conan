import sys
sys.path.insert(0, '../Common/')

import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd

import os

#config parser
import configparser

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
# config.read('/home/jcharla/LiporLab/Conan/MyConfig.INI')
config.read('../MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

# ipDir = "../Data/AIS/LAPort/Hourly/"
# opDir = "../Data/AIS/LAPort/DailyInterval/"

# ipDir = "../Data/AIS_0117_0317_30_M124_35_M118/Hourly/"
# opDir = "../Data/AIS_0117_0317_30_M124_35_M118/DailyInterval/"

ipDir = "../Data/AIS_0117_0317_31_M120_345_M117/Hourly/"
opDir = "../Data/AIS_0117_0317_31_M120_345_M117/DailyIntvl/"

monToTue = np.arange(24*0,2160,step=24*7)
tueToWed = np.arange(24*1,2160,step=24*7)
wedToThurs = np.arange((24*2),2160,step=24*7)
thursToFri = np.arange((24*3),2160,step=24*7)
friToSat = np.arange((24*4),2160,step=24*7)
satToSun = np.arange((24*5),2160,step=24*7)
sunToMon = np.arange((24*6),2160,step=24*7)

startIndxArrayList = [monToTue \
				,tueToWed \
				,wedToThurs \
				,thursToFri \
				,friToSat \
				,satToSun \
				,sunToMon \
				]

intvlList = []
for startIndexArray in startIndxArrayList: 
	hrArray = []
	for startIndx in range(startIndexArray.shape[0]):
		start = startIndexArray[startIndx]
		for hrCount in range(24):
			hrArray.append(start+hrCount)
	# print(hrArray)
	intvlList.append(hrArray)


fileCounter = 0
for intvl in intvlList:
	#empty df in which we will append
	opDF = pd.DataFrame()
	# for fileNum in range(intvl.shape[0]):
	for fileNum in range(len(intvl)):
		# print(intvl[fileNum])
		fileNameToRead = ipDir + str(intvl[fileNum]) + '.csv'
		print(fileNameToRead)

		
		#load the hourly file
		hRData,retVal = aISDM.load_data_from_csv(fileNameToRead)
		if(retVal == c.errNO['SUCCESS']):
			#keep on appending
			opDF = opDF.append(hRData, ignore_index = True)	
		else:
			print("could not load the file")
			break
		
	print("**********")

	fileToWr = opDir + str(fileCounter) + '.csv' 
	fileCounter = fileCounter + 1
	print(fileToWr)

	aISDM.save_data_to_csv(opDF,fileToWr)

	print("###########")