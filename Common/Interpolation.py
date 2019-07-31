import numpy as np

def apply_linear_interpolation(xStart, yStart, xEnd, yEnd, xDesired):
	#equation of line will be 
	#FIXME look for divide by zero here

	#compute slope of line
	#i.e. (y2 - y1)/(x2 - x1)
	slope = (yEnd - yStart)/(xEnd - xStart)
	#compute the desired y value
	#i.e y = m(x - x1) + y1
	ret = (slope*(xDesired - xStart)) + yStart
	return ret


if __name__ == '__main__':
	####################################
	a = apply_linear_interpolation(1,2,10,4,5.5)
	print(a)