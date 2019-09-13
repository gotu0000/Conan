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
# opDir = "../Data/AIS/LAPort/HourlyInterval/"

# ipDir = "../Data/AIS_0117_0317_30_M124_35_M118/Hourly/"
# opDir = "../Data/AIS_0117_0317_30_M124_35_M118/HourlyInterval/"

ipDir = "../Data/AIS_0117_0317_31_M120_345_M117/Hourly/"
opDir = "../Data/AIS_0117_0317_31_M120_345_M117/HourlyIntvl/"

zeroToOne = np.arange(0,2160,step=24)
oneToTwo = np.arange(1,2160,step=24)
twoToThree = np.arange(2,2160,step=24)
threeToFour = np.arange(3,2160,step=24)
fourToFive = np.arange(4,2160,step=24)
fiveToSix = np.arange(5,2160,step=24)
sixToSeven = np.arange(6,2160,step=24)
sevenToEight = np.arange(7,2160,step=24)
eightToNine = np.arange(8,2160,step=24)
nineToTen = np.arange(9,2160,step=24)
tenToEleven = np.arange(10,2160,step=24)
elvenToTwelve = np.arange(11,2160,step=24)
twelveToThirteen = np.arange(12,2160,step=24)
thirteenToFourteen = np.arange(13,2160,step=24)
fourteenToFifteen = np.arange(14,2160,step=24)
fifteenToSixteen = np.arange(15,2160,step=24)
sixteenToSeventeen = np.arange(16,2160,step=24)
seventeenToEighteen = np.arange(17,2160,step=24)
eighteenToNineteen = np.arange(18,2160,step=24)
nineteenToTwenty = np.arange(19,2160,step=24)
twentyToTwentyOne = np.arange(20,2160,step=24)
twentyOneToTwentyTwo = np.arange(21,2160,step=24)
twentyTwoToTwentyThree = np.arange(22,2160,step=24)
thwentyThreeToTwentyFour = np.arange(23,2160,step=24)

intvlList = [zeroToOne \
			,oneToTwo \
			,twoToThree \
			,threeToFour \
			,fourToFive \
			,fiveToSix \
			,sixToSeven \
			,sevenToEight \
			,eightToNine \
			,nineToTen \
			,tenToEleven \
			,elvenToTwelve \
			,twelveToThirteen \
			,thirteenToFourteen \
			,fourteenToFifteen \
			,fifteenToSixteen \
			,sixteenToSeventeen \
			,seventeenToEighteen \
			,eighteenToNineteen \
			,nineteenToTwenty \
			,twentyToTwentyOne \
			,twentyOneToTwentyTwo \
			,twentyTwoToTwentyThree \
			,thwentyThreeToTwentyFour \
		]

fileCounter = 0
for intvl in intvlList:
	#empty df in which we will append
	opDF = pd.DataFrame()
	for fileNum in range(intvl.shape[0]):
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