# %matplotlib inline
# import matplotlib.pyplot as plt
import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd

import os

#config parser
import configparser

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
# config.read('/home/jcharla/LiporLab/Conan/MyConfig.INI')
config.read('MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()


lonMin = (float)(config['REGEION']['LON_MIN'])
lonMax = (float)(config['REGEION']['LON_MAX'])

latMin = (float)(config['REGEION']['LAT_MIN'])
latMax = (float)(config['REGEION']['LAT_MAX'])

print(lonMin,latMin)
print(lonMax,latMax)

increStep = 0.01
incrRes = 2

xGrid = np.arange(lonMin,lonMax,increStep)
xGrid = np.around(xGrid,incrRes)
yGrid = np.arange(latMin,latMax,increStep)
yGrid = np.around(yGrid,incrRes)

print("Starting Heat Map Generation")

# fileNameList = ["/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_01_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_02_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_03_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_04_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_05_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_06_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_07_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_08_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_09_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_10_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_11_LAP_Dropped.csv"\
                # ,"/home/jcharla/LiporLab/Data/AIS_2017_LAP/AIS_2017_12_LAP_Dropped.csv"\
               # ]

fileNameList = [\
                # "./Data/AIS_2017_LA/LAPort/AIS_2017_01_LAP_Dropped.csv"\
                # ,"./Data/AIS_2017_LA/LAPort/AIS_2017_01_LAP_Dropped.csv"
                # ,"./Data/AIS_2017_LA/LAPort/AIS_2017_03_LAP_Dropped.csv"\
                # ,"./Data/AIS_2017_LA/LAPort/AIS_2017_04_LAP_Dropped.csv"\
                # ,"./Data/AIS_2017_LA/LAPort/AIS_2017_05_LAP_Dropped.csv"\
                # ,"./Data/AIS_2017_LA/LAPort/AIS_2017_06_LAP_Dropped.csv"\
                "./Data/AIS_2017_LA/LAPort/AIS_2017_07_LAP_Dropped.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_08_LAP_Dropped.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_09_LAP_Dropped.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_10_LAP_Dropped.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_11_LAP_Dropped.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_12_LAP_Dropped.csv"\
               ]

lonLatMinMax = []
gridCounter = 0
for i in range(0,yGrid.shape[0]):
    for j in range(0,xGrid.shape[0]):
        if(i < (yGrid.shape[0]-1)):
            if(j < (xGrid.shape[0]-1)):
                localLonMin = xGrid[j]
                localLonMax = xGrid[j+1]
                localLatMin = yGrid[i]
                localLatMax = yGrid[i+1]
            else:
                localLonMin = xGrid[j]
                localLonMax = np.around(xGrid[j]+increStep,incrRes)
                localLatMin = yGrid[i]
                localLatMax = yGrid[i+1]
        else:
            if(j < (xGrid.shape[0]-1)):
                localLonMin = xGrid[j]
                localLonMax = xGrid[j+1]
                localLatMin = yGrid[i]
                localLatMax = np.around(yGrid[i]+increStep,incrRes)
            else:
                localLonMin = xGrid[j]
                localLonMax = np.around(xGrid[j]+increStep,incrRes)
                localLatMin = yGrid[i]
                localLatMax = np.around(yGrid[i]+increStep,incrRes)        
        lonLatMinMax.append([localLonMin,localLonMax,localLatMin,localLatMax,gridCounter])
        # print(lonLatMinMax[-1])
        gridCounter = gridCounter + 1
print(gridCounter)

#make numpy array to this function will accesss
heatMapVal = np.zeros(xGrid.shape[0]*yGrid.shape[0])

dF, retVal = aISDM.load_data_from_csv(fileNameList[0])
print(dF.shape)

for i in range(1,len(fileNameList)):
    temp, retVal = aISDM.load_data_from_csv(fileNameList[i])
    print(temp.shape)
    dF = dF.append(temp,ignore_index = True)
    print(dF.shape)


def compute_transit_count(localLonMin, localLonMax, localLatMin, localLatMax, gridC):
    global heatMapVal
    #make set of unique MMSI for the specific regeion
    localDF = aISDM.filter_based_on_lon_lat(dF,localLonMin,localLonMax,localLatMin,localLatMax)
    vesselList = aISDM.get_list_of_unique_mmsi(localDF)
    heatMapVal[gridC] = len(vesselList)
    print("Done")
    print(gridC)
    print(len(vesselList))

    #save to file 
    # vesseListDir = "./Data/AIS_2017_LA/VesselListGrid/"+str(gridC)+"/Part1.txt"
    vesseListDir = "./Data/AIS_2017_LA/VesselListGrid/"+str(gridC)+"/Part2.txt"
    # vesseListDir = "./Data/AIS_2017_LA/VesselListGrid/"+str(gridC)+"/Part3.txt"
    with open(vesseListDir, 'w') as f:
        for item in vesselList:
            f.write("%s\n" % item)

    # dummy = np.zeros(1)
    # dummy[0] = len(vesselList)
    # dummyStore = "/home/jcharla/LiporLab/Data/DummyStatus/"+str(gridC)+".npy"
    # np.save(dummyStore, dummy)

numCores = multiprocessing.cpu_count()
print(numCores)

# Parallel(n_jobs=numCores, verbose=10)(delayed(compute_transit_count)(boundary[0],boundary[1],boundary[2],boundary[3],boundary[4]) for boundary in lonLatMinMax)

for i in range(len(lonLatMinMax)):
    compute_transit_count(lonLatMinMax[i][0],lonLatMinMax[i][1],lonLatMinMax[i][2],lonLatMinMax[i][3],lonLatMinMax[i][4])

# np.save("/home/jcharla/LiporLab/Conan/HeatMap.npy", heatMapVal)
# np.save("HeatMap1.npy", heatMapVal)
np.save("HeatMap2.npy", heatMapVal)
# np.save("HeatMap3.npy", heatMapVal)
print("Done Generating Histogram")