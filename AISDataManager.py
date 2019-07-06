import pandas as pd
import numpy as np 
import Constants as c

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
        ret = dFObj[columnName].unique()
        return ret

    #specific to AIS kind of data
    def get_list_of_unique_mmsi(self, dFObj):
        return self.get_list_of_unique_enries(dFObj,"MMSI")
        
    #get all the entires of one particular MMSI     
    def filter_based_on_mmsi(self, dFObj, mMSINum):
        #filtered data frame
        #based on MMSI number
        filteredDF = dFObj[dFObj["MMSI"] == mMSINum]
        return filteredDF

    def filter_based_on_lon_lat(self, dFObj, lonMin, lonMax, latMin, latMax):
        filteredDF = dFObj[dFObj["LON"] >= lonMin]
        filteredDF = filteredDF[filteredDF["LON"] <= lonMax]
        filteredDF = filteredDF[filteredDF["LAT"] >= latMin]
        filteredDF = filteredDF[filteredDF["LAT"] <= latMax]
        '''
        filteredDF = dFObj[(dFObj["LON"] >= lonMin) \
                    & (dFObj["LON"] <= lonMax) \
                    & (dFObj["LAT"] >= latMin) \
                    & (dFObj["LAT"] <= latMax) \
                     ]
        '''
        return filteredDF

    #will return DF with extra column
    def format_time(self, dFObj, colName):
        formattedDF = dFObj.copy()
        formattedDF.loc[:, colName] = pd.to_datetime(formattedDF['BaseDateTime'], format='%Y-%m-%dT%H:%M:%S')
        return formattedDF

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


if __name__ == '__main__':
    aDMTest = AISDataManager()
    lAData,retVal = aDMTest.load_data_from_csv("./Data/AIS_2017_LA/AIS_2017_Zone_11/AIS_2017_01_Zone11_Cropped.csv")
    print(retVal)
    aDMTest.save_data_for_targeted_area("./Data/AIS_2017_LA/AIS_2017_Zone_11/AIS_2017_01_Zone11_Cropped.csv"\
        ,-119.50, -117.10, 32.00, 34.20\
        ,"./Data/AIS_2017_LA/LAPort/AIS_2017_01_LA_Cropped.csv"
        )
    # croppedData,retVal1,retVal2 = aDMTest.crop_df_and_save_csv(lAData,0,1000,"./Data/AIS_2017_LA/AIS_2017_Zone_11/AIS_2017_01_Zone11_Cropped_.csv")
    # print(retVal1)
    # print(retVal2)
    # retVal = aDMTest.save_data_to_csv(lAData,"./Data/AIS_2017_LB/AIS_2017_Zone_11/AIS_2017_01_Zone11.csv")
    # print(retVal)
    # print(c.errNO)

    '''
    newDF = aDMTest.format_time(lAData,'DateTime')
    newDF = newDF.sort_values(by='DateTime')
    aDMTest.save_data_to_csv(newDF,"./Data/AIS_2017_LA/AIS_2017_01_Zone11/AIS_ASCII_by_UTM_Month/2017_v2/AIS_2017_01_Zone11_Cropped_Sorted.csv")
    '''