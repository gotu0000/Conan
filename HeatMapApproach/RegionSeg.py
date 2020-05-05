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

lonMin = (float)(config['REGION']['LON_MIN'])
lonMax = (float)(config['REGION']['LON_MAX'])

latMin = (float)(config['REGION']['LAT_MIN'])
latMax = (float)(config['REGION']['LAT_MAX'])

print("(lonMin , latMin) = (%f,%f)"%(lonMin,latMin))
print("(lonMax , latMax) = (%f,%f)"%(lonMax,latMax))

#depending on approach things will change
#1 for cropping from the raw data of AIS
approach = (int)(config['REGION_SEG']['APPROACH'])
print("approach = %d"%(approach))

fileSuffix = (config['REGION_SEG']['FILE_SUFFIX'])
print(fileSuffix)

#years for which we want to crop the data 2015,1016,1017
#based on that we can have more data
yearsToConsider = [int(year) for year in (config['REGION_SEG']['YEARS_TO_CONSIDER'].split(','))]

print("Starting Cropping...")
#approach 0 takes source and destination as list of files
if(approach == 0):

    DEST_DIR = sU.convert_boundary_to_string(lonMin \
                                        , lonMax \
                                        , latMin \
                                        , latMax \
                                        )
    
    #FIXME this list can be generated
    fileNameList = [\
                    ("../Data/M121_00_M119_00_33_50_34_50/17_01"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_01"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_02"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_02"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_03"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_03"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_04"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_04"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_05"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_05"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_06"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_06"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_07"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_07"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_08"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_08"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_09"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_09"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_10"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_10"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_11"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_11"+fileSuffix+".csv") \
                    ,("../Data/M121_00_M119_00_33_50_34_50/17_12"+fileSuffix+".csv", \
                    "../Data/"+DEST_DIR+"/17_12"+fileSuffix+".csv") \
                    ]

    
    SRC_INDEX = 0
    DEST_INDEX = 1

    #take list of files and 
    #filter the data of particular region
    #and store it as destination file
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
    DEST_DIR = sU.convert_boundary_to_string(lonMin \
                                        , lonMax \
                                        , latMin \
                                        , latMax \
                                        )

    #generate list of files from the approach
    fileNameList = []
    for year in yearsToConsider:
        for monthNum in range(1,13):
            fileNames = ("../Data/RawData/AIS_20"+"%02d"%(year)+"_Zone_11/AIS_20"+"%02d"%(year)+"_"+"%02d"%(monthNum)+"_Zone11.csv", \
                    "../Data/RawData/AIS_20"+"%02d"%(year)+"_Zone_10/AIS_20"+"%02d"%(year)+"_"+"%02d"%(monthNum)+"_Zone10.csv", \
                    "../Data/"+DEST_DIR+"/"+"%02d"%(year)+"_"+"%02d"%(monthNum)+fileSuffix+".csv")
            
            fileNameList.append(fileNames)

    SRC_1_INDEX = 0
    SRC_2_INDEX = 1
    DEST_INDEX = 2
    for file in fileNameList:
        src1, _ = aISDM.load_data_from_csv(file[SRC_1_INDEX])
        filteredDF1 = aISDM.filter_based_on_lon_lat(src1,lonMin, lonMax, latMin, latMax)
        print(src1.shape)
        print(filteredDF1.shape)
        src1 = pd.DataFrame()
        gc.collect()
        src2, _ = aISDM.load_data_from_csv(file[SRC_2_INDEX])
        filteredDF2 = aISDM.filter_based_on_lon_lat(src2,lonMin, lonMax, latMin, latMax)
        print(src2.shape)
        print(filteredDF2.shape)
        src2 = pd.DataFrame()
        gc.collect()
        combinedDF = filteredDF1.append(filteredDF2, ignore_index = True)
        print(combinedDF.shape)
        #filter for the desired region
        #save data to destination
        aISDM.save_data_to_csv(combinedDF,file[DEST_INDEX])
        print("%s generated"%(file[DEST_INDEX]))

        filteredDF1 = pd.DataFrame()
        filteredDF2 = pd.DataFrame()
        combinedDF = pd.DataFrame()

        gc.collect()

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

elif(approach == 3):
    #read list of MMSI
    mMSIListFile = "../Data/M121_00_M119_00_33_50_34_50/MMSIList17.txt"
    mMSIList = [line.rstrip('\n') for line in open(mMSIListFile)]
    #and for each vessel data
    #crop the data limited to that region
    srcDir = "../Data/M121_00_M119_00_33_50_34_50/MMSI/"
    destDir = "../Data/M119_50_M119_00_34_00_34_16/MMSI/"
    for name in mMSIList:
        srcFile = srcDir + name + '_Sorted.csv'
        destFile = destDir + name + '_Sorted.csv'
        aISDM.save_data_for_targeted_area( \
                                        srcFile \
                                        , lonMin \
                                        , lonMax \
                                        , latMin \
                                        , latMax \
                                        , destFile \
                                        )
        print("%s generated"%(destFile))
elif(approach == 4):
    DEST_DIR = sU.convert_boundary_to_string(lonMin \
                                        , lonMax \
                                        , latMin \
                                        , latMax \
                                        )
    
    #FIXME this list can be generated
    fileNameList = [\
                    ("../Data/RawData/AIS_2017_Zone_18/AIS_2017_01_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_01"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_02_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_02"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_03_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_03"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_04_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_04"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_05_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_05"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_06_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_06"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_07_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_07"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_08_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_08"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_09_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_09"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_10_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_10"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_11_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_11"+fileSuffix+".csv") \
                    ,("../Data/RawData/AIS_2017_Zone_18/AIS_2017_12_Zone18.csv", \
                    "../Data/"+DEST_DIR+"/17_12"+fileSuffix+".csv") \
                    ]

    
    SRC_INDEX = 0
    DEST_INDEX = 1

    #take list of files and 
    #filter the data of particular region
    #and store it as destination file
    for file in fileNameList:
        # aISDM.save_data_for_targeted_area( \
        #                                 file[SRC_INDEX] \
        #                                 , lonMin \
        #                                 , lonMax \
        #                                 , latMin \
        #                                 , latMax \
        #                                 , file[DEST_INDEX] \
        #                                 )
        #initalise empty cropped DF
        croppedDF = pd.DataFrame()
        #read csv in chunk and 
        #crop it
        #and keep on appending it
        for srcChunk in pd.read_csv(f'{file[SRC_INDEX]}',chunksize=(10 ** 6)):
            croppedChunk = aISDM.filter_based_on_lon_lat(srcChunk,lonMin, lonMax, latMin, latMax)
            croppedDF = croppedDF.append(croppedChunk, ignore_index = True)
        aISDM.save_data_to_csv(croppedDF,file[DEST_INDEX])
        print("%s generated"%(file[DEST_INDEX]))