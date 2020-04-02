import sys
import numpy as np
from keras.models import load_model
from keras.models import Model
import configparser
from sklearn.preprocessing import OneHotEncoder

#CONAN_PRED.INI stores all the run time constants
config = configparser.ConfigParser()
config.read('CONAN_PRED.INI')

lonMin = (float)(config['REGION']['LON_MIN'])
lonMax = (float)(config['REGION']['LON_MAX'])

latMin = (float)(config['REGION']['LAT_MIN'])
latMax = (float)(config['REGION']['LAT_MAX'])

modelPath = config['MODEL']['MODEL_PATH']
maxTypes = (int)(config['MODEL']['MAX_TYPES'])

print(lonMin, latMin)
print(lonMax, latMax)
print(modelPath)

#Load the Model
model = load_model(modelPath)
onehot_encoder = OneHotEncoder(n_values = maxTypes, sparse=False)

def run_lstm(lat_t1, lon_t1, lat_t2, lon_t2, spd, brg, cls):
    """
    """
    #check for the instance
    #whether its an ND array or just a scalar
    isScalar = 0
    if(isinstance(lat_t1,np.ndarray)):
#         print("NP Array")
        m = lat_t1.shape[0]
        isScalar = 0
    else:
#         print("Scaler")
        m = 1
        isScalar = 1
        
#     print("Number of Rows =",m)
    typeDataRows = m
    #Normalise LAT and LON
    lon_t1_norm = (lon_t1 - lonMin)/(lonMax - lonMin)
    lon_t2_norm = (lon_t2 - lonMin)/(lonMax - lonMin)
    lat_t1_norm = (lat_t1 - latMin)/(latMax - latMin)
    lat_t2_norm = (lat_t2 - latMin)/(latMax - latMin)
    if(isScalar == 1):
        typeData = np.zeros((typeDataRows, maxTypes))
        typeData[0,(int)(cls)] = 1
        t1Data = np.array([[lon_t1_norm, lat_t1_norm]])
        t2Data = np.array([[lon_t2_norm, lat_t2_norm]])
        xData = np.hstack((t1Data, typeData, t2Data, typeData))
        
    else:
#         typeData = np.zeros((typeDataRows, maxTypes))
#         for row in range(typeData.shape[0]):
#             typeData[row,(int)(cls[row])] = 1
        typeData = onehot_encoder.fit_transform(np.reshape(cls,(cls.shape[0],1)))
        lon_t1_norm = np.reshape(lon_t1_norm,(lon_t1_norm.shape[0],1))
        lon_t2_norm = np.reshape(lon_t2_norm,(lon_t2_norm.shape[0],1))
        lat_t1_norm = np.reshape(lat_t1_norm,(lat_t1_norm.shape[0],1))
        lat_t2_norm = np.reshape(lat_t2_norm,(lat_t2_norm.shape[0],1))
        xData = np.hstack((lon_t1_norm, lat_t1_norm, typeData, lon_t2_norm, lat_t2_norm, typeData))
    
#     print(xData)
    xDataTS = np.reshape(xData,(xData.shape[0], 2, 4))
#     print(xDataTS)
    
    predLatLon = model.predict(xDataTS)
    
    predLon = predLatLon[:,0]
    predLat = predLatLon[:,1]
    
    #after prediction de normalise it
    predLonScaled = (predLon * (lonMax - lonMin)) + lonMin
    predLatScaled = (predLat * (latMax - latMin)) + latMin
    
    return predLatScaled, predLonScaled, spd, brg

if __name__ == "__main__":
    ret = run_lstm(34.29972, -120.41112, 34.27673, -120.30972, 10.1, 92, 0);
    print(ret)
    ret = run_lstm(np.array([34.29972, 34.27673]) \
             , np.array([-120.41112, -120.30972]) \
             , np.array([34.27673,34.25507]) \
             , np.array([-120.30972,-120.21332]) \
             , np.array([10.1,10.1]) \
             , np.array([92, 92]) \
             , np.array([0,0])); 
#     firstLat = 34.29972
#     fisrtLon = -120.41112
#     secLat = 34.27673
#     secLon = -120.30972
#     for i in range(8):
#         ret = run_lstm(firstLat, fisrtLon, secLat, secLon, 10.1, 92, 0);
# #         print(type(ret[1]))
#         print(ret[1][0], ret[0][0])
    
#         firstLat = secLat
#         fisrtLon = secLon
#         secLat = ret[0][0]
#         secLon = ret[1][0]