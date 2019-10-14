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

SOURCE_DIR = "M119_50_M119_00_34_00_34_16"

fileNameList = [\
                "../Data/"+SOURCE_DIR+"/17_01_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_02_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_03_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_04_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_05_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_06_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_07_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_08_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_09_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_10_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_11_Dropped.csv" \
                ,"../Data/"+SOURCE_DIR+"/17_12_Dropped.csv" \
                ]

#this flag specifies 
#whether to store in same directory or use different directory
storeInDestDir = 1
#destination directory path
destDir = "../Data/M119_50_M119_00_34_00_34_16/"
#suffix to be added for the sorted data
sortedSuffix = "_Sorted.csv"

for file in fileNameList:
    #load the data csv file data
    dFObj,_ = aISDM.load_data_from_csv(file)
    #sort with respect to time
    aISDM.formate_time(dFObj,'DateTime',inPlace = True)

    dFObjSorted = dFObj.sort_values(by='DateTime')
    if(storeInDestDir == 1):
        #get just the file name 
        fileName = file.split("/")[-1]
        #replace it with suffix
        drFileName = fileName.replace(".csv",sortedSuffix)
        #generate destination path
        drFileNameToStore = destDir + drFileName
    else:
        #generate destination path by replacing with suffix
        drFileNameToStore = file.replace(".csv",sortedSuffix)
        
    #store in destination
    aISDM.save_data_to_csv(dFObjSorted,drFileNameToStore)
    print("Done Sorting %s"%(file))