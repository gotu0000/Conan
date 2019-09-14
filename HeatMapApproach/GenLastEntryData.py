import sys
sys.path.insert(0, '../Common/')

import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd

import os

#config parser
import configparser

#MyConfig.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('../MyConfig.INI')

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

print("Generating Last Entry Files")

runInParallel = 1

#number of CPU cores to be used
numCores = multiprocessing.cpu_count()
print("Number of available cores = %d"%(numCores))
numCores = 8
print("Using %d cores"%(numCores))    

#assumption is the directory contains souce files in numbered way
sourceDir = "../Data/AIS_SB/Hourly/"
destDir = "../Data/AIS_SB/HourlyLastEntry/"


def gen_last_entry_data(number):
    sourceFile = sourceDir + str(number) + '.csv'
    sourceDF, retVal = aISDM.load_data_from_csv(sourceFile)
    #reverse the rows 
    #so that we can get the last entries in a row
    invertedSourceDF = aISDM.inver_df(sourceDF)
    invertedSourceDFOnce = invertedSourceDF.drop_duplicates(subset="MMSI")
    destFile = destDir + str(number) + '.csv'
    print(destFile)
    aISDM.save_data_to_csv(invertedSourceDFOnce,destFile)


Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber) \
    for fileNumber in range(8760))

print("Done Generating The Data")