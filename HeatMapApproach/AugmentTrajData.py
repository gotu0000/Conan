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

sourceDir = (config['AUGMENT_TRAJ_DATA']['SRC_DIR'])
destDir = (config['AUGMENT_TRAJ_DATA']['DEST_DIR'])
mMSIListFile = (config['AUGMENT_TRAJ_DATA']['MMSI_LIST'])
#read the MMSI data

print(sourceDir)
print(destDir)

#time interval data 
#useful for indexing
#based on those indexes 30 different files will be made
timeIntvlText = "../Data/TimeInterval/HalfHourIntvl1501To1801_00.txt"
timeWindow = [line.rstrip('\n') for line in open(timeIntvlText)]
#1 minute slots to augment the data
timeIntvlTextList = [\
                    "../Data/TimeInterval/HalfHourIntvl1501To1801_00.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_02.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_04.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_06.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_08.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_10.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_12.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_14.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_16.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_18.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_20.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_22.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_24.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_26.txt"\
                    ,"../Data/TimeInterval/HalfHourIntvl1501To1801_28.txt"\
                    ]

#list of time interval lists
timeWindowList = []
for file in timeIntvlTextList:
    timeWindowList.append([line.rstrip('\n') for line in open(file)])
mMSIList = [line.rstrip('\n') for line in open(mMSIListFile)]


def convert_to_seconds(timeDel):
    return datetime.timedelta.total_seconds(timeDel)

#get time stamp where minutes are multiple of 30
#and seconds are 0
#returns interval 
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

fileStoreCounter = 0
def gen_last_entry_data(sourceDF,start,end):
    global fileStoreCounter

    #now for every list in timewindow list
    #30 in this case
    #we will make 30 data frames of vessel trajectories
    #separated by interval of 1 minute
    for tWin in timeWindowList:
        #initialise empty data frame
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

        if(oneVesselLastData.shape[0] > 3):
            opFile = destDir + str(fileStoreCounter) + '.csv'
            fileStoreCounter = fileStoreCounter + 1
            #get the index of DateTime column
            timeIDX = oneVesselLastData.columns.get_loc("DateTime")
            #get second last and last entry
            secLastTS = oneVesselLastData.iloc[-2,timeIDX]
            lastTS = oneVesselLastData.iloc[-1,timeIDX]
            #check for difference 
            lastTimeDiff = convert_to_seconds(lastTS - secLastTS)
            if(lastTimeDiff < 1740):
                aISDM.save_data_to_csv(oneVesselLastData.iloc[0:-1,:],opFile)
            else:
                aISDM.save_data_to_csv(oneVesselLastData,opFile)

def get_sequence_data_frame(vesselName, trajNum):
    #read the data sorted data
    sourceFile = sourceDir + vesselName + '_' + trajNum + '.csv'
    sourceDF, retVal = aISDM.load_data_from_csv(sourceFile)
    # print(sourceDF)
    # print(sourceDF.dtypes)
    #formate the date time
    sourceDFFT = aISDM.formate_time(sourceDF,'DateTime')    
    
    ret = sourceDFFT.copy()
    print(ret.shape)
    
    timeIDX = ret.columns.get_loc("DateTime")
    lowerTimeWin = get_lower_time(ret.iloc[0,timeIDX])
    upperTimeWin = get_lower_time(ret.iloc[-1,timeIDX])
    lowerTimeWinIdx = timeWindow.index(lowerTimeWin)
    upperTimeWinIdx = timeWindow.index(upperTimeWin) + 1
    if(upperTimeWinIdx >= len(timeWindow)):
        upperTimeWinIdx = timeWindow.index(upperTimeWin)

    gen_last_entry_data(ret,lowerTimeWinIdx,upperTimeWinIdx)

for mMSI in mMSIList:
    vname,vTraj = mMSI.split("-")
    for vTrajNum in range(int(vTraj)):
        get_sequence_data_frame(vname, str(vTrajNum))