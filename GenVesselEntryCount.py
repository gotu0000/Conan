import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd

#get all the MMSI entires
mMSIList = [line.rstrip('\n') for line in open('MMSIList_15_17.txt')]
# print(mMSIList)

#make object of AIS data manager
aISDM = AISDataManager()

#dictinary to keep track of number of entires 
#key will be MMSI and corresponding value will be its occurences

vesselEntries = {}
vesselEntries = { i : 0 for i in mMSIList }

# for vessel, count in vesselEntries.items():
# 	print(vessel,":",count)

fileNameList = ["./Data/AIS_2017_LA/LAPort/AIS_2015_01_LAP.csv"
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_02_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_03_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_04_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_05_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_06_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_07_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_08_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_09_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_10_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_11_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2015_12_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_01_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_02_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_03_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_04_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_05_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_06_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_07_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_08_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_09_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_10_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_11_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2016_12_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_01_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_02_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_03_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_04_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_05_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_06_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_07_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_08_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_09_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_10_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_11_LAP.csv"\
                ,"./Data/AIS_2017_LA/LAPort/AIS_2017_12_LAP.csv"\
               ]

#open the file from the list
for file in fileNameList:
	lAPData,retVal = aISDM.load_data_from_csv(file)
	if(retVal == c.errNO['SUCCESS']):
		for index, row in lAPData.iterrows():
			vesselEntries[str(row['MMSI'])] = vesselEntries[str(row['MMSI'])] + 1
	else:
	    print("Unable to load")
	    break;
	
f = open("VesselEntryCount.txt","w")
f.write( str(vesselEntries) )
f.close()