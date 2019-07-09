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
config.read('MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

print("Starting Hourly Data Segregation")

fileNameList = ["./Data/AIS_2017_LA/LAPort/AIS_2017_01_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_02_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_03_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_04_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_05_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_06_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_07_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_08_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_09_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_10_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_11_LAP_Sorted.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_12_LAP_Sorted.csv"\
               ]

#list of CSVs from which to load

#list of timestamps
timeIntervalList = ["TimeInterval0.txt"\
                    ,"TimeInterval1.txt"\
                    ,"TimeInterval2.txt"\
                    ,"TimeInterval3.txt"\
                    ,"TimeInterval4.txt"\
                    ,"TimeInterval5.txt"\
                    ,"TimeInterval6.txt"\
                    ,"TimeInterval7.txt"\
                    ,"TimeInterval8.txt"\
                    ,"TimeInterval9.txt"\
                    ,"TimeInterval10.txt"\
                    ,"TimeInterval11.txt"\
                    ]

#destination directory 
#where files will be saved
filePathToStore = "/home/jcharla/PDX/LiporLab/Conan/Data/AIS_2017_LA/LAPort/Hourly/"

fileWriteCounter = 0;

#iterate through all the files
#usually monthly file
#and start segregating them one by one
for i in range(0,len(fileNameList)):
    #load the file
    tempDF, retVal = aISDM.load_data_from_csv(fileNameList[i])
    if(retVal == c.errNO['SUCCESS']):
        #load the corresponding time stamps
        timeWindows = [line.rstrip('\n') for line in open(timeIntervalList[i])]
        for timeSlot in timeWindows:
                #FIXME check for out of bound
                temp = timeSlot.split(',')
                startTime = temp[0]
                endTime = temp[1]

                hourlyDF = aISDM.filter_based_on_time_stamp(tempDF,'DateTime',startTime,endTime)
                tempFilePathToStore = filePathToStore+str(fileWriteCounter)+'.csv'
                print(fileWriteCounter)
                print(tempFilePathToStore)
                fileWriteCounter = fileWriteCounter + 1

                aISDM.save_data_to_csv(hourlyDF,tempFilePathToStore)
        pass
    else:
        print("Something wrong with the file")
        break

print("Done Segregating the data")