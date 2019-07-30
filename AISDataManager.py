import pandas as pd
import numpy as np 
import Constants as c
import Interpolation as lIP
import GeoCompute as gC

#this class helps to handle
#raw AIS file 
#like filter for one partiular MMSI
#make regeion specific data
#this is more like a library
class AISDataManager():
    def __init__(self):
        pass

    #to load data from the csv file
    def load_data_from_csv(self, fileName):
        try:
            data = pd.read_csv(f'{fileName}')
            return data, c.errNO['SUCCESS']
        except FileNotFoundError:
            print("File : '%s' Not found"%fileName)
            return None, c.errNO['FILE_NOT_FOUND']
    
    #to save the datarame to a file
    def save_data_to_csv(self, dFObj, fileName):
        try:
            dFObj.to_csv(fileName,index=False)
            return c.errNO['SUCCESS']
        except FileNotFoundError:
            print("File : '%s' Not found"%fileName)
            return c.errNO['FILE_NOT_FOUND']

    #excluding endIndex
    #saves cropped df into csv 
    #this will change the original dFObj
    #if we try to modify the returned dataframe 
    def crop_df_and_save_csv(self, dFObj, startIndex, endIndex,fileName = None):
        #get number of rows and columns
        #assumption is dFObj has atleast two dimensions 
        noRows = dFObj.shape[0]
        noCols = dFObj.shape[1]
        if((startIndex >= 0) and (endIndex <= noRows)):
            croppedData = dFObj.iloc[startIndex:endIndex]
        else:
            print("The desired indexes %d:%d causes out of bound"%(startIndex,endIndex))
            return None, c.errNO['INDEX_OUT_OF_BOUND'], c.errNO['DUMMY']

        if(fileName != None):
            ret = self.save_data_to_csv(croppedData,fileName)
        else:
            ret = c.errNO['DUMMY']
        return croppedData, c.errNO['SUCCESS'], ret

    #save data into pickle file
    #serialization module
    def save_data_to_pickle(self, dFObj, fileName):
        #FIXME put this into try except
        dFObj.to_pickle(f'{fileName}')

    #get unique entries of data frame
    def get_list_of_unique_enries(self, dFObj, columnName):
        #check for corresponding column
        #FIXME put this into try cache
        ret = dFObj[columnName].unique()
        return ret

    #specific to AIS kind of data
    def get_list_of_unique_mmsi(self, dFObj):
        return self.get_list_of_unique_enries(dFObj,c.MMSI_COL_NAME)

    #specific to AIS kind of data
    def get_list_of_unique_type(self, dFObj):
        return self.get_list_of_unique_enries(dFObj,c.VESSEL_TYPE_COL_NAME)
        
    #get all the entires of one particular MMSI     
    def filter_based_on_mmsi(self, dFObj, mMSINum):
        #filtered data frame
        #based on MMSI number
        filteredDF = dFObj[dFObj[c.MMSI_COL_NAME] == mMSINum]
        return filteredDF

    #to extract data limited to regeion
    def filter_based_on_lon_lat(self, dFObj, lonMin, lonMax, latMin, latMax):
        filteredDF = dFObj[(dFObj[c.LON_COL_NAME] >= lonMin) \
                            & (dFObj[c.LON_COL_NAME] < lonMax) \
                            & (dFObj[c.LAT_COL_NAME] >= latMin) \
                            & (dFObj[c.LAT_COL_NAME] < latMax) \
                            ]
        return filteredDF

    #will return same DF with extra column
    #this will change the original DF if we change the return value
    def formate_time(self, dFObj, colName):
        #check for whether date time column is already there or not
        if(colName in dFObj.columns):
            if(dFObj.loc[:, colName].dtypes == np.dtype('object')):
                dFObj[colName] = pd.to_datetime(dFObj[colName])
        else:
            dFObj.loc[:, colName] = pd.to_datetime(dFObj['BaseDateTime'], format='%Y-%m-%dT%H:%M:%S')
        return dFObj

    def get_df_for_targeted_area(self, fileName, lonMin, lonMax, latMin, latMax):
        #load df from a file
        dFObj,retVal = self.load_data_from_csv(fileName)
        if(retVal == c.errNO['SUCCESS']):
            #return the min and max
            return self.filter_based_on_lon_lat(dFObj,lonMin, lonMax, latMin, latMax),c.errNO['SUCCESS']
        else:
            return None, retVal

    #loads
    #gets targeted area
    #stores back
    def save_data_for_targeted_area(self, fileName, lonMin, lonMax, latMin, latMax, fileToStore):
        dFObj, retVal = self.get_df_for_targeted_area(fileName, lonMin, lonMax, latMin, latMax)
        if(retVal == c.errNO['SUCCESS']):
            ret = self.save_data_to_csv(dFObj,fileToStore)
            return ret
        else:
            return retVal

    #to drop some columns
    #to reduce memory usage
    def drop_columns(self,dFObj):
        retDF = dFObj.drop(columns=['SOG', 'COG', 'Heading',\
        'VesselName', 'IMO', 'CallSign', \
        'VesselType', 'Status', 'Length',\
        'Width', 'Draft', 'Cargo'])
        return retDF

    def drop_columns(self,dFObj,colList):
        retDF = dFObj.drop(columns = colList)
        return retDF

    #this is to generate data for one vessel
    #append operation may be time consuming
    def get_data_for_one_vessel(self,fileList,mMSINum):
        retDF = pd.DataFrame() 
        for i in fileList:
            #load data from file
            data, retVal = self.load_data_from_csv(i)
            if(retVal == c.errNO['SUCCESS']):
                #get data for one type of vessel
                vesselData = self.filter_based_on_mmsi(data,mMSINum)
                retDF = retDF.append(vesselData,ignore_index = True)
            else:
                break
        return retDF, retVal

    #assumpution with the time 
    def filter_based_on_time_stamp(self, dFObj, timeColName, startTime, endTime):
        self.formate_time(dFObj,timeColName)
        filteredDF = dFObj[(dFObj[timeColName] >= startTime) & (dFObj[timeColName] < endTime)]
        return filteredDF

    #function to get lower bound of time
    #useful for linear interpolation
    #returns a series object
    def get_left_time_stamp_values(self, dFObj, timeColName, timeObj):
        filteredDF = dFObj[(dFObj[timeColName] <= timeObj)]
        if(filteredDF.shape[0] > 0):
            return filteredDF.iloc[-1], c.errNO['SUCCESS']
        else:
            return None, c.errNO['INDEX_OUT_OF_BOUND']

    #function to get upper bound of time
    #useful for linear interpolation
    #returns a series object
    def get_right_time_stamp_values(self, dFObj, timeColName, timeObj):
        filteredDF = dFObj[(dFObj[timeColName] > timeObj)]
        if(filteredDF.shape[0] > 0):
            return filteredDF.iloc[0], c.errNO['SUCCESS']
        else:
            return None, c.errNO['INDEX_OUT_OF_BOUND']

    def append_seconds_column(self, dFObj, timeColName):
        #convert into total seconds
        filteredDF = dFObj.copy()
        filteredDF[timeColName] = pd.to_datetime(filteredDF[timeColName])

        #to generate time delta instance
        startTime = pd.to_datetime(c.SEC_START_TIME)

        #compute the difference
        #this converts into time delta
        secCol = filteredDF[timeColName].copy()
        secCol = secCol - startTime

        filteredDF[c.SEC_COL_NAME] = secCol.dt.total_seconds()

        return filteredDF

    def get_time_stamp_data(self, dFObj, timeColName, timeStampFile):
        #make empty dataframe to return
        retDF = pd.DataFrame(columns=dFObj.columns)
        #append column for seconds 
        secDF = self.append_seconds_column(dFObj,timeColName)
        #FIXME check for file missing
        timeSteps = [line.rstrip('\n') for line in open(timeStampFile)]
        for tS in timeSteps:
            #get the lower value
            lowerValue, retVal = self.get_left_time_stamp_values(secDF,timeColName,tS)
            if(retVal == c.errNO['SUCCESS']):
                secDiffL = pd.to_datetime(tS) - pd.to_datetime(lowerValue[timeColName])
                secDiffL = secDiffL.total_seconds()
                #this is when we have data at desired time stamp
                if(secDiffL == 0):
                    # print(lowerValue)
                    # print(type(lowerValue))
                    interpDF = pd.DataFrame(lowerValue).transpose()
                    interpDF = self.drop_columns(interpDF, colList = [c.SEC_COL_NAME])
                    retDF = retDF.append(interpDF, ignore_index = True, sort = False)
                else:
                    #get the upper value
                    upperValue, retVal = self.get_right_time_stamp_values(secDF,timeColName,tS)
                    if(retVal == c.errNO['SUCCESS']):
                        secDiffR = pd.to_datetime(upperValue[timeColName]) - pd.to_datetime(tS)
                        secDiffR = secDiffR.total_seconds()

                        #check for the data
                        #only register those enties
                        #when there is data between neighbouring time window
                        if((secDiffL < 3600) and (secDiffR < 3600)):

                            interpDict = {}
                            if('MMSI' in secDF.columns):
                                tempMMSI = lowerValue['MMSI']
                                interpDict.update({"MMSI" : [tempMMSI]})

                            if('BaseDateTime' in secDF.columns):
                                # tempBST = tS
                                tempBST = pd.to_datetime(tS).strftime("%Y-%m-%dT%H:%M:%S")
                                interpDict.update({"BaseDateTime" : [tempBST]})

                            if('LAT' in secDF.columns):
                                tempLAT = lIP.apply_linear_interpolation(lowerValue['Seconds']\
                                    ,lowerValue['LAT']\
                                    ,upperValue['Seconds']\
                                    ,upperValue['LAT']\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({"LAT" : [tempLAT]})

                            if('LON' in secDF.columns):
                                tempLON = lIP.apply_linear_interpolation(lowerValue['Seconds']\
                                    ,lowerValue['LON']\
                                    ,upperValue['Seconds']\
                                    ,upperValue['LON']\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({"LON" : [tempLON]})

                            if('SOG' in secDF.columns):
                                tempSOG = lIP.apply_linear_interpolation(lowerValue['Seconds']\
                                    ,lowerValue['SOG']\
                                    ,upperValue['Seconds']\
                                    ,upperValue['SOG']\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({"SOG" : [tempSOG]})

                            if('COG' in secDF.columns):
                                tempCOG = lIP.apply_linear_interpolation(lowerValue['Seconds']\
                                    ,lowerValue['COG']\
                                    ,upperValue['Seconds']\
                                    ,upperValue['COG']\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({"COG" : [tempCOG]})

                            if('Heading' in secDF.columns):
                                tempHeading = lIP.apply_linear_interpolation(lowerValue['Seconds']\
                                    ,lowerValue['Heading']\
                                    ,upperValue['Seconds']\
                                    ,upperValue['Heading']\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({"Heading" : [tempHeading]})

                            if('VesselName' in secDF.columns):
                                tempVesselName = lowerValue['VesselName']
                                interpDict.update({"VesselName" : [tempVesselName]})

                            if('IMO' in secDF.columns):
                                tempIMO = lowerValue['IMO']
                                interpDict.update({"IMO" : [tempIMO]})

                            if('CallSign' in secDF.columns):
                                tempCallSign = lowerValue['CallSign']
                                interpDict.update({"CallSign" : [tempCallSign]})

                            if('VesselType' in secDF.columns):
                                tempVesselType = lowerValue['VesselType']
                                interpDict.update({"VesselType" : [tempVesselType]})

                            if('Status' in secDF.columns):
                                tempStatus = lowerValue['Status']
                                interpDict.update({"Status" : [tempStatus]})

                            if('Length' in secDF.columns):
                                tempLength = lowerValue['Length']
                                interpDict.update({"Length" : [tempLength]})

                            if('Width' in secDF.columns):
                                tempWidth = lowerValue['Width']
                                interpDict.update({"Width" : [tempWidth]})

                            if('Draft' in secDF.columns):
                                tempDraft = lowerValue['Draft']
                                interpDict.update({"Draft" : [tempDraft]})

                            if('Cargo' in secDF.columns):
                                tempCargo = lowerValue['Cargo']
                                interpDict.update({"Cargo" : [tempCargo]})

                            interpDict.update({timeColName : [tS]})                            
                            # interpDF = pd.DataFrame({"MMSI":[tempMMSI]\
                            #                         ,"BaseDateTime":[tempBST]\
                            #                         ,"LAT":[tempLAT]\
                            #                         ,"LON":[tempLON]\
                            #                         ,"SOG":[tempSOG]\
                            #                         ,"COG":[tempCOG]\
                            #                         ,"Heading":[tempHeading]\
                            #                         })

                            #make one data frame
                            interpDF = pd.DataFrame(interpDict)
                            #append to retDF
                            retDF = retDF.append(interpDF, ignore_index = True, sort = False)
                    else:
                        continue
            else:
                #continue if we dont get the lower boundf
                continue
        return retDF

    #this helps to generate timely data
    def get_time_stamp_interpolated_data(self, dFObj, timeColName, timeStampFile):
        tSDF = self.get_time_stamp_data(dFObj, timeColName, timeStampFile)
        dFCopy = dFObj.copy()
        retDF = dFCopy.append(tSDF, ignore_index = True)
        self.formate_time(retDF,'DateTime')
        sortedRet = retDF.sort_values(by='DateTime')
        return sortedRet

    #this function takes houurly time stamped interpolated data
    #then based on cropped dF, it will compute the distance
    def get_time_stamp_data_with_distance(self, dFObj, timeColName, timeStampFile):
        #make empty dataframe to return
        retDF = pd.DataFrame()
        #FIXME check for file missing
        timeColSeries = dFObj[timeColName].tolist()
        # print(timeColSeries)
        #read timestamps file
        timeSteps = [line.rstrip('\n') for line in open(timeStampFile)]

        for tS in range(len(timeSteps)-1):
            lowerVal = timeSteps[tS]
            upperVal = timeSteps[tS+1]
            if(lowerVal in timeColSeries) and (upperVal in timeColSeries):
                print(lowerVal, upperVal)

                lowerIndex = timeColSeries.index(lowerVal)
                upperIndex = timeColSeries.index(upperVal)

                # print(lowerIndex, upperIndex)
                tempDF = dFObj.iloc[lowerIndex:upperIndex+1,:].copy()
                tempLON = tempDF['LON']
                tempLAT = tempDF['LAT']
                tempAvgSOG = tempDF['SOG'].mean()

                #compute the temporary distance betwwen hourly time stamp data
                tempDistance = 0
                for ii in range(tempLON.shape[0]-1):
                    lon1 = tempLON.iloc[ii]
                    lat1 = tempLAT.iloc[ii]
                    lon2 = tempLON.iloc[ii+1]
                    lat2 = tempLAT.iloc[ii+1]
                    # print(lon1,lat1,lon2,lat2)
                    tempDistance = tempDistance + gC.compute_distance(lon1, lat1, lon2, lat2)
                #get the last row which contains value at time stamp
                interpDF = pd.DataFrame(tempDF.iloc[-1]).transpose()
                interpDF.loc[:, "TotalDistance"] = tempDistance
                interpDF.loc[:, "AvgSOG"] = tempAvgSOG
                tempAngle = gC.compute_heading(tempLON.iloc[0], tempLAT.iloc[0], tempLON.iloc[-1], tempLAT.iloc[-1])
                interpDF.loc[:, "Angle"] = tempAngle
                retDF = retDF.append(interpDF, ignore_index = True, sort = False)
        print(retDF)
        return retDF
            

if __name__ == '__main__':
    '''
    aDMTest = AISDataManager()
    lAData,retVal = aDMTest.load_data_from_csv("./Data/AIS_2017_LA/AIS_2017_Zone_11/AIS_2017_01_Zone11_Cropped.csv")
    print(retVal)
    aDMTest.save_data_for_targeted_area("./Data/AIS_2017_LA/AIS_2017_Zone_11/AIS_2017_01_Zone11_Cropped.csv"\
        ,-119.50, -117.10, 32.00, 34.20\
        ,"./Data/AIS_2017_LA/LAPort/AIS_2017_01_LA_Cropped.csv"
        )
    '''
    # croppedData,retVal1,retVal2 = aDMTest.crop_df_and_save_csv(lAData,0,1000,"./Data/AIS_2017_LA/AIS_2017_Zone_11/AIS_2017_01_Zone11_Cropped_.csv")
    # print(retVal1)
    # print(retVal2)
    # retVal = aDMTest.save_data_to_csv(lAData,"./Data/AIS_2017_LB/AIS_2017_Zone_11/AIS_2017_01_Zone11.csv")
    # print(retVal)
    # print(c.errNO)

    '''
    newDF = aDMTest.formate_time(lAData,'DateTime')
    newDF = newDF.sort_values(by='DateTime')
    aDMTest.save_data_to_csv(newDF,"./Data/AIS_2017_LA/AIS_2017_01_Zone11/AIS_ASCII_by_UTM_Month/2017_v2/AIS_2017_01_Zone11_Cropped_Sorted.csv")
    '''
    ###########################
    #Test case for formate time
    aDMTest = AISDataManager()
    lAData,retVal = aDMTest.load_data_from_csv("Dummy.csv")
    if(retVal == c.errNO['SUCCESS']):
        aDMTest.formate_time(lAData, 'DateTime')
        print(lAData.dtypes)
    else:
        print("Erro in loading file")