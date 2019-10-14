import sys
import os
import numpy as np
import pandas as pd
import math

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

SOURCE_DIR = "M119_50_M119_00_34_00_34_16"
fileNameList = [\
                "../Data/"+SOURCE_DIR+"/17_01_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_02_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_03_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_04_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_05_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_06_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_07_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_08_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_09_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_10_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_11_Dropped_Sorted.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_12_Dropped_Sorted.csv" \
                ]

#this flag specifies 
#whether to store in same directory or use different directory
storeInDestDir = 1
#destination directory path
destDir = "../Data/M119_50_M119_00_34_00_34_16/"
#suffix to be added for the cargo column appended data
# cargoSuffix = "_Cargo.csv"
cargoSuffix = "_Tanker.csv"

#first read the vessel info file
vesselInfoFName = "../Data/M121_00_M119_00_33_50_34_50/VesselTypeInfo.csv"

vesselInfo,_  = aISDM.load_data_from_csv(vesselInfoFName)

print(vesselInfo.shape)
#from excel file
MMSI_COL_NUM = 0
CARGO_BOOL_COL_NUM = 5

# vesselInfo = vesselInfo.dropna(subset=["CargoBool"])
print(vesselInfo.columns)
print(vesselInfo.shape)

mMSIDict = {}
for i in range(vesselInfo.shape[0]):
    # print(vesselInfo.iloc[i,MMSI_COL_NUM])
    # print(vesselInfo.iloc[i,CARGO_BOOL_COL_NUM])
    mMSIDict.update({vesselInfo.iloc[i,MMSI_COL_NUM] : vesselInfo.iloc[i,CARGO_BOOL_COL_NUM]})    

# print(mMSIDict)
def get_cargo_type(x):
    return mMSIDict[x]

#now iterate through every files
for file in fileNameList:
    #load the data csv file data
    dFObj,_ = aISDM.load_data_from_csv(file)
    #assign not a cargo to every line
    dFObj['CargoBool'] = "Not Cargo"
    #assign CargoBool Column
    print(dFObj.shape)
    dFObj['CargoBool'] = dFObj['MMSI'].apply(get_cargo_type)
    # dFObjCargo = dFObj[(dFObj['CargoBool'] == 'Cargo')]
    dFObjCargo = dFObj[(dFObj['CargoBool'] == 'Tanker')]
    if(storeInDestDir == 1):
        #get just the file name 
        fileName = file.split("/")[-1]
        #replace it with suffix
        drFileName = fileName.replace(".csv",cargoSuffix)
        #generate destination path
        drFileNameToStore = destDir + drFileName
    else:
        #generate destination path by replacing with suffix
        drFileNameToStore = file.replace(".csv",cargoSuffix)
        
    #store in destination
    aISDM.save_data_to_csv(dFObjCargo,drFileNameToStore)
    print("Done Assigning Cargo Bool Column %s"%(file))