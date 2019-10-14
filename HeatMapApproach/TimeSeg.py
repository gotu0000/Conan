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
config.read('../MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

print("Starting Time Based Data Segregation")

runInParallel = 1

#list for parallel execution
parallelDFList = []

#number of CPU cores to be used
numCores = multiprocessing.cpu_count()
print("Number of available cores = %d"%(numCores))
numCores = 4
print("Using %d cores"%(numCores))

#for serial segregation
serialTempDF = pd.DataFrame()

#make empty data frames
for i in range(numCores):
    parallelDFList.append(pd.DataFrame())    

#list of CSVs from which to load
#works on whole data set 
#we have monthly based data sorted in time
#also few of the columns also have been dropped
#for faster implementation
fileNameList = ["../Data/M119_50_M119_00_34_00_34_16/17_01_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_02_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_03_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_04_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_05_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_06_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_07_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_08_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_09_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_10_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_11_Dropped_Sorted_Tanker.csv"\
                ,"../Data/M119_50_M119_00_34_00_34_16/17_12_Dropped_Sorted_Tanker.csv"\
               ]

timeIntervalList = ["../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1701To1702.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1702To1703.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1703To1704.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1704To1705.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1705To1706.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1706To1707.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1707To1708.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1708To1709.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1709To1710.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1710To1711.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1711To1712.txt"\
                    ,"../Data/M119_50_M119_00_34_00_34_16/TimeInterval/HalfHourIntvl1712To1801.txt"\
                    ]

#destination directory 
#where files will be saved
filePathToStore = "../Data/M119_50_M119_00_34_00_34_16/HalfHrTanker/"

def serial_time_segregation(timeIntvl, number):
    temp = timeIntvl.split(',')
    startTime = temp[0]
    endTime = temp[1]

    timelyDF = aISDM.filter_based_on_time_stamp_without_copy(serialTempDF,'DateTime',startTime,endTime)
    tempFilePathToStore = filePathToStore+str(number)+'.csv'

    print(tempFilePathToStore)
    aISDM.save_data_to_csv(timelyDF,tempFilePathToStore)

def parallel_time_segregation(timeIntvl, number, offset):
    dFtoUse = (offset + number) % numCores
    print(dFtoUse)

    temp = timeIntvl.split(',')
    startTime = temp[0]
    endTime = temp[1]

    timelyDF = aISDM.filter_based_on_time_stamp_without_copy(parallelDFList[dFtoUse],'DateTime',startTime,endTime)
    tempFilePathToStore = filePathToStore+str(offset + number)+'.csv'
    print(tempFilePathToStore)

    aISDM.save_data_to_csv(timelyDF,tempFilePathToStore)

if(runInParallel == 0):
    print("Running in Serial")
    #iterate through all the files
    #usually monthly file
    #and start segregating them one by one
    fileWriteCounter = 0;
    for i in range(0,len(fileNameList)):
        #load the file
        serialTempDF, retVal = aISDM.load_data_from_csv(fileNameList[i])
        serialTempDF = aISDM.formate_time(serialTempDF,'DateTime')
        if(retVal == c.errNO['SUCCESS']):
            #load the corresponding time intervals
            timeWindows = [line.rstrip('\n') for line in open(timeIntervalList[i])]
            for timeSlot in timeWindows:
                #FIXME check for out of bound
                serial_time_segregation(timeSlot,fileWriteCounter)
                fileWriteCounter = fileWriteCounter + 1
        else:
            print("Something wrong with the file")
            break
else:
    print("Running in parallel")
    #iterate through all the files
    #usually monthly file
    #and start segregating them one by one
    fileOffsetCounter = 0
    for i in range(0,len(fileNameList)):
        #load the file
        tempDF, retVal = aISDM.load_data_from_csv(fileNameList[i])
        print("Done Reading %s"%(fileNameList[i]))
        tempDF = aISDM.formate_time(tempDF,'DateTime')
        parallelDFList[0] = tempDF
        for parallelDFIndex in range(1,numCores):
            parallelDFList[parallelDFIndex] = tempDF.copy()


        #get the time stamps
        timeWindows = [line.rstrip('\n') for line in open(timeIntervalList[i])]
        # for timeSlotIndx in range(len(timeWindows)):
        #     parallel_time_segregation(timeWindows[timeSlotIndx] \
        #                     , timeSlotIndx \
        #                     )

        Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10)(delayed(parallel_time_segregation)(timeWindows[timeSlotIndx], timeSlotIndx, fileOffsetCounter) for timeSlotIndx in range(len(timeWindows)))
        fileOffsetCounter = fileOffsetCounter + len(timeWindows)

print("Done Segregating the data")