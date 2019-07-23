import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd

#make object of AIS data manager
aISDM = AISDataManager()

def generate_vessel_name_list(fileNameList):
	#generate list of unique entries for entire regeion
	vesselListSets = []
	for i in fileNameList:
	    lAPData,retVal = aISDM.load_data_from_csv(i)
	    if(retVal == c.errNO['SUCCESS']):
	        vesselListSets.append(aISDM.get_list_of_unique_mmsi(lAPData))
	    else:
	        print("Unable to load")
	        break;

	#make empty set
	unionOfVesselList = set()
	#get unioun of all the sets
	for i in vesselListSets:
	    unionOfVesselList = unionOfVesselList.union(set(i))

	#convert set to list
	unionOfVesselList = list(unionOfVesselList)

	#sort them
	sortedMMSI = unionOfVesselList.copy()
	sortedMMSI.sort()

	#save to file 
	with open('MMSIList_15_17.txt', 'w') as f:
	    for item in sortedMMSI:
	        f.write("%s\n" % item)

def generate_vessel_type_list(fileNameList):
	vesselTypeListSets = []
	for i in fileNameList:
	    lAPData,retVal = aISDM.load_data_from_csv(i)
	    if(retVal == c.errNO['SUCCESS']):
	        vesselTypeListSets.append(aISDM.get_list_of_unique_type(lAPData))
	    else:
	        print("Unable to load")
	        break;

	#make empty set
	unionOfVesselTypeList = set()
	#get unioun of all the sets
	for i in vesselTypeListSets:
	    unionOfVesselTypeList = unionOfVesselTypeList.union(set(i))

	#convert set to list
	unionOfVesselTypeList = list(unionOfVesselTypeList)

	#sort them
	sortedType = unionOfVesselTypeList.copy()
	sortedType.sort()

	#save to file 
	with open('TypeList_15_17.txt', 'w') as f:
	    for item in sortedType:
	        f.write("%s\n" % item)
	

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

#generate 
generate_vessel_name_list(fileNameList)
generate_vessel_type_list(fileNameList)