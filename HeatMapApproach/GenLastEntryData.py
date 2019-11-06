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
SHIP_TYPE_DIR = (config['GEN_LAST_ENTRY']['SHIP_TYPE_DIR'])
genCount = (int)(config['GEN_LAST_ENTRY']['GEN_COUNT'])

sourceDir = [\
            SHIP_TYPE_DIR+"/HalfHr00/"\
            ,SHIP_TYPE_DIR+"/HalfHr01/"\
            ,SHIP_TYPE_DIR+"/HalfHr02/"\
            ,SHIP_TYPE_DIR+"/HalfHr03/"\
            ,SHIP_TYPE_DIR+"/HalfHr04/"\
            ,SHIP_TYPE_DIR+"/HalfHr05/"\
            ,SHIP_TYPE_DIR+"/HalfHr06/"\
            ,SHIP_TYPE_DIR+"/HalfHr07/"\
            ,SHIP_TYPE_DIR+"/HalfHr08/"\
            ,SHIP_TYPE_DIR+"/HalfHr09/"\
            ,SHIP_TYPE_DIR+"/HalfHr10/"\
            ,SHIP_TYPE_DIR+"/HalfHr11/"\
            ,SHIP_TYPE_DIR+"/HalfHr12/"\
            ,SHIP_TYPE_DIR+"/HalfHr13/"\
            ,SHIP_TYPE_DIR+"/HalfHr14/"\
            ,SHIP_TYPE_DIR+"/HalfHr15/"\
            ,SHIP_TYPE_DIR+"/HalfHr16/"\
            ,SHIP_TYPE_DIR+"/HalfHr17/"\
            ,SHIP_TYPE_DIR+"/HalfHr18/"\
            ,SHIP_TYPE_DIR+"/HalfHr19/"\
            ,SHIP_TYPE_DIR+"/HalfHr20/"\
            ,SHIP_TYPE_DIR+"/HalfHr21/"\
            ,SHIP_TYPE_DIR+"/HalfHr22/"\
            ,SHIP_TYPE_DIR+"/HalfHr23/"\
            ,SHIP_TYPE_DIR+"/HalfHr24/"\
            ,SHIP_TYPE_DIR+"/HalfHr25/"\
            ,SHIP_TYPE_DIR+"/HalfHr26/"\
            ,SHIP_TYPE_DIR+"/HalfHr27/"\
            ,SHIP_TYPE_DIR+"/HalfHr28/"\
            ,SHIP_TYPE_DIR+"/HalfHr29/"\
            ]

destDir = [\
            SHIP_TYPE_DIR+"/HalfHr00LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr01LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr02LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr03LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr04LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr05LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr06LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr07LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr08LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr09LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr10LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr11LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr12LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr13LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr14LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr15LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr16LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr17LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr18LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr19LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr20LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr21LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr22LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr23LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr24LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr25LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr26LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr27LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr28LE/"\
            ,SHIP_TYPE_DIR+"/HalfHr29LE/"\
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

if (genCount >= 0):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,0) \
        for fileNumber in range(17519))
    
if(genCount >= 1):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,1) \
        for fileNumber in range(17519))
    
if(genCount >= 2):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,2) \
        for fileNumber in range(17519))

if(genCount >= 3):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,3) \
        for fileNumber in range(17519))

if(genCount >= 4):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,4) \
        for fileNumber in range(17519))

if(genCount >= 5):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,5) \
        for fileNumber in range(17519))

if(genCount >= 6):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,6) \
        for fileNumber in range(17519))

if(genCount >= 7):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,7) \
        for fileNumber in range(17519))

if(genCount >= 8):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,8) \
        for fileNumber in range(17519))

if(genCount >= 9):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,9) \
        for fileNumber in range(17519))

if(genCount >= 10):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,10) \
        for fileNumber in range(17519))

if(genCount >= 11):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,11) \
        for fileNumber in range(17519))    

if(genCount >= 12):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,12) \
        for fileNumber in range(17519))

if(genCount >= 13):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,13) \
        for fileNumber in range(17519))

if(genCount >= 14):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,14) \
        for fileNumber in range(17519))

if(genCount >= 15):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,15) \
        for fileNumber in range(17519))

if(genCount >= 16):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,16) \
        for fileNumber in range(17519))

if(genCount >= 17):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,17) \
        for fileNumber in range(17519))

if(genCount >= 18):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,18) \
        for fileNumber in range(17519))

if(genCount >= 19):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,19) \
        for fileNumber in range(17519))
    
if(genCount >= 20):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,20) \
        for fileNumber in range(17519))

if(genCount >= 21):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,21) \
        for fileNumber in range(17519))

if(genCount >= 22):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,22) \
        for fileNumber in range(17519))

if(genCount >= 23):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,23) \
        for fileNumber in range(17519))

if(genCount >= 24):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,24) \
        for fileNumber in range(17519))

if(genCount >= 25):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,25) \
        for fileNumber in range(17519))

if(genCount >= 26):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,26) \
        for fileNumber in range(17519))

if(genCount >= 27):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,27) \
        for fileNumber in range(17519))

if(genCount >= 28):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,28) \
        for fileNumber in range(17519))

if(genCount >= 29):
    Parallel(n_jobs=numCores, backend = 'multiprocessing', verbose=10) \
        (delayed(gen_last_entry_data) \
        (fileNumber,29) \
        for fileNumber in range(17519))

print("Done Generating The Data")