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

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

aISDM = AISDataManager()
numCores = multiprocessing.cpu_count()

SOURCE_DIR = (config['DROP_COL']['SRC_DIR_NAME'])
SRC_FILE_SUFFIX = (config['DROP_COL']['SRC_FILE_SUFFIX'])
#destination directory path
destDir = (config['DROP_COL']['DEST_DIR'])
#suffix to be added for the dropped data
droppedSuffix = (config['DROP_COL']['DEST_FILE_SUFFIX'])

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

for file in fileNameList:
    #load the data csv file data
    dFObj,_ = aISDM.load_data_from_csv(file)
    #drop unnecessary columns
    droppedDF = aISDM.drop_columns(dFObj)
    if(storeInDestDir == 1):
        #get just the file name 
        fileName = file.split("/")[-1]
        #replace it with suffix
        drFileName = fileName.replace(".csv",droppedSuffix)
        #generate destination path
        drFileNameToStore = destDir + drFileName
    else:
        #generate destination path by replacing with suffix
        drFileNameToStore = file.replace(".csv",droppedSuffix)
        
    #store in destination
    aISDM.save_data_to_csv(droppedDF,drFileNameToStore)
    print("Done Dropping %s"%(file))