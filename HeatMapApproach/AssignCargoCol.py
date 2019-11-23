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
subTypeStr = (config['ASSIGN_CARGO_COL']['SUB_TYPE_STR'])

yearsToConsider = [int(year) for year in (config['ASSIGN_CARGO_COL']['YEARS_TO_CONSIDER'].split(','))]

fileNameList = []
for year in yearsToConsider:
    for monthNum in range(1,13):
        fileName = "../Data/"+SOURCE_DIR+"/"+"%02d"%(year)+"_"+"%02d"%(monthNum)+SRC_FILE_SUFFIX+".csv"
        fileNameList.append(fileName)

#this flag specifies 
#whether to store in same directory or use different directory
storeInDestDir = 1
mMSIList = [line.rstrip('\n') for line in open(vesselInfoFName)]

def get_cargo_type(x):
    if(str(x) in mMSIList):
        return subTypeStr
    else:
        return 'Not ' + subTypeStr

#now iterate through every files
for file in fileNameList:
    #load the data csv file data
    dFObj,_ = aISDM.load_data_from_csv(file)
    #assign not a cargo to every line
    dFObj['TypeBool'] = "Not " + subTypeStr
    #assign TypeBool Column
    print(dFObj.shape)
    dFObj['TypeBool'] = dFObj['MMSI'].apply(get_cargo_type)
    print(dFObj.head())
    dFObjCargo = dFObj[(dFObj['TypeBool'] == subTypeStr)]
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