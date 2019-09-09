import os
import sys
import datetime
import numpy as np


##
## @brief      generates weekly interval file between two date time instances 
## be cautious while giving endDate
## otherwise it will stuck into while loop
##
## @param      startDate   The start date time object
## @param      endDate     The end date time object
## @param      nameOfFile  The name of file in which we will save the 
## intervals
##
## @return     None
##
def generate_weekly_interval(startDate, endDate, nameOfFile):

	#container for date time objects
	dateList = []

	#first object will be start date itself
	dateList.append(startDate)
	#this is used to determine the next date time object 
	incrCounter = 1

	#dummy initialisation
	nextDate = startDate

	while(nextDate != endDate):
		#keep on generating next date time instance 
		#using time delta
		nextDate = startDate + datetime.timedelta(weeks=incrCounter)
		dateList.append(nextDate)
		incrCounter = incrCounter + 1

	#open a file and write everything into list
	with open(nameOfFile, 'w') as f:
		for i in range(len(dateList)-1):
			f.write("%s,%s\n" % (dateList[i],dateList[i+1]))


##
## @brief      Generate intervals separated by hours
##
## @param      startDate   The start date time object
## @param      endDate     The end date time object
## @param      nameOfFile  The name of file in which to store interval
## @param      incrBy      The number of hour by which we want to increment
##
## @return     None
##
def generate_interval(startDate, endDate, nameOfFile, incrBy = 1):

	#container for time stamps
	dateList = []

	#first put start time
	dateList.append(startDate)

	incrCounter = incrBy
	nextDate = startDate
	print(incrCounter)
	#keep on appending the date time objects created 
	#using timedelta
	while(nextDate != endDate):
		nextDate = startDate + datetime.timedelta(hours=incrCounter)
		dateList.append(nextDate)
		incrCounter = incrCounter + incrBy

	#write it into a file
	with open(nameOfFile, 'w') as f:
		for i in range(len(dateList)-1):
			f.write("%s,%s\n" % (dateList[i],dateList[i+1]))

#unit 0 for sec
#unit 1 for min
def generate_sec_min_interval(startTime, endTime, nameOfFile, unit = 0, incrBy = 1):
	#container for time stamps
	timeList = []

	#first put start time
	timeList.append(startTime)

	incrCounter = incrBy
	nextTime = startTime

	#keep on appending the date time objects created 
	#using timedelta
	while(nextTime != endTime):
		#if seconds
		if(unit == 0):
			nextTime = startTime + datetime.timedelta(seconds=incrCounter)
		else:
			nextTime = startTime + datetime.timedelta(minutes=incrCounter)
		timeList.append(nextTime)
		incrCounter = incrCounter + incrBy

	#write it into a file
	with open(nameOfFile, 'w') as f:
		for i in range(len(timeList)-1):
			f.write("%s,%s\n" % (timeList[i],timeList[i+1]))


##
## @brief      Generate time stamp data
##
## @param      startDate   The start date time object
## @param      endDate     The end date time object
## @param      nameOfFile  The name of file in which we want to save time stamps
## @param      incrBy      The value in hour by which we want increment time stamps
##
## @return     None
##
def generate_time_stamps(startDate, endDate, nameOfFile, incrBy = 1):

	dateList = []

	dateList.append(startDate)
	incrCounter = incrBy
	nextDate = startDate

	while(nextDate != endDate):
		nextDate = startDate + datetime.timedelta(hours=incrCounter)
		dateList.append(nextDate)
		incrCounter = incrCounter + incrBy

	with open(nameOfFile, 'w') as f:
		for i in range(len(dateList)):
			f.write("%s\n" % (dateList[i]))

if __name__ == '__main__':
	#YY-MM-DD-HH-MIMI-SESE
	# generate_interval(datetime.datetime(2017, 1, 1, 0, 0, 0), datetime.datetime(2017, 1, 2, 0, 0, 0), "DummyTest.txt", 1)
	# generate_time_stamps(datetime.datetime(2017, 1, 1, 0, 0, 0), datetime.datetime(2017, 1, 2, 0, 0, 0), "DummyTest.txt", 1)
	generate_weekly_interval(datetime.datetime(2017, 1, 1, 0, 0, 0), datetime.datetime(2017, 1, 15, 0, 0, 0), "DummyTest.txt")