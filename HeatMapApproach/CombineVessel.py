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

SOURCE_DIR_NAME = (config['COMBINE_VESSEL']['SOURCE_DIR_NAME'])
mMSIFile = (config['COMBINE_VESSEL']['MMSI_FILE'])
destDir = (config['COMBINE_VESSEL']['DEST_DIR'])
yearsToConsider = [int(year) for year in (config['COMBINE_VESSEL']['YEARS_TO_CONSIDER'].split(','))]

print(SOURCE_DIR_NAME)
print(mMSIFile)
print(destDir)
#open list of MMSI file
#and put it into list
mMSIList = [line.rstrip('\n') for line in open(mMSIFile)]

# yearsToConsider = [ \
#                     15  \
#                     ,16 \
#                     ,17 \
#                     ]


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

destDirList = []

for year in yearsToConsider:
    for monthNum in monthToConsider:
        destDirName = SOURCE_DIR_NAME+"MMSI_"+"%02d"%(year)+"/"+"%02d"%(monthNum)+"/"
        destDirList.append(destDirName)

for dirEn in destDirList:
    print(dirEn)
    

def combine_vessel_data(name):
    #empty dataframe initialization
    yearTrajDF = pd.DataFrame()
    for dirEn in destDirList:
        monTrajFile = dirEn + name +'.csv'
        print(monTrajFile)
        #load and append monthly based data
        monTrajDF,_ = aISDM.load_data_from_csv(monTrajFile)
        yearTrajDF = yearTrajDF.append(monTrajDF, ignore_index = True)
    #write it into file
    yearTrajFile = destDir + name +'.csv'
    aISDM.save_data_to_csv(yearTrajDF,yearTrajFile)
    
    #sort it with time
    aISDM.formate_time(yearTrajDF,'DateTime',inPlace = True)
    sortedYearTrajDF = yearTrajDF.sort_values(by='DateTime')
    
    yearTrajSortedFile = destDir + name +'_Sorted.csv'
    aISDM.save_data_to_csv(sortedYearTrajDF,yearTrajSortedFile)

for name in mMSIList:
    combine_vessel_data(name)