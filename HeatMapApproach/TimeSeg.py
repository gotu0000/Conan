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

FILE_SUFFIX = (config['TIME_SEG']['FILE_SUFFIX'])
SOURCE_DIR_NAME = (config['TIME_SEG']['SOURCE_DIR_NAME'])
DEST_DIR = (config['TIME_SEG']['DEST_DIR'])

fileNameList = ["../Data/"+SOURCE_DIR_NAME+"/17_01_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_02_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_03_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_04_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_05_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_06_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_07_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_08_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_09_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_10_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_11_Dr_Sort_"+FILE_SUFFIX+".csv"\
                ,"../Data/"+SOURCE_DIR_NAME+"/17_12_Dr_Sort_"+FILE_SUFFIX+".csv"\
               ]

timeSuffix = (config['TIME_SEG']['TIME_SUFFIX'])

timeIntervalList = ["../Data/TimeInterval/HalfHourIntvl1701To1702_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1702To1703_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1703To1704_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1704To1705_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1705To1706_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1706To1707_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1707To1708_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1708To1709_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1709To1710_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1710To1711_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1711To1712_"+timeSuffix+".txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1712To1801_"+timeSuffix+".txt"\
                    ]


#destination directory 
#where files will be saved
filePathToStore = DEST_DIR+"/HalfHr"+timeSuffix+"/"

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