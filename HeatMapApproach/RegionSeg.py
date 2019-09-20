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

config = configparser.ConfigParser()
config.read('../MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

aISDM = AISDataManager()
numCores = multiprocessing.cpu_count()

lonMin = (float)(config['REGION']['LON_MIN'])
lonMax = (float)(config['REGION']['LON_MAX'])

latMin = (float)(config['REGION']['LAT_MIN'])
latMax = (float)(config['REGION']['LAT_MAX'])

print("(lonMin , latMin) = (%f,%f)"%(lonMin,latMin))
print("(lonMax , latMax) = (%f,%f)"%(lonMax,latMax))

#depending on approach things will change
approach = 0

if(approach == 0):
    #take list of files and 
    #filter the data of particular region
    #and store it as destination file
    DEST_DIR = "M120_00_M190_50_34_12_34_24"
    fileNameList = [\
                    ("../Data/RawData/AIS_2017_Zone_11/AIS_2017_01_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_01.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_02_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_02.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_03_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_03.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_04_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_04.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_05_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_05.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_06_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_06.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_07_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_07.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_08_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_08.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_09_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_09.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_10_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_10.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_11_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_11.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_12_Zone11.csv", \
                    "../Data/"+DEST_DIR+"/17_12.csv") \
                    ]

    SRC_INDEX = 0
    DEST_INDEX = 1

    for file in fileNameList:
        aISDM.save_data_for_targeted_area( \
                                        file[SRC_INDEX] \
                                        , lonMin \
                                        , lonMax \
                                        , latMin \
                                        , latMax \
                                        , file[DEST_INDEX] \
                                        )
        print("%s generated"%(file[DEST_INDEX]))