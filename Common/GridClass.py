import numpy as np
import copy

#this is more like structures
#more like a data base
#useful for implementing greedy and random walk
class GridClass():
    #actual lon and lat boundaries
    lonMin = 0.0  
    latMin = 0.0
    
    lonMax = 0.0
    latMax = 0.0
    
    #index when array is flatten
    myFlattenIdx = 0

    #indexes in case of 2dimensianal array
    codeX = 0
    codeY = 0
    
    #transition probabilities of the cell
    p40 = 0
    p41 = 0
    p42 = 0
    p43 = 0
    p44 = 0
    p45 = 0
    p46 = 0
    p47 = 0
    p48 = 0

    def __init__(self, idxVal):
        self.myFlattenIdx = idxVal
        
    def copy(self):
        return copy.deepcopy(self)
    
    #set the value of lon and lat
    def set_lon_min_max(self,minVal, maxVal):
        self.lonMin = minVal
        self.lonMax = maxVal
        
    def set_lat_min_max(self,minVal, maxVal):
        self.latMin = minVal
        self.latMax = maxVal
        
    def set_p40(self,val):
        self.p40 = val
        
    def set_p41(self,val):
        self.p41 = val
        
    def set_p42(self,val):
        self.p42 = val
        
    def set_p43(self,val):
        self.p43 = val
        
    def set_p44(self,val):
        self.p44 = val
        
    def set_p45(self,val):
        self.p45 = val
        
    def set_p46(self,val):
        self.p46 = val
        
    def set_p47(self,val):
        self.p47 = val
        
    def set_p48(self,val):
        self.p48 = val
        
    #return the neigbouring cell with maximum probability
    def get_greedy_cell(self):
        #make np array of probability values
        probArray = np.array([self.p40 \
                              , self.p41 \
                              , self.p42 \
                              , self.p43 \
                              , self.p44 \
                              , self.p45 \
                              , self.p46 \
                              , self.p47 \
                              , self.p48 \
                             ])
        
        #return index of maximum value
        #that will be the cell value
        retVal = np.argmax(probArray)
#         print(retVal)
        return retVal

    #return the neighborung cell with random walk probability
    def get_random_walk_cell(self):
        unifDist = np.random.uniform()
#         print(unifDist)
        
        #first make list of non zero probabilities
        #probVal , cell
        nonZeroList = []
        if(self.p40 > 0):
            nonZeroList.append([self.p40,0])
        if(self.p41 > 0):
            nonZeroList.append([self.p41,1])
        if(self.p42 > 0):
            nonZeroList.append([self.p42,2])
        if(self.p43 > 0):
            nonZeroList.append([self.p43,3])
        if(self.p44 > 0):
            nonZeroList.append([self.p44,4])
        if(self.p45 > 0):
            nonZeroList.append([self.p45,5])
        if(self.p46 > 0):
            nonZeroList.append([self.p46,6])
        if(self.p47 > 0):
            nonZeroList.append([self.p47,7])
        if(self.p48 > 0):
            nonZeroList.append([self.p48,8])
        
#         print(nonZeroList)
        
        #then make list of intervals 
        intvlList = []
        probSum = 0
        for prob,idx in nonZeroList:
            if(len(intvlList) == 0):
                probSum = probSum + prob
                intvlList.append([0,probSum])
            else:
                probSum = probSum + prob
                intvlList.append([intvlList[-1][1],probSum])
#         print(intvlList)
        retVal = 4
        intvlCount = 0
        #now scan through intervals
        for intvl in intvlList:
            #open on left and close on right
            if((unifDist > intvl[0]) and (unifDist <= intvl[1])):
                retVal = nonZeroList[intvlCount][1]
                break
            intvlCount = intvlCount + 1
        
        print(retVal)
        return retVal
    
    #tells whether its in cell or not
    def is_in_cell(self, lon, lat):
        #if its within boundary then its in this cell
        if(lon >= self.lonMin) and (lon < self.lonMax) and (lat >= self.latMin) and (lat < self.latMax):
            return True
        else:
            return False
        
        
if __name__ == '__main__':
    np.random.seed(3)
    gridTest = GridClass(0)
    gridTest.set_p40(0.1)
    gridTest.set_p41(0.0)
    gridTest.set_p42(0.3)
    gridTest.set_p43(0.0)
    gridTest.set_p44(0.0)
    gridTest.set_p45(0.2)
    gridTest.set_p46(0.1)
    gridTest.set_p47(0.0)
    gridTest.set_p48(0.3)
    gridTest.get_random_walk_cell()
    gridTest.get_random_walk_cell()
    gridTest.get_random_walk_cell()
    gridTest.get_random_walk_cell()
    gridTest.get_greedy_cell()
    