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
dropType = (int)(config['DROP_COL']['DROP_TYPE'])

#years for which we want to crop the data 2015,1016,1017
#based on that we can have more data
yearsToConsider = [int(year) for year in (config['DROP_COL']['YEARS_TO_CONSIDER'].split(','))]

fileNameList = []
for year in yearsToConsider:
    for monthNum in range(1,13):
        fileName = "../Data/"+SOURCE_DIR+"/"+"%02d"%(year)+"_"+"%02d"%(monthNum)+SRC_FILE_SUFFIX+".csv"
        fileNameList.append(fileName)

#this flag specifies 
#whether to store in same directory or use different directory
storeInDestDir = 1

for file in fileNameList:
    #load the data csv file data
    dFObj,_ = aISDM.load_data_from_csv(file)
    #drop unnecessary columns
    if(dropType == 0):
        droppedDF = aISDM.drop_columns(dFObj)
    elif(dropType == 1):
        droppedDF = aISDM.drop_columns_except_sog(dFObj)
    elif(dropType == 2):
        droppedDF = aISDM.drop_columns_except_cog(dFObj)
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