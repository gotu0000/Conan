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
fileNameList = [\
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

#this flag specifies 
#whether to store in same directory or use different directory
storeInDestDir = 1
#destination directory path
destDir = "../Data/M120_00_M190_50_34_12_34_24/"
#suffix to be added for the dropped data
droppedSuffix = "_Dropped.csv"

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