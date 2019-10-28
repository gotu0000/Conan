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

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

aISDM = AISDataManager()
numCores = multiprocessing.cpu_count()

SOURCE_DIR = (config['ASSIGN_CARGO_COL']['SRC_DIR_NAME'])
SRC_FILE_SUFFIX = (config['ASSIGN_CARGO_COL']['SRC_FILE_SUFFIX'])
#destination directory path
destDir = (config['ASSIGN_CARGO_COL']['DEST_DIR'])
#suffix to be added for the specific type of data
cargoSuffix = (config['ASSIGN_CARGO_COL']['DEST_FILE_SUFFIX'])
vesselInfoFName = (config['ASSIGN_CARGO_COL']['VESSEL_INFO'])

fileNameList = [\
                "../Data/"+SOURCE_DIR+"/17_01"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_02"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_03"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_04"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_05"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_06"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_07"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_08"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_09"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_10"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_11"+SRC_FILE_SUFFIX+".csv" \
                ,"../Data/"+SOURCE_DIR+"/17_12"+SRC_FILE_SUFFIX+".csv" \
                ]

#this flag specifies 
#whether to store in same directory or use different directory
storeInDestDir = 1
mMSIList = [line.rstrip('\n') for line in open(vesselInfoFName)]
'''
#first read the vessel info file
vesselInfo,_  = aISDM.load_data_from_csv(vesselInfoFName)

print(vesselInfo.shape)
#from excel file
MMSI_COL_NUM = 0
CARGO_BOOL_COL_NUM = 2

# vesselInfo = vesselInfo.dropna(subset=["CargoBool"])
print(vesselInfo.columns)
print(vesselInfo.shape)

mMSIDict = {}
for i in range(vesselInfo.shape[0]):
    # print(vesselInfo.iloc[i,MMSI_COL_NUM])
    # print(vesselInfo.iloc[i,CARGO_BOOL_COL_NUM])
    mMSIDict.update({vesselInfo.iloc[i,MMSI_COL_NUM] : vesselInfo.iloc[i,CARGO_BOOL_COL_NUM]})    

print(mMSIDict)
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
'''

def get_cargo_type(x):
    if(str(x) in mMSIList):
        return 'Container'
    else:
        return 'Not Container'

#now iterate through every files
for file in fileNameList:
    #load the data csv file data
    dFObj,_ = aISDM.load_data_from_csv(file)
    #assign not a cargo to every line
    dFObj['CargoBool'] = "Not Container"
    #assign CargoBool Column
    print(dFObj.shape)
    dFObj['CargoBool'] = dFObj['MMSI'].apply(get_cargo_type)
    print(dFObj.head())
    dFObjCargo = dFObj[(dFObj['CargoBool'] == 'Container')]
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