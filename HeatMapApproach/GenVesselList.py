import sys
import os
import numpy as np
import pandas as pd
import gc

import configparser
sys.path.insert(0, '../Common/')

from AISDataManager import AISDataManager
import Constants as c
import HMUtils as hMUtil
import TimeUtils as timeUtils
import SimpleUtils as sU

from joblib import Parallel, delayed
import multiprocessing

aISDM = AISDataManager()
numCores = multiprocessing.cpu_count()

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

SOURCE_DIR_NAME = (config['GEN_VESSEL_LIST_TXT']['SRC_DIR_NAME'])
fileSuffix = (config['GEN_VESSEL_LIST_TXT']['FILE_SUFFIX'])
destFileName = (config['GEN_VESSEL_LIST_TXT']['DEST_FILE_NAME'])

yearsToConsider = [int(year) for year in (config['GEN_VESSEL_LIST_TXT']['YEARS_TO_CONSIDER'].split(','))]

fileNameList = []
for year in yearsToConsider:
    for monthNum in range(1,13):
        fileName = "../Data/"+SOURCE_DIR_NAME+"/"+"%02d"%(year)+"_"+"%02d"%(monthNum)+fileSuffix+".csv"
        fileNameList.append(fileName)

#generate list of unique entries for entire regeion
vesselListSets = []
for i in fileNameList:
    lAPData,retVal = aISDM.load_data_from_csv(i)
    if(retVal == c.errNO['SUCCESS']):
        vesselListSets.append(aISDM.get_list_of_unique_mmsi(lAPData))
    else:
        print("Unable to load")
        break;

#make empty set
unionOfVesselList = set()
#get unioun of all the sets
for i in vesselListSets:
    unionOfVesselList = unionOfVesselList.union(set(i))

#convert set to list
unionOfVesselList = list(unionOfVesselList)

#sort them
sortedMMSI = unionOfVesselList.copy()
sortedMMSI.sort()

#save to file 
with open(destFileName, 'w') as f:
    for item in sortedMMSI:
        f.write("%s\n" % item)