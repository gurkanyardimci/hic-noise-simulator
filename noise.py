import numpy as np
import time 
import random

def SubSampleMatrix(CM, subSampleN = 1000000, symmetric = True ):

	if subSampleN >= np.sum(np.triu(CM)) : 
		print 'Asked for ' + str(subSampleN) + 'entries, matrix has ' + str(np.sum(np.triu(CM)))
		print 'Sampling more entries than available, returning original matrix'
		return CM

	index1 = []
	index2 = []
	subCM = np.zeros((len(CM),len(CM)))

	for i in range(len(CM)):
		for k in range(i,len(CM)):
			count = int(CM[i,k])
			v1=np.empty(count); v1.fill(i)				
			v2=np.empty(count); v2.fill(k)				
			index1.extend(v1); index2.extend(v2)
	
	index1 = np.array(index1)
	index2 = np.array(index2)
	shufIndex = range(0,len(index1));	random.shuffle(shufIndex);
	subSampleIndex = np.random.choice(shufIndex,size=subSampleN,replace=False)
	index1 = index1[subSampleIndex]
	index2 = index2[subSampleIndex]

	for i in range(len(index1)):
		a = int(index1[i]); b = int(index2[i])
		subCM[a,b] = subCM[a,b] + 1

	subCM = subCM + np.triu(subCM,1).T		
	return(np.matrix(subCM))


def stratifiedSample ( V, F, strataSize = 100 ):
	N = len(V)
	V = np.array(V)
	F = np.array(F)

	strataCount = int(np.ceil(float(N) / strataSize))
	sortInd = np.argsort(F)
	strata = []
	strataMax = []

	#print '%d to stratify, %d strata to be filled' % (N,strataCount)

	
	for i in range(strataCount) :
		stratum = V [ sortInd[ (strataSize*(i) ) : (strataSize*(i+1)) ] ]
		stratumF = F [ sortInd[ (strataSize*(i) ) : (strataSize*(i+1)) ] ]
		strata.append( stratum )
		strataMax.append(max(stratumF))
		#print str(strataSize*(i)) + ' ' + str(strataSize*(i+1)) + ' ' + str(len(stratum))


	sample = []
	for i in range(len(V) ):
		if ( F[i] == 0 ) :
			sample.append (0)
		else :
			stratumInd = 0
			for k in range(strataCount) :
				#if ( F[i] >= strataMax[k] ):
				if ( F[i] <= strataMax[k] ):
					stratumInd = k
					break
			if ( stratumInd == 0 ):
				stratumInd = k
			sample.append ( np.random.choice(strata[k],size=1)[0] )

	return ( sample )

def uniformMatrix ( CM, subSampleCount = 1000000, bias = False ):
	(R,C) = np.shape(CM)
	marginal = np.sum(np.array(CM),1)
	uniSampleCM = np.matrix( np.zeros((R,C)) )
	#triuSum = sum(np.arange(R)+1)
	
	indexMap = []
	indexProb = []
	for i in range(R) :
	    	for k in range(i,R) :
			if marginal[i] != 0 and marginal[k] != 0 :
	       			indexMap.append([i,k])
				if bias :
					indexProb.append(marginal[i] * marginal[k])

	if bias :
		totalProb = float(sum(indexProb))
		indexProb = [ iP / totalProb for iP in indexProb ]
		triuSample = np.random.choice(len(indexMap),subSampleCount,p=indexProb)
	else :
		triuSample = np.random.choice(len(indexMap),subSampleCount)
        	
	for s in triuSample :
	    	(i,k) = indexMap[s]
    		uniSampleCM[i,k] += 1
	uniSampleCM += np.transpose(np.triu(uniSampleCM,1))

	return (uniSampleCM)


def shuffleMatrix ( CM, stratumSize = 50 ):
	#Convert to integer
	CM = CM.astype(int)
	#Get marginals and number of rows
	contactSum = np.sum(np.array(CM),1)

	print contactSum 
	print contactSum[1]
	print contactSum[1] * contactSum[2]
	N = len(CM)

	# For matrix entry Mik, store Marginal i * Marginal k in CountByDist
	# and the Mik itself in matrixByDist
	countByDist = []
	matrixByDist = []
	for i in range(0,N):
		for k in range(i,N):
			dist = k-i
			if ( len(countByDist)-1 < dist ):
				countByDist.append( [ float(contactSum[i]) * contactSum[k] ] )
				matrixByDist.append( [ int( CM[i,k] ) ] )
			else:
				countByDist[dist].append( float(contactSum[i]) * contactSum[k] )
				matrixByDist[dist].append( int( CM[i,k] ) )
	
	noiseMatrix = np.zeros((N,N))
	t1 = time.time()

	for i in range(len(matrixByDist)):
	#for i in range(1):
		#print "dist is %d" % (i)
		thisSample = stratifiedSample(matrixByDist[i],countByDist[i],stratumSize)
		for k in range(len(thisSample)):				
			noiseMatrix[k,k+i] = thisSample[k]
		
	for i in range(0,N):
		for k in range(i,N):
			noiseMatrix[k,i] = noiseMatrix[i,k]
	
	t2 = time.time()
	print 'Time is %f' % (t2-t1)
	return ( noiseMatrix )
	

