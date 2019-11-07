import numpy as np

def nonlin(x, deriv=False):
	if(deriv==True):
 		return (x*(1-x))

  	return 1/(1+np.exp(-x))

def ReadFileaAndReturnArray(filename, row, col):
	file = open(filename,"r")
	filestring = file.read()
	l = []
	for t in filestring.split():
		try:
			l.append(int(t))
		except ValueError:
			pass
	array = np.asarray(l)
	array = array.reshape(row,col)
	return array

def ArraySplit(array, RowLow, RowHigh, ColLow, ColHigh):
	SplitArray = []
	for row in range(RowLow, RowHigh):
		for col in range(ColLow, ColHigh):
			SplitArray[row][col] = array[row][col]
	return SplitArray

X = ReadFileaAndReturnArray('data.txt', 4, 3)
print X
X = ArraySplit(X, 0, 4, 0, 2)
print X
x = np.array([[0,0,1],
 	[0,1,1],
 	[1,0,1],
 	[1,1,1]])

y = np.array([[0],[1],[1],[0]])

#seed

np.random.seed(1)

#synapses

syn0 = 2*np.random.random((3,4)) - 1
syn1 = 2*np.random.random((4,1)) - 1

#traning

for j in xrange(60000):

	#layers
	l0 = x
	l1 = nonlin(np.dot(l0,syn0))
	l2 = nonlin(np.dot(l1,syn1))

	#backpropagation
	l2_error = y - l2
	if (j%10000) == 0:
		print 'Error:' + str(np.mean(np.abs(l2_error)))

	l2_delta = l2_error * nonlin(l2, deriv=True)
	l1_error = l2_delta.dot(syn1.T)
	l1_delta = l1_error * nonlin(l1, deriv=True)

	#update our synapses
	syn1 += l1.T.dot(l2_delta)
	syn0 += l0.T.dot(l1_delta)

print 'Output after training'
print l2
