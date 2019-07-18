#this is more like a structure
#we will make objects of this to store lattice information
class LatticeObject():
	#bottom left LON and LAT coordinates
	lon = 0.0  
	lat = 0.0

	codeX = 0
	codeY = 0
	#nuumber of AIS record
	sampleCount = 0

	#MMSI number
	vesselID = ''

	#-1 for not assigned
	# 0 onwards assigned
	clusterID = -1

	def __init__(self):
		pass

	def __init__(self, lonVal, latVal):
		self.lon = lonVal
		self.lat = latVal
