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

sourceDir = "../Data/M120_00_M190_50_34_12_34_24/MMSI/"
destDir = "../Data/M120_00_M190_50_34_12_34_24/MMSI/"
#read the MMSI data

lonMin = (float)(-120.0)
lonMax = (float)(-119.50)

latMin = (float)(34.12)
latMax = (float)(34.24)

print(lonMin,latMin)
print(lonMax,latMax)

increStep = (float)(0.01)
incrRes = (int)(2)

minuteInterval = 30

timeIntvlTexts = [\
                "../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1701To1702.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1702To1703.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1703To1704.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1704To1705.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1705To1706.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1706To1707.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1707To1708.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1708To1709.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1709To1710.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1710To1711.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1711To1712.txt" \
                ,"../Data/M120_00_M190_50_34_12_34_24/TimeInterval/HalfHourIntvl1712To1801.txt" \
                ]

timeWindows = []
for intvl in timeIntvlTexts:
    # timeWindows = [line.rstrip('\n') for line in open(timeIntervalList)]
    for line in open(intvl):
        timeWindows.append(line.rstrip('\n'))

mMSIListFile = "../Data/M120_00_M190_50_34_12_34_24/MMSIList17.txt"

mMSIList = [line.rstrip('\n') for line in open(mMSIListFile)]

groupDestDir = "../Data/M120_00_M190_50_34_12_34_24/MMSIGroup/"

def gen_last_entry_data(vesselName):
    sourceFile = sourceDir + vesselName + '_Sorted.csv'
    sourceDF, retVal = aISDM.load_data_from_csv(sourceFile)

    oneVesselLastData = pd.DataFrame()
    #based on time stamps 
    for timeSlot in timeWindows:
        temp = timeSlot.split(',')
        startTime = temp[0]
        endTime = temp[1]

        timelyDF = aISDM.filter_based_on_time_stamp(sourceDF,'DateTime',startTime,endTime)
        oneVesselRows = timelyDF.shape[0]
        
        invertedTimelyDF = aISDM.inver_df(timelyDF)
        invertedTimelyDF = invertedTimelyDF.drop_duplicates(subset="MMSI")
        
        oneVesselLastData = oneVesselLastData.append(invertedTimelyDF, ignore_index = True)
    opFile = sourceDir + vesselName + '_SortedLE.csv'
    aISDM.save_data_to_csv(oneVesselLastData,opFile)

# Uncomment the block to generate the data
# Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
#     (delayed(gen_last_entry_data) \
#     (name) \
#     for name in mMSIList)

# def get_index_from_lon_lat(lat,lon):
def get_index_from_lon_lat(latLonRow):
    retVal = -1
    lat = latLonRow['LAT']
    lon = latLonRow['LON']
    for boundary in boundaryArray: 
        if(lon >= boundary[0]) and (lon < boundary[1]) \
            and (lat >= boundary[2]) and (lat < boundary[3]):
            retVal = boundary[4]
            break 
    return retVal

heatMapGrid = hMUtil.generate_grid(lonMin, lonMax, latMin, latMax, increStep, incrRes)

boundaryArray = heatMapGrid[2]
horizontalAxis = heatMapGrid[0]
verticalAxis = heatMapGrid[1]

def convert_to_seconds(timeDel):
    return datetime.timedelta.total_seconds(timeDel)

#function to generate sequence data
#will return list of numpy arrays
def get_sequence_data(vesselName):
    #read the data
    sourceFile = sourceDir + vesselName + '_SortedLE.csv'
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
    colNum = sourceDFFT.columns.tolist().index('VesselType')
  
    if(sourceDFFT.iloc[0,colNum] != 1004.0):
        return []
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

    #get only LAT and LON
    #so that we can use apply to get the sequence of numbers
    sourceDFFT = sourceDFFT.iloc[:,2:4]
    print(slicIdx)
    print(sourceDFFT)

    #list to store all the sequences
    seqArray = []
    if(len(slicIdx) > 0):
        firstIndex = 0
        for i in range(0,len(slicIdx)):
            # print(firstIndex, slicIdx[i]+1)
            ret = sourceDFFT.iloc[firstIndex:slicIdx[i]+1,:].apply(get_index_from_lon_lat,axis=1)
            seqArray.append(ret.to_numpy())
            firstIndex = slicIdx[i]+1
        firstIndex = slicIdx[-1]+1
        ret = sourceDFFT.iloc[firstIndex:,:].apply(get_index_from_lon_lat,axis=1)
        seqArray.append(ret.to_numpy())
    #its all part of one sequence
    else:
        ret = sourceDFFT.apply(get_index_from_lon_lat,axis=1)
        seqArray.append(ret.to_numpy())
    return seqArray

fileStoreCounter = 0
#function to generate sequence data
#will return list of numpy arrays
def get_sequence_data_frame(vesselName):
    global fileStoreCounter
    #read the data
    sourceFile = sourceDir + vesselName + '_SortedLE.csv'
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
    colNum = sourceDFFT.columns.tolist().index('VesselType')
  
    if(sourceDFFT.iloc[0,colNum] != 1004.0):
        return []
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

    if(len(slicIdx) > 0):
        firstIndex = 0
        for i in range(0,len(slicIdx)):
            # print(firstIndex, slicIdx[i]+1)
            ret = sourceDFFT.iloc[firstIndex:slicIdx[i]+1,:].copy()
            print(ret.shape)
            if(ret.shape[0] > 5):
                fileStoreName = groupDestDir + str(fileStoreCounter) + '.csv'
                aISDM.save_data_to_csv(ret,fileStoreName)
                fileStoreCounter = fileStoreCounter + 1
            firstIndex = slicIdx[i]+1
        firstIndex = slicIdx[-1]+1
        ret = sourceDFFT.iloc[firstIndex:,:].copy()
        print(ret.shape)
        if(ret.shape[0] > 5):
            fileStoreName = groupDestDir + str(fileStoreCounter) + '.csv'
            aISDM.save_data_to_csv(ret,fileStoreName)
            fileStoreCounter = fileStoreCounter + 1
            
    #its all part of one sequence
    else:
        ret = sourceDFFT.copy()
        print(ret.shape)
        if(ret.shape[0] > 5):
            fileStoreName = groupDestDir + str(fileStoreCounter) + '.csv'
            aISDM.save_data_to_csv(ret,fileStoreName)
            fileStoreCounter = fileStoreCounter + 1
  
#uncomment to generate sequential data  
# dataList = []
# for name in mMSIList:
#     ret = get_sequence_data(name)
#     for seq in ret:
#         dataList.append(seq)

# print(dataList)
# np.savez("../Data/M120_00_M190_50_34_12_34_24/SeqData.npz",*dataList)

for name in mMSIList:
    get_sequence_data_frame(name)
print(fileStoreCounter)