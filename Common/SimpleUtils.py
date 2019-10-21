#this function is useful for directory name
def convert_boundary_to_string(lonMin, lonMax, latMin, latMax):
	lonMinStr = "%.2f"%(lonMin)
	lonMinStr = lonMinStr.replace('-','M')
	lonMinStr = lonMinStr.replace('.','_')

	lonMaxStr = "%.2f"%(lonMax)
	lonMaxStr = lonMaxStr.replace('-','M')
	lonMaxStr = lonMaxStr.replace('.','_')

	latMinStr = "%.2f"%(latMin)
	latMinStr = latMinStr.replace('-','M')
	latMinStr = latMinStr.replace('.','_')

	latMaxStr = "%.2f"%(latMax)
	latMaxStr = latMaxStr.replace('-','M')
	latMaxStr = latMaxStr.replace('.','_')

	ret = lonMinStr + "_" + lonMaxStr \
					+ "_" + latMinStr \
					+ "_" + latMaxStr
	print(ret)
	return ret

if __name__ == '__main__':
	convert_boundary_to_string(-121.00, -119.00, 33.50, 34.50)

