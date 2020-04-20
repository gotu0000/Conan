import sys
import os
import numpy as np
import pandas as pd

import configparser
sys.path.insert(0, '../Common/')

from AISDataManager import AISDataManager
import Constants as c
import HMUtils as hMUtil
import TimeUtils as timeUtils

from joblib import Parallel, delayed
import multiprocessing

aISDM = AISDataManager()
numCores = multiprocessing.cpu_count()

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

SOURCE_DIR_NAME = (config['SEG_VESSEL']['SRC_DIR_NAME'])
mMSIFile = (config['SEG_VESSEL']['MMSI_FILE'])

print(mMSIFile)
#open list of MMSI file
#and put it into list
mMSIList = [line.rstrip('\n') for line in open(mMSIFile)]

yearsToConsider = [ \
                    15
                    , 16
                    , 17
                    ]

monthToConsider = [ \
                    timeUtils.month['Jan']    \
                    ,timeUtils.month['Feb']   \
                    ,timeUtils.month['March'] \
                    ,timeUtils.month['April'] \
                    ,timeUtils.month['May']   \
                    ,timeUtils.month['June']  \
                    ,timeUtils.month['July']  \
                    ,timeUtils.month['Aug']   \
                    ,timeUtils.month['Sept']  \
                    ,timeUtils.month['Oct']   \
                    ,timeUtils.month['Nov']   \
                    ,timeUtils.month['Dec']   \
                    ]

fileNameList = []
destDirList = []

for year in yearsToConsider:
    for monthNum in monthToConsider:
        fileName = "../Data/"+SOURCE_DIR_NAME+"/"+"%02d"%(year)+"_"+"%02d"%(monthNum)+".csv"
        fileNameList.append(fileName)
        destDirName = "../Data/"+SOURCE_DIR_NAME+"/"+"MMSI_"+"%02d"%(year)+"/"+"%02d"%(monthNum)+"/"
        destDirList.append(destDirName)


for file in fileNameList:
    print(file)

for dir in destDirList:
    print(dir)
'''
dirToStore = (config['SEG_VESSEL']['DEST_DIR'])
print(dirToStore)
data = pd.DataFrame()
for file in fileNameList:
    tempData,_ = aISDM.load_data_from_csv(file)
    data = data.append(tempData, ignore_index = True)

def segregate_vessel_data(vesselName):
    #filter based on MMSI
    vesselData = aISDM.filter_based_on_mmsi(data, int(vesselName))

    #get the name of file
    fileName = dirToStore + vesselName + '.csv'
    aISDM.save_data_to_csv(vesselData,fileName)

    aISDM.formate_time(vesselData,'DateTime',inPlace = True)
    sortedVD = vesselData.sort_values(by='DateTime')

    fileName = dirToStore + vesselName + '_Sorted.csv'
    print(fileName)
    aISDM.save_data_to_csv(sortedVD,fileName)

# Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10)(delayed(segregate_vessel_data)(name) for name in mMSIList)

# segregate_vessel_data(mMSIList[0])
for name in mMSIList:
    segregate_vessel_data(name)
'''


def segregate_vessel_data(vesselName, dirToStore):
    #filter based on MMSI
    vesselData = aISDM.filter_based_on_mmsi(data, int(vesselName))

    #get the name of file
    fileName = dirToStore + vesselName + '.csv'
    aISDM.save_data_to_csv(vesselData,fileName)

    aISDM.formate_time(vesselData,'DateTime',inPlace = True)
    sortedVD = vesselData.sort_values(by='DateTime')

    fileName = dirToStore + vesselName + '_Sorted.csv'
    print(fileName)
    aISDM.save_data_to_csv(sortedVD,fileName)


fileCounter = 0
for file in fileNameList:

    data,_ = aISDM.load_data_from_csv(file)

    destDir = destDirList[fileCounter]

    for name in mMSIList:
        segregate_vessel_data(name,destDir)

    fileCounter = fileCounter + 1