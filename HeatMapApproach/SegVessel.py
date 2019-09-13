import sys
sys.path.insert(0, '../Common/')

import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd

import os

import configparser

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

fileNameList = [\
#                 "../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_01_LAP_DrSorted.csv"\
#                 ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_02_LAP_DrSorted.csv"\
#                 ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_03_LAP_DrSorted.csv"\
#                 ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_04_LAP_DrSorted.csv"\
#                 ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_05_LAP_DrSorted.csv"\
#                 ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_06_LAP_DrSorted.csv"\
                "../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_07_LAP_DrSorted.csv"\
                ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_08_LAP_DrSorted.csv"\
                ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_09_LAP_DrSorted.csv"\
                ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_10_LAP_DrSorted.csv"\
                ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_11_LAP_DrSorted.csv"\
                ,"../Data/AIS_0117_1217_31_M120_345_M117/AIS_2017_12_LAP_DrSorted.csv"\
               ]
dirToStore = "../Data/AIS_0117_1217_31_M120_345_M117/MMSI/"

mMSIList = [line.rstrip('\n') for line in open('../Data/AIS_0117_1217_31_M120_345_M117/Output/MMSIList.txt')]

numCores = multiprocessing.cpu_count()
print(numCores)


data = pd.DataFrame()
for file in fileNameList:
    tempData,_ = aISDM.load_data_from_csv(file)
    data = data.append(tempData, ignore_index = True)

def segregate_vessel_data(vesselName):
    #read the CSV file
    #filter based on MMSI
    vesselData = aISDM.filter_based_on_mmsi(data, int(vesselName))

    #get the name 
    fileName = dirToStore + vesselName + '_2.csv'
    aISDM.save_data_to_csv(vesselData,fileName)

    vesselData = aISDM.formate_time(vesselData,'DateTime')
    sortedVD = vesselData.sort_values(by='DateTime')
    fileName = dirToStore + vesselName + '_2_Sorted.csv'
    aISDM.save_data_to_csv(sortedVD,fileName)
    print(fileName)

# Parallel(n_jobs=numCores, verbose=10)(delayed(segregate_vessel_data)(name) for name in mMSIList)


# segregate_vessel_data(mMSIList[0])
for name in mMSIList:
    segregate_vessel_data(name)

'''
def segregate_vessel_data(vesselName):
    #empty data frame
    vesselData = pd.DataFrame()
    #iterate through files
    for file in fileNameList:
        #read the CSV file
        data,_ = aISDM.load_data_from_csv(file)
        
        #filter based on MMSI
        tempVesselData = aISDM.filter_based_on_mmsi(data, int(vesselName))
        vesselData = vesselData.append(tempVesselData, ignore_index = True)
    #get the name 
    fileName = dirToStore + vesselName + '.csv'
    aISDM.save_data_to_csv(vesselData,fileName)

    vesselData = aISDM.formate_time(vesselData,'DateTime')
    sortedVD = vesselData.sort_values(by='DateTime')
    fileName = dirToStore + vesselName + '_Sorted.csv'
    aISDM.save_data_to_csv(sortedVD,fileName)
    print(fileName)

# Parallel(n_jobs=numCores, verbose=10)(delayed(segregate_vessel_data)(name) for name in mMSIList)


# segregate_vessel_data(mMSIList[0])
for name in mMSIList:
    segregate_vessel_data(name)
'''