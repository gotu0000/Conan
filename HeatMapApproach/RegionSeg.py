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

# lonMin = (float)(config['REGION']['LON_MIN'])
# lonMax = (float)(config['REGION']['LON_MAX'])

# latMin = (float)(config['REGION']['LAT_MIN'])
# latMax = (float)(config['REGION']['LAT_MAX'])

# print("(lonMin , latMin) = (%f,%f)"%(lonMin,latMin))
# print("(lonMax , latMax) = (%f,%f)"%(lonMax,latMax))

lonMin = (float)(-120.50)
lonMax = (float)(-119.00)

latMin = (float)(33.90)
latMax = (float)(34.38)

print("(lonMin , latMin) = (%f,%f)"%(lonMin,latMin))
print("(lonMax , latMax) = (%f,%f)"%(lonMax,latMax))


#depending on approach things will change
approach = 2

if(approach == 0):
    #take list of files and 
    #filter the data of particular region
    #and store it as destination file
    # DEST_DIR = "M120_00_M190_50_34_12_34_24"
    # fileNameList = [\
    #                 ("../Data/RawData/AIS_2017_Zone_11/AIS_2017_01_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_01.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_02_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_02.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_03_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_03.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_04_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_04.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_05_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_05.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_06_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_06.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_07_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_07.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_08_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_08.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_09_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_09.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_10_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_10.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_11_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_11.csv") \
    #                 ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_12_Zone11.csv", \
    #                 "../Data/"+DEST_DIR+"/17_12.csv") \
    #                 ]
    #                 
    fileNameList = [\
                    ("../Data/M121_00_M119_00_33_50_34_50/MMSI/566952000_Sorted.csv", \
                    "../Data/M119_50_M119_00_34_00_34_16/MMSI/566952000_Sorted.csv") \
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
    
elif(approach == 1):
    DEST_DIR = "M121_00_M119_00_33_50_34_50"
    fileNameList = [\
                    # ("../Data/RawData/AIS_2017_Zone_11/AIS_2017_01_Zone11.csv", \
                    # "../Data/RawData/AIS_2017_Zone_10/AIS_2017_01_Zone10.csv", \
                    # "../Data/"+DEST_DIR+"/17_01.csv") \
                    # ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_02_Zone11.csv", \
                    # "../Data/RawData/AIS_2017_Zone_10/AIS_2017_02_Zone10.csv", \
                    # "../Data/"+DEST_DIR+"/17_02.csv") \
                    # ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_03_Zone11.csv", \
                    # "../Data/RawData/AIS_2017_Zone_10/AIS_2017_03_Zone10.csv", \
                    # "../Data/"+DEST_DIR+"/17_03.csv") \
                    # ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_04_Zone11.csv", \
                    # "../Data/RawData/AIS_2017_Zone_10/AIS_2017_04_Zone10.csv", \
                    # "../Data/"+DEST_DIR+"/17_04.csv") \
                    ("../Data/RawData/AIS_2017_Zone_11/AIS_2017_05_Zone11.csv", \
                    "../Data/RawData/AIS_2017_Zone_10/AIS_2017_05_Zone10.csv", \
                    "../Data/"+DEST_DIR+"/17_05.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_06_Zone11.csv", \
                    "../Data/RawData/AIS_2017_Zone_10/AIS_2017_06_Zone10.csv", \
                    "../Data/"+DEST_DIR+"/17_06.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_07_Zone11.csv", \
                    "../Data/RawData/AIS_2017_Zone_10/AIS_2017_07_Zone10.csv", \
                    "../Data/"+DEST_DIR+"/17_07.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_08_Zone11.csv", \
                    "../Data/RawData/AIS_2017_Zone_10/AIS_2017_08_Zone10.csv", \
                    "../Data/"+DEST_DIR+"/17_08.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_09_Zone11.csv", \
                    "../Data/RawData/AIS_2017_Zone_10/AIS_2017_09_Zone10.csv", \
                    "../Data/"+DEST_DIR+"/17_09.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_10_Zone11.csv", \
                    "../Data/RawData/AIS_2017_Zone_10/AIS_2017_10_Zone10.csv", \
                    "../Data/"+DEST_DIR+"/17_10.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_11_Zone11.csv", \
                    "../Data/RawData/AIS_2017_Zone_10/AIS_2017_11_Zone10.csv", \
                    "../Data/"+DEST_DIR+"/17_11.csv") \
                    ,("../Data/RawData/AIS_2017_Zone_11/AIS_2017_12_Zone11.csv", \
                    "../Data/RawData/AIS_2017_Zone_10/AIS_2017_12_Zone10.csv", \
                    "../Data/"+DEST_DIR+"/17_12.csv") \
                    ]

    SRC_1_INDEX = 0
    SRC_2_INDEX = 1
    DEST_INDEX = 2
    for file in fileNameList:
        src1, _ = aISDM.load_data_from_csv(file[SRC_1_INDEX])
        filteredDF1 = aISDM.filter_based_on_lon_lat(src1,lonMin, lonMax, latMin, latMax)
        print(src1.shape)
        print(filteredDF1.shape)
        src1 = pd.DataFrame()
        src2, _ = aISDM.load_data_from_csv(file[SRC_2_INDEX])
        filteredDF2 = aISDM.filter_based_on_lon_lat(src2,lonMin, lonMax, latMin, latMax)
        print(src2.shape)
        print(filteredDF2.shape)
        src2 = pd.DataFrame()
        combinedDF = filteredDF1.append(filteredDF2, ignore_index = True)
        print(combinedDF.shape)
        #filter for the desired region
        #save data to destination
        aISDM.save_data_to_csv(combinedDF,file[DEST_INDEX])
        print("%s generated"%(file[DEST_INDEX]))

        filteredDF1 = pd.DataFrame()
        filteredDF2 = pd.DataFrame()
        combinedDF = pd.DataFrame()
elif(approach == 2):
    srcDir = "../Data/M121_00_M119_00_33_50_34_50/HalfHourly/"
    destDir = "../Data/M120_50_M119_00_33_90_34_38/HalfHourly/"
    for file in range(17519):
        srcFile = srcDir + str(file) + '.csv'
        destFile = destDir + str(file) + '.csv'
        aISDM.save_data_for_targeted_area( \
                                        srcFile \
                                        , lonMin \
                                        , lonMax \
                                        , latMin \
                                        , latMax \
                                        , destFile \
                                        )
        print("%s generated"%(destFile))