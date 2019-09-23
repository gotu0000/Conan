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

SOURCE_DIR = "M120_00_M190_50_34_12_34_24"

fileNameList = [ \
            "../Data/"+SOURCE_DIR+"/17_01.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_02.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_03.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_04.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_05.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_06.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_07.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_08.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_09.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_10.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_11.csv" \
            ,"../Data/"+SOURCE_DIR+"/17_12.csv" \
            ]

dirToStore = "../Data/M120_00_M190_50_34_12_34_24/MMSI/"

mMSIList = [line.rstrip('\n') for line in open('../Data/M120_00_M190_50_34_12_34_24/MMSIList17.txt')]

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

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10)(delayed(segregate_vessel_data)(name) for name in mMSIList)

# segregate_vessel_data(mMSIList[0])
# for name in mMSIList:
#     segregate_vessel_data(name)