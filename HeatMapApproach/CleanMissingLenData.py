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

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

srcDir = (config['CLEAN_MISSING_LEN_DATA']['SRC_DIR'])
fileStart = (int)(config['CLEAN_MISSING_LEN_DATA']['START'])
fileEnd = (int)(config['CLEAN_MISSING_LEN_DATA']['END'])
destDir = (config['CLEAN_MISSING_LEN_DATA']['DEST_DIR'])

print(srcDir)
print(fileStart)
print(fileEnd)
print(destDir)

missingLen = 0
fileWriteCounter = 0
for num in range(fileStart, fileEnd):
    sorceFile = srcDir + str(num) + '.csv'
    sourceDF,_ = aISDM.load_data_from_csv(sorceFile)
    if(math.isnan(sourceDF.loc[0,'Length'])):
        missingLen = missingLen + 1
    else:
    	destFile = destDir + str(fileWriteCounter) + '.csv'
    	aISDM.save_data_to_csv(sourceDF,destFile)
    	fileWriteCounter = fileWriteCounter + 1

print(fileWriteCounter, "+", missingLen)