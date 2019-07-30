import os
import sys
import datetime
import numpy as np

def generate_weekly_interval(startDate, endDate, nameOfFile):

	dateList = []

	dateList.append(startDate)
	incrCounter = 1
	nextDate = startDate

	while(nextDate != endDate):
		nextDate = startDate + datetime.timedelta(weeks=incrCounter)
		dateList.append(nextDate)
		incrCounter = incrCounter + 1

	with open(nameOfFile, 'w') as f:
		for i in range(len(dateList)-1):
			f.write("%s,%s\n" % (dateList[i],dateList[i+1]))


def generate_interval(startDate, endDate, nameOfFile):

	dateList = []

	dateList.append(startDate)
	incrCounter = 1
	nextDate = startDate

	while(nextDate != endDate):
		nextDate = startDate + datetime.timedelta(hours=incrCounter)
		dateList.append(nextDate)
		incrCounter = incrCounter + 1

	with open(nameOfFile, 'w') as f:
		for i in range(len(dateList)-1):
			f.write("%s,%s\n" % (dateList[i],dateList[i+1]))

def generate_time_stamps(startDate, endDate, nameOfFile):

	dateList = []

	dateList.append(startDate)
	incrCounter = 1
	nextDate = startDate

	while(nextDate != endDate):
		nextDate = startDate + datetime.timedelta(hours=incrCounter)
		dateList.append(nextDate)
		incrCounter = incrCounter + 1

	with open(nameOfFile, 'w') as f:
		for i in range(len(dateList)):
			f.write("%s\n" % (dateList[i]))

if __name__ == '__main__':
	#uncomment for hourly based data
	'''
	#YY-MM-DD-HH-MIMI-SESE
	startDateList = [datetime.datetime(2017, 1, 1, 0, 0, 0)\
					,datetime.datetime(2017, 2, 1, 0, 0, 0)\
					,datetime.datetime(2017, 3, 1, 0, 0, 0)\
					,datetime.datetime(2017, 4, 1, 0, 0, 0)\
					,datetime.datetime(2017, 5, 1, 0, 0, 0)\
					,datetime.datetime(2017, 6, 1, 0, 0, 0)\
					,datetime.datetime(2017, 7, 1, 0, 0, 0)\
					,datetime.datetime(2017, 8, 1, 0, 0, 0)\
					,datetime.datetime(2017, 9, 1, 0, 0, 0)\
					,datetime.datetime(2017, 10, 1, 0, 0, 0)\
					,datetime.datetime(2017, 11, 1, 0, 0, 0)\
					,datetime.datetime(2017, 12, 1, 0, 0, 0)\
					]

	endDateList = [datetime.datetime(2017, 2, 1, 0, 0, 0)\
					,datetime.datetime(2017, 3, 1, 0, 0, 0)\
					,datetime.datetime(2017, 4, 1, 0, 0, 0)\
					,datetime.datetime(2017, 5, 1, 0, 0, 0)\
					,datetime.datetime(2017, 6, 1, 0, 0, 0)\
					,datetime.datetime(2017, 7, 1, 0, 0, 0)\
					,datetime.datetime(2017, 8, 1, 0, 0, 0)\
					,datetime.datetime(2017, 9, 1, 0, 0, 0)\
					,datetime.datetime(2017, 10, 1, 0, 0, 0)\
					,datetime.datetime(2017, 11, 1, 0, 0, 0)\
					,datetime.datetime(2017, 12, 1, 0, 0, 0)\
					,datetime.datetime(2018, 1, 1, 0, 0, 0)\
					]

	fileCounter = 0;
	for i in range(len(startDateList)):
		fileToStore = "TimeInterval"+str(fileCounter)+'.txt'
		generate_interval(startDateList[i],endDateList[i],fileToStore)
		fileCounter = fileCounter + 1
	'''
	###############################################################
	#to generate hourly interval
	# generate_time_stamps(datetime.datetime(2017, 1, 1, 0, 0, 0), datetime.datetime(2018, 1, 1, 0, 0, 0) , "HourlyTimeStamp17To18.txt")
	############################################
	# generate_interval(datetime.datetime(2017, 1, 1, 0, 0, 0), datetime.datetime(2018, 1, 1, 0, 0, 0), "HourlyTimeInterval17To18.txt")
	generate_weekly_interval(datetime.datetime(2017, 1, 1, 0, 0, 0), datetime.datetime(2017, 12, 31, 0, 0, 0), "WeeklyTimeInterval17To18.txt")
	##############################################################