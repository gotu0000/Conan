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
    
    def read_data_from_pickle(self,fileName):
        #FIXME try except
        retDF = pd.read_pickle(fileName)
        return retDF

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
        retDF = dFObj.copy()
        if(colName in retDF.columns):
            if(retDF.loc[:, colName].dtypes == np.dtype('object')):
                retDF.loc[:, colName] = pd.to_datetime(retDF[colName])
        else:
            retDF.loc[:, colName] = pd.to_datetime(retDF[c.BASE_TIME_COL_NAME], format='%Y-%m-%dT%H:%M:%S')
        return retDF

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
    def drop_columns(self,dFObj,colList = ['SOG', 'COG', 'Heading',\
        'VesselName', 'IMO', 'CallSign', \
        'VesselType', 'Status', 'Length',\
        'Width', 'Draft', 'Cargo']):
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
        tempDF = self.formate_time(dFObj,timeColName)
        filteredDF = tempDF[(tempDF[timeColName] >= startTime) & (tempDF[timeColName] < endTime)]
        return filteredDF

    #assumption is df is date time formatted
    def filter_based_on_time_stamp_without_copy(self, dFObj, timeColName, startTime, endTime):
        filteredDF = dFObj[(dFObj[timeColName] >= startTime) & (dFObj[timeColName] < endTime)].copy()
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

        #convert into seconds
        filteredDF[c.SEC_COL_NAME] = secCol.dt.total_seconds()

        return filteredDF

    #useful for single vessels data
    #where MMSI would be same
    #this data is useful for modelling time series
    def get_time_stamp_data(self, dFObj, timeColName, timeStampFile, neighbourWindow = 3600):
        #make empty dataframe to return
        retDF = pd.DataFrame(columns=dFObj.columns)
        #append column for seconds 
        secDF = self.append_seconds_column(dFObj,timeColName)
        #FIXME check for file missing
        timeSteps = [line.rstrip('\n') for line in open(timeStampFile)]
        #iterate though time stamps
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
                        if((secDiffL < neighbourWindow) and (secDiffR < neighbourWindow)):

                            interpDict = {}
                            if(c.MMSI_COL_NAME in secDF.columns):
                                tempMMSI = lowerValue[c.MMSI_COL_NAME]
                                interpDict.update({c.MMSI_COL_NAME : [tempMMSI]})

                            if(c.BASE_TIME_COL_NAME in secDF.columns):
                                # tempBST = tS
                                tempBST = pd.to_datetime(tS).strftime("%Y-%m-%dT%H:%M:%S")
                                interpDict.update({c.BASE_TIME_COL_NAME : [tempBST]})

                            if(c.LAT_COL_NAME in secDF.columns):
                                tempLAT = lIP.apply_linear_interpolation(lowerValue[c.SEC_COL_NAME]\
                                    ,lowerValue[c.LAT_COL_NAME]\
                                    ,upperValue[c.SEC_COL_NAME]\
                                    ,upperValue[c.LAT_COL_NAME]\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({c.LAT_COL_NAME : [tempLAT]})

                            if(c.LON_COL_NAME in secDF.columns):
                                tempLON = lIP.apply_linear_interpolation(lowerValue[c.SEC_COL_NAME]\
                                    ,lowerValue[c.LON_COL_NAME]\
                                    ,upperValue[c.SEC_COL_NAME]\
                                    ,upperValue[c.LON_COL_NAME]\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({c.LON_COL_NAME : [tempLON]})

                            if(c.SOG_COL_NAME in secDF.columns):
                                tempSOG = lIP.apply_linear_interpolation(lowerValue[c.SEC_COL_NAME]\
                                    ,lowerValue[c.SOG_COL_NAME]\
                                    ,upperValue[c.SEC_COL_NAME]\
                                    ,upperValue[c.SOG_COL_NAME]\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({c.SOG_COL_NAME : [tempSOG]})

                            if(c.COG_COL_NAME in secDF.columns):
                                tempCOG = lIP.apply_linear_interpolation(lowerValue[c.SEC_COL_NAME]\
                                    ,lowerValue[c.COG_COL_NAME]\
                                    ,upperValue[c.SEC_COL_NAME]\
                                    ,upperValue[c.COG_COL_NAME]\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({c.COG_COL_NAME : [tempCOG]})

                            if(c.HEADING_COL_NAME in secDF.columns):
                                tempHeading = lIP.apply_linear_interpolation(lowerValue[c.SEC_COL_NAME]\
                                    ,lowerValue[c.HEADING_COL_NAME]\
                                    ,upperValue[c.SEC_COL_NAME]\
                                    ,upperValue[c.HEADING_COL_NAME]\
                                    ,(pd.to_datetime(tS) - pd.to_datetime(c.SEC_START_TIME)).total_seconds()
                                    )
                                interpDict.update({c.HEADING_COL_NAME : [tempHeading]})

                            if(c.VESSEL_NAME_COL_NAME in secDF.columns):
                                tempVesselName = lowerValue[c.VESSEL_NAME_COL_NAME]
                                interpDict.update({c.VESSEL_NAME_COL_NAME : [tempVesselName]})

                            if(c.IMO_COL_NAME in secDF.columns):
                                tempIMO = lowerValue[c.IMO_COL_NAME]
                                interpDict.update({c.IMO_COL_NAME : [tempIMO]})

                            if(c.CALL_SIGN_COL_NAME in secDF.columns):
                                tempCallSign = lowerValue[c.CALL_SIGN_COL_NAME]
                                interpDict.update({c.CALL_SIGN_COL_NAME : [tempCallSign]})

                            if(c.VESSEL_TYPE_COL_NAME in secDF.columns):
                                tempVesselType = lowerValue[c.VESSEL_TYPE_COL_NAME]
                                interpDict.update({c.VESSEL_TYPE_COL_NAME : [tempVesselType]})

                            if(c.STATUS_COL_NAME in secDF.columns):
                                tempStatus = lowerValue[c.STATUS_COL_NAME]
                                interpDict.update({c.STATUS_COL_NAME : [tempStatus]})

                            if(c.LENGTH_COL_NAME in secDF.columns):
                                tempLength = lowerValue[c.LENGTH_COL_NAME]
                                interpDict.update({c.LENGTH_COL_NAME : [tempLength]})

                            if(c.WIDTH_COL_NAME in secDF.columns):
                                tempWidth = lowerValue[c.WIDTH_COL_NAME]
                                interpDict.update({c.WIDTH_COL_NAME : [tempWidth]})

                            if(c.DRAFT_COL_NAME in secDF.columns):
                                tempDraft = lowerValue[c.DRAFT_COL_NAME]
                                interpDict.update({c.DRAFT_COL_NAME : [tempDraft]})

                            if(c.CARGO_COL_NAME in secDF.columns):
                                tempCargo = lowerValue[c.CARGO_COL_NAME]
                                interpDict.update({c.CARGO_COL_NAME : [tempCargo]})

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
    #and compute the distance feature for timely data
    def get_time_stamp_interpolated_data(self, dFObj, timeColName, timeStampFile):
        tSDF = self.get_time_stamp_data(dFObj, timeColName, timeStampFile)
        dFCopy = dFObj.copy()
        retDF = dFCopy.append(tSDF, ignore_index = True)
        retDF = self.formate_time(retDF,'DateTime')
        sortedRet = retDF.sort_values(by='DateTime')
        sortedRet  = sortedRet.drop_duplicates(subset ='DateTime')
        return sortedRet

    #this function takes houurly time stamped interpolated data
    #then based on cropped dF, it will compute the distance
    def get_time_stamp_data_with_distance(self, dFObj, timeColName, timeStampFile):
        #make empty dataframe to return
        retDF = pd.DataFrame()
        #FIXME check for file missing
        #FIXME doesnt work if column is time stamp 
        #convert series to series of string then convert into list
        timeColSeries = dFObj[timeColName].tolist()

        # print(timeColSeries)
        #read timestamps file
        timeSteps = [line.rstrip('\n') for line in open(timeStampFile)]

        for tS in range(len(timeSteps)-1):
            lowerVal = timeSteps[tS]
            upperVal = timeSteps[tS+1]

            # print(lowerVal,upperVal)
            #check for lower and upper time stamp
            #if both of them are there then only we can get distance
            if(lowerVal in timeColSeries) and (upperVal in timeColSeries):
                # print(lowerVal, upperVal)

                #get lower index 
                #and upper index
                lowerIndex = timeColSeries.index(lowerVal)
                upperIndex = timeColSeries.index(upperVal)

                # print(lowerIndex, upperIndex)
                tempDF = dFObj.iloc[lowerIndex:upperIndex+1,:].copy()

                # print(tempDF)
                tempLON = tempDF[c.LON_COL_NAME]
                tempLAT = tempDF[c.LAT_COL_NAME]

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
                interpDF.loc[:, c.TOTAL_DISTANCE_COL_NAME] = tempDistance
                tempAngle = gC.compute_heading(tempLON.iloc[0], tempLAT.iloc[0], tempLON.iloc[-1], tempLAT.iloc[-1])
                interpDF.loc[:, c.ANGLE_COL_NAME] = tempAngle
                retDF = retDF.append(interpDF, ignore_index = True, sort = False)
                # print(tempAngle)
        # print(retDF)
        return retDF
            

if __name__ == '__main__':
    ##########################################
    #Test case for formate_time
    # aDMTest = AISDataManager()
    # lAData,retVal = aDMTest.load_data_from_csv("Dummy.csv")
    # if(retVal == c.errNO['SUCCESS']):
    #     lAData = aDMTest.formate_time(lAData, 'DateTime')
    #     print(lAData.dtypes)
    #     print(lAData.shape)
    #     droppedDF = aDMTest.drop_columns(lAData)
    #     print(lAData.shape)
    #     print(droppedDF.shape)
    # else:
    #     print("Erro in loading file")
    ##########################################
    #Test case for get_time_stamp_data
    # aDMTest = AISDataManager()
    # dummyData,retVal = aDMTest.load_data_from_csv("Dummy.csv")
    # if(retVal == c.errNO['SUCCESS']):
    #     dummyData = aDMTest.get_time_stamp_data(dummyData, 'DateTime', 'HourlyTimeStamp15To18.txt')
    #     aDMTest.save_data_to_csv(dummyData,'DummyTS.csv')
    # else:
    #     print("Erro in loading file")
    ##########################################
    #Test case for get_time_stamp_interpolated_data
    # aDMTest = AISDataManager()
    # dummyData,retVal = aDMTest.load_data_from_csv("Dummy.csv")
    # if(retVal == c.errNO['SUCCESS']):
    #     dummyData = aDMTest.get_time_stamp_interpolated_data(dummyData, 'DateTime', 'HourlyTimeStamp15To18.txt')
    #     aDMTest.save_data_to_csv(dummyData,'DummyTSI.csv')
    # else:
    #     print("Erro in loading file")
    ##########################################
    #Test case for get_time_stamp_data_with_distance
    aDMTest = AISDataManager()
    dummyData,retVal = aDMTest.load_data_from_csv("DummyTSI.csv")
    if(retVal == c.errNO['SUCCESS']):
        dummyData = aDMTest.get_time_stamp_data_with_distance(dummyData,'DateTime', 'HourlyTimeStamp15To18.txt')
        aDMTest.save_data_to_csv(dummyData,'DummyTSID.csv')
    else:
        print("Erro in loading file")