import os
import sys
import datetime
import numpy as np

#give it in a list formate
#YY-MM-DD-HH-MIMI-SESE
startDate = datetime.datetime(2017, 1, 1, 0, 0, 0)
endDate = datetime.datetime(2017, 1, 2, 0, 0, 0)

dateList = []

dateList.append(startDate)
incrCounter = 1
nextDate = startDate

while(nextDate != endDate):
	nextDate = startDate + datetime.timedelta(hours=incrCounter)
	dateList.append(nextDate)
	incrCounter = incrCounter + 1

print(dateList)