import numpy as np
import math
#to compute haversine distance
from haversine import haversine, Unit

def compute_distance(lon1,lat1,lon2,lat2):
	#(LAT,LON) formate
	startPoint = (lat1, lon1)
	endPoint = (lat2, lon2)
	distanceKM = haversine(startPoint, endPoint)
	return distanceKM

def compute_heading(lon1,lat1,lon2,lat2):
	diffLong = math.radians(lon2 - lon1)

	lat1Rad = math.radians(lat1)
	lat2Rad = math.radians(lat2)

	y = math.sin(diffLong) * math.cos(lat2Rad)
	x = math.cos(lat1Rad) * math.sin(lat2Rad)\
		- (math.sin(lat1Rad) * math.cos(lat2Rad) * math.cos(diffLong))

	compassBearing = 0

	compassBearing = math.atan2(x, y)

	return (-1*math.degrees(compassBearing))+90

if __name__ == '__main__':
	#test 1
	#comment uncomment as needed
	####################################
	# distVal = compute_distance(-119.20,32.0,-119.21,32.01)
	# print(distVal)
	####################################
	angle = compute_heading(-118.25061, 33.71417, -118.24766, 33.71412)
	print(angle)
	angle = compute_heading(-118.24766, 33.71412, -118.24507, 33.71475)
	print(angle)
	angle = compute_heading(-118.24507, 33.71475, -118.24211, 33.71527)
	print(angle)