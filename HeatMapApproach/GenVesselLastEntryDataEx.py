import sys
sys.path.insert(0, '../Common/')

import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import HMUtils as hMUtil
import TimeUtils as timeUtils

import pandas as pd
import datetime

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

print("Generating Last Entry Files")

runInParallel = 1

#number of CPU cores to be used
numCores = multiprocessing.cpu_count()
print("Number of available cores = %d"%(numCores))
numCores = 8
print("Using %d cores"%(numCores))    

sourceDir = (config['GEN_VESSEL_LAST_ENTRY_DATA']['SRC_DIR'])
destDir = (config['GEN_VESSEL_LAST_ENTRY_DATA']['DEST_DIR'])
mMSIListFile = (config['GEN_VESSEL_LAST_ENTRY_DATA']['MMSI_LIST'])
#read the MMSI data

print(sourceDir)
print(destDir)
minuteInterval = 30

#time interval data 
#useful for indexing
timeIntvlText = "../Data/TimeInterval/HalfHourIntvl1701To1801_00.txt"
timeWindow = [line.rstrip('\n') for line in open(timeIntvlText)]

#1 minute slots to augment the data
timeIntvlTextList = [\
                    "../Data/TimeInterval/HalfHourIntvl1701To1801_00.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_01.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_02.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_03.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_04.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_05.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_06.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_07.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_08.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_09.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_10.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_11.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_12.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_13.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_14.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_15.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_16.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_17.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_18.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_19.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_20.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_21.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_22.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_23.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_24.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_25.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_26.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_27.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_28.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1701To1801_29.txt"\
                    ]

timeWindowList = []
for file in timeIntvlTextList:
    timeWindowList.append([line.rstrip('\n') for line in open(file)])

mMSIList = [line.rstrip('\n') for line in open(mMSIListFile)]
fileStoreCounter = 0

def convert_to_seconds(timeDel):
    return datetime.timedelta.total_seconds(timeDel)

def get_lower_time(timeStamp):
    timeStampStr = str(timeStamp)
    # print(timeStampStr)
    yYMMDD = timeStampStr.split(' ')[0]
    hHMMSS = timeStampStr.split(' ')[1]
    # print(yYMMDD)
    # print(hHMMSS)
    yY = int(yYMMDD.split('-')[0])
    monMon = int(yYMMDD.split('-')[1])
    dD = int(yYMMDD.split('-')[2])

    hH = int(hHMMSS.split(':')[0])
    mM = hHMMSS.split(':')[1]
    minMin = (int(mM) // 30)*30
    # print(minMin)

    startTime = datetime.datetime(yY, monMon, dD, hH, minMin, 0)
    nextTime = startTime + datetime.timedelta(minutes=30)
    ret = str(startTime) + ',' + str(nextTime)
    # print(ret)
    return ret

def gen_last_entry_data(vesselName,start,end):
    global fileStoreCounter
    sourceFile = sourceDir + vesselName + '_Sorted.csv'
    sourceDF, retVal = aISDM.load_data_from_csv(sourceFile)

    for tWin in timeWindowList:
        oneVesselLastData = pd.DataFrame()
        #based on time stamps 
        for timeWinIdx in range(start,end):
            timeSlot = tWin[timeWinIdx]
            temp = timeSlot.split(',')
            startTime = temp[0]
            endTime = temp[1]

            timelyDF = aISDM.filter_based_on_time_stamp(sourceDF,'DateTime',startTime,endTime)
            oneVesselRows = timelyDF.shape[0]
            
            invertedTimelyDF = aISDM.inver_df(timelyDF)
            invertedTimelyDF = invertedTimelyDF.drop_duplicates(subset="MMSI")
            
            oneVesselLastData = oneVesselLastData.append(invertedTimelyDF, ignore_index = True)
        # opFile = sourceDir + vesselName + '_SortedLE.csv'
        opFile = destDir + str(fileStoreCounter) + '.csv'
        fileStoreCounter = fileStoreCounter + 1
        aISDM.save_data_to_csv(oneVesselLastData,opFile)

def get_sequence_data_frame(vesselName):
    #read the data
    sourceFile = sourceDir + vesselName + '_Sorted.csv'
    sourceDF, retVal = aISDM.load_data_from_csv(sourceFile)
    # print(sourceDF)
    # print(sourceDF.dtypes)
    #formate the date time
    sourceDFFT = aISDM.formate_time(sourceDF,'DateTime')
    # print(sourceDFFT)
    # print(sourceDFFT.dtypes)
    if(sourceDFFT.shape[0] < 2):
        return []
        
    sourceDFFT = sourceDFFT.reset_index(drop=True)
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
    #last element of series
    dateTimeSeriesNextLE = dateTimeSeries.iloc[-1] + datetime.timedelta(minutes=minuteInterval)
    # print(dateTimeSeries.iloc[-1])
    # print(dateTimeSeriesNextLE)
    dateTimeSeriesNext = dateTimeSeriesNext.append(pd.Series(dateTimeSeriesNextLE),ignore_index = True)
    dateTimeSeriesNext.reset_index(drop = True)
    sourceDFFT['DateTimeNext'] = dateTimeSeriesNext
    # print(sourceDFFT)
    # print(sourceDFFT.dtypes)
    sourceDFFT['TimeDiff'] = (sourceDFFT['DateTimeNext'] - sourceDFFT['DateTime']).apply(convert_to_seconds)
    # print(sourceDFFT)
    # print(sourceDFFT.dtypes)
    slicIdx = sourceDFFT[(sourceDFFT['TimeDiff'] > 3600)].index.tolist()
    print(slicIdx)
    if(len(slicIdx) > 0):
        firstIndex = 0
        for i in range(0,len(slicIdx)):
            # print(firstIndex, slicIdx[i]+1)
            ret = sourceDFFT.iloc[firstIndex:slicIdx[i]+1,:].copy()
            print(ret.shape)
            timeIDX = ret.columns.get_loc("DateTime")
            lowerTimeWin = get_lower_time(ret.iloc[0,timeIDX])
            upperTimeWin = get_lower_time(ret.iloc[-1,timeIDX])
            lowerTimeWinIdx = timeWindow.index(lowerTimeWin)
            upperTimeWinIdx = timeWindow.index(upperTimeWin) + 1
            if(upperTimeWinIdx >= len(timeWindow)):
                upperTimeWinIdx = timeWindow.index(upperTimeWin)

            gen_last_entry_data(vesselName,lowerTimeWinIdx,upperTimeWinIdx)
            firstIndex = slicIdx[i]+1
        firstIndex = slicIdx[-1]+1
        ret = sourceDFFT.iloc[firstIndex:,:].copy()
        print(ret.shape)
        timeIDX = ret.columns.get_loc("DateTime")
        lowerTimeWin = get_lower_time(ret.iloc[0,timeIDX])
        upperTimeWin = get_lower_time(ret.iloc[-1,timeIDX])
        lowerTimeWinIdx = timeWindow.index(lowerTimeWin)
        upperTimeWinIdx = timeWindow.index(upperTimeWin) + 1
        if(upperTimeWinIdx >= len(timeWindow)):
            upperTimeWinIdx = timeWindow.index(upperTimeWin)

        gen_last_entry_data(vesselName,lowerTimeWinIdx,upperTimeWinIdx)
            
    #its all part of one sequence
    else:
        ret = sourceDFFT.copy()
        print(ret.shape)
        timeIDX = ret.columns.get_loc("DateTime")
        lowerTimeWin = get_lower_time(ret.iloc[0,timeIDX])
        upperTimeWin = get_lower_time(ret.iloc[-1,timeIDX])
        lowerTimeWinIdx = timeWindow.index(lowerTimeWin)
        upperTimeWinIdx = timeWindow.index(upperTimeWin) + 1
        if(upperTimeWinIdx >= len(timeWindow)):
            upperTimeWinIdx = timeWindow.index(upperTimeWin)

        gen_last_entry_data(vesselName,lowerTimeWinIdx,upperTimeWinIdx)

# get_sequence_data_frame('209251000')
for name in mMSIList:
    get_sequence_data_frame(name)

print(fileStoreCounter)