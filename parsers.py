import numpy as np
import gzip

def getChrLen ( chr = 'chr1', assembly = 'hg19' ):
	chrsizes = np.loadtxt(assembly + '.chromsizes.txt',dtype={'names': ('chr','len'),'formats':('S6','i4')} )
	for i in range(len(chrsizes)):
		#print chrsizes[i,]
		if ( chrsizes[i][0] == chr ):
			return (chrsizes[i][1] )

def ParseInteractionBed ( filename, chr, chr2 = "", resolution = 10**6, assembly = 'hg19', header = False, columnIndex = 4, isInt = True, zeros = True ):
	if chr2 == "" :
		chr2 = chr
	chrLen1 = getChrLen(chr,assembly=assembly)
	chrLen2 = getChrLen(chr2,assembly=assembly)
	N1 = chrLen1 / resolution + 1
	N2 = chrLen2 / resolution + 1
	if zeros :
		M = np.matrix( np.zeros((N1,N2)) )
	else :
		M = np.matrix( np.ones((N1,N2)) )

	flip = False
	if chr2 < chr :
		flip = True

	if filename[-3:] == '.gz' :
		file = gzip.open(filename)
	else :
		file = open(filename)
	if header :
		file.readline()

	for line in file:
		line.strip()
                tokens = line.split()
		if flip == False :
			C1 = tokens[0]; C2 = tokens[2]
	       	        i = int(tokens[1]); j = int(tokens[3])
		else :
			C1 = tokens[2]; C2 = tokens[0]
	       	        i = int(tokens[3]); j = int(tokens[1])
		if isInt :
	               	c = int(float(tokens[columnIndex]))
		else :
	               	c = float(tokens[columnIndex])
		
			
		if C1 == chr and C2 == chr2 :
	       	        M [ i / resolution, j / resolution ] = c
        	       	if chr == chr2 :
				M [ j / resolution, i / resolution ] = c

	#rowSums = sum(M)
	file.close()
	return(M)


def OutInteractionFormat ( CM, filename, chr = 'nochr', resolution = 10**6 ):
	if ( chr == 'nochr' ):
		print('chromosome no not specified, exiting')
		exit(1)

	out = open(filename,'w')
	for i in range(len(CM)):
		for k in range(len(CM)):
			if ( CM[i,k] > 0 ):
				firstmid = i * resolution + resolution / 2
				secondmid = k * resolution + resolution / 2
				out.write ( "%s\t%d\t%s\t%d\t%d\n" % (chr,firstmid,chr,secondmid,CM[i,k]) )
	out.close()

