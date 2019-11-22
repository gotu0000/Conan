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

SOURCE_DIR = (config['SORT_DATA']['SRC_DIR_NAME'])
SRC_FILE_SUFFIX = (config['SORT_DATA']['SRC_FILE_SUFFIX'])
#destination directory path
destDir = (config['SORT_DATA']['DEST_DIR'])
#suffix to be added for the sorted data
sortedSuffix = (config['SORT_DATA']['DEST_FILE_SUFFIX'])


#years for which we want to crop the data 2015,1016,1017
#based on that we can have more data
yearsToConsider = [int(year) for year in (config['SORT_DATA']['YEARS_TO_CONSIDER'].split(','))]

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