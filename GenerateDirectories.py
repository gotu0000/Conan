import os

dirName = "/home/jcharla/PDX/LiporLab/Conan/Data/AIS_2017_LA/VesselListGrid/"
for i in range(0,53261):
	dirNameGen = dirName + str(i)
	os.makedirs(dirNameGen)