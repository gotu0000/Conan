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
dirToStore = (config['SEG_VESSEL']['DEST_DIR'])
mMSIFile = (config['SEG_VESSEL']['MMSI_FILE'])

#open list of MMSI file
#and put it into list
mMSIList = [line.rstrip('\n') for line in open(mMSIFile)]

fileNameList = [ \
            "../Data/"+SOURCE_DIR_NAME+"/16_01.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_02.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_03.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_04.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_05.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_06.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_07.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_08.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_09.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_10.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_11.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/16_12.csv" \
            
            ,"../Data/"+SOURCE_DIR_NAME+"/17_01.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_02.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_03.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_04.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_05.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_06.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_07.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_08.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_09.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_10.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_11.csv" \
            ,"../Data/"+SOURCE_DIR_NAME+"/17_12.csv" \
            ]

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