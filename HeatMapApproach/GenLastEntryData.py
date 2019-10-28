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

sourceDir = [\
            "../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr00/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr01/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr02/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr03/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr04/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr05/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr06/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr07/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr08/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr09/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr10/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr11/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr12/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr13/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr14/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr15/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr16/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr17/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr18/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr19/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr20/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr21/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr22/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr23/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr24/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr25/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr26/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr27/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr28/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr29/"\
            ]

destDir = [\
            "../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr00LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr01LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr02LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr03LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr04LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr05LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr06LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr07LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr08LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr09LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr10LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr11LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr12LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr13LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr14LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr15LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr16LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr17LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr18LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr19LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr20LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr21LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr22LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr23LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr24LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr25LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr26LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr27LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr28LE/"\
            ,"../Data/M120_50_M119_00_33_90_34_44/Container/HalfHr29LE/"\
            ]

def gen_last_entry_data(number,index):
    sourceFile = sourceDir[index] + str(number) + '.csv'
    sourceDF, retVal = aISDM.load_data_from_csv(sourceFile)
    #reverse the rows 
    #so that we can get the last entries in a row
    invertedSourceDF = aISDM.inver_df(sourceDF)
    invertedSourceDFOnce = invertedSourceDF.drop_duplicates(subset="MMSI")
    destFile = destDir[index] + str(number) + '.csv'
    print(destFile)
    aISDM.save_data_to_csv(invertedSourceDFOnce,destFile)

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,0) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,1) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,2) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,3) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,4) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,5) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,6) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,7) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,8) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,9) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,10) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,11) \
    for fileNumber in range(17519))    

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,12) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,13) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,14) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,15) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,16) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,17) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,18) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,19) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,20) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,21) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,22) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,23) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,24) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,25) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,26) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,27) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,28) \
    for fileNumber in range(17519))

Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
    (delayed(gen_last_entry_data) \
    (fileNumber,29) \
    for fileNumber in range(17519))
print("Done Generating The Data")