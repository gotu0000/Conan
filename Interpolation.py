import numpy as np

def apply_linear_interpolation(xStart, yStart, xEnd, yEnd, xDesired):
	# print(xStart,yStart)
	# print(xDesired)
	# print(xEnd, yEnd)

	#equation of line will be 
	#FIXME look for divide by zero here
	slope = (yEnd - yStart)/(xEnd - xStart)
	ret = (slope*(xDesired - xStart)) + yStart
	return ret


if __name__ == '__main__':
	a = apply_linear_interpolation(1,2,10,4,5.5)
	print(a)