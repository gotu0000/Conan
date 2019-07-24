import numpy as np
from AISDataManager import AISDataManager
import Constants as c
import pandas as pd
import Interpolation as lIP
import datetime as dt

from joblib import Parallel, delayed
import multiprocessing

#make object of AIS data manager
aISDM = AISDataManager()

ipDirectory = "./Data/AIS_2017_LA/MMSI/Accumulated/"
#in seconds
#for 48 hours
allowedTimeDiff = 3600*48
#time for which interpolation is needed
hourTime = 3600

def interpolate_vessel_data(vesselName):
	#open the csv file
	iPFile = ipDirectory + vesselName + '_Sorted.csv'
	print(iPFile)
	data, retVal = aISDM.load_data_from_csv(iPFile)

	lastRow = 0
	tempDF = pd.DataFrame()
	if(retVal == c.errNO['SUCCESS']):
		#now we have seconds
		dataSec = aISDM.append_seconds_column(data, 'DateTime')

		colList = dataSec.columns.tolist() 
		for row in range(dataSec.shape[0]-1):
			colNum = colList.index(c.SEC_COL_NAME)
			timeDiff = dataSec.iloc[row+1,colNum] - dataSec.iloc[row,colNum]
			if(timeDiff > allowedTimeDiff):
				#do nothing
				#assumption here is that ship got lost
				#crop from last row to current row
				dFSoFar = dataSec.iloc[lastRow:(row+1),:].copy()
				tempDF = tempDF.append(dFSoFar, ignore_index = True)
				lastRow = (row+1)

			elif(timeDiff > hourTime):
				dFSoFar = dataSec.iloc[lastRow:(row+1),:].copy()
				tempDF = tempDF.append(dFSoFar, ignore_index = True)
				lastRow = (row+1)

				#get the sec start 
				colNum = colList.index(c.SEC_COL_NAME)
				secStart = dataSec.iloc[row,colNum]

				#get the time start value 
				#useful for delta 
				colNum = colList.index('DateTime')
				timeStart = dataSec.iloc[row,colNum]

				#get the sec end value
				colNum = colList.index(c.SEC_COL_NAME)
				secEnd = dataSec.iloc[row+1,colNum]

				#get the number of steps
				interpStep = int((timeDiff // hourTime))

				#initailise empty data frame
				interpDF = pd.DataFrame()

				#iterate throgh steps to get the values
				for i in range(interpStep):
					secInterp = secStart + ((i+1) * hourTime)

					interpDict = {}
					colNum = colList.index('MMSI')

					tempMMSI = dataSec.iloc[row,colNum]
					interpDict.update({"MMSI" : [tempMMSI]})

					tempBDT = timeStart + dt.timedelta(seconds = ((i+1)*hourTime))
					interpDict.update({"BaseDateTime" : [tempBDT.strftime("%Y-%m-%dT%H:%M:%S")]})

					colNum = colList.index('LAT')
					tempLAT = lIP.apply_linear_interpolation(secStart\
													,dataSec.iloc[row,colNum]\
													,secEnd\
													,dataSec.iloc[row+1,colNum]\
													,secInterp
													)
					interpDict.update({"LAT" : [tempLAT]})

					colNum = colList.index('LON')
					tempLON = lIP.apply_linear_interpolation(secStart\
													,dataSec.iloc[row,colNum]\
													,secEnd\
													,dataSec.iloc[row+1,colNum]\
													,secInterp
													)
					interpDict.update({"LON" : [tempLON]})

					colNum = colList.index('SOG')
					tempSOG = lIP.apply_linear_interpolation(secStart\
													,dataSec.iloc[row,colNum]\
													,secEnd\
													,dataSec.iloc[row+1,colNum]\
													,secInterp
													)
					interpDict.update({"SOG" : [tempSOG]})

					colNum = colList.index('COG')
					tempCOG = lIP.apply_linear_interpolation(secStart\
													,dataSec.iloc[row,colNum]\
													,secEnd\
													,dataSec.iloc[row+1,colNum]\
													,secInterp
													)
					interpDict.update({"COG" : [tempCOG]})

					colNum = colList.index('Heading')
					tempHeading = lIP.apply_linear_interpolation(secStart\
													,dataSec.iloc[row,colNum]\
													,secEnd\
													,dataSec.iloc[row+1,colNum]\
													,secInterp
													)
					interpDict.update({"Heading" : [tempHeading]})

					colNum = colList.index('VesselName')
					tempVesselName = dataSec.iloc[row,colNum]
					interpDict.update({"VesselName" : [tempVesselName]})

					colNum = colList.index('IMO')
					tempIMO = dataSec.iloc[row,colNum]
					interpDict.update({"IMO" : [tempIMO]})

					colNum = colList.index('CallSign')
					tempCallSign = dataSec.iloc[row,colNum]
					interpDict.update({"CallSign" : [tempCallSign]})

					colNum = colList.index('VesselType')
					tempVesselType = dataSec.iloc[row,colNum]
					interpDict.update({"VesselType" : [tempVesselType]})

					colNum = colList.index('Status')
					tempStatus = dataSec.iloc[row,colNum]
					interpDict.update({"Status" : [tempStatus]})

					colNum = colList.index('Length')
					tempLength = dataSec.iloc[row,colNum]
					interpDict.update({"Length" : [tempLength]})

					colNum = colList.index('Width')
					tempWidth = dataSec.iloc[row,colNum]
					interpDict.update({"Width" : [tempWidth]})

					colNum = colList.index('Draft')
					tempDraft = dataSec.iloc[row,colNum]
					interpDict.update({"Draft" : [tempDraft]})

					colNum = colList.index('Cargo')
					tempCargo = dataSec.iloc[row,colNum]
					interpDict.update({"Cargo" : [tempCargo]})

					interpDict.update({"DateTime" : [timeStart + dt.timedelta(seconds = ((i+1)*hourTime))]})

					interpDF = interpDF.append(pd.DataFrame(interpDict), ignore_index = True)

				# print(interpDF.head())
				#also append interpolated data
				tempDF = tempDF.append(interpDF, ignore_index = True, sort= False)

		dFSoFar = dataSec.iloc[lastRow:,:].copy()
		tempDF = tempDF.append(dFSoFar, ignore_index = True)

		tempDF = aISDM.drop_columns(tempDF, colList = [c.SEC_COL_NAME])
		#read the content
		#write it into file
		oPFileName = ipDirectory + vesselName + '_Sorted_LIP.csv'
		aISDM.save_data_to_csv(tempDF,oPFileName)
	else:
		print("Erro Loading the file")

mMSIList = [line.rstrip('\n') for line in open('MMSIList_15_17.txt')]

numCores = multiprocessing.cpu_count()
print(numCores)

Parallel(n_jobs=numCores, verbose=10)(delayed(interpolate_vessel_data)(name) for name in mMSIList)

# interpolate_vessel_data("0Trial")