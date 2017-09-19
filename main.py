from functions import * 
import numpy as np
import time
import os
import sys
import random
from parsers import ParseInteractionBed, getChrLen, OutInteractionFormat
from noise import shuffleMatrix, uniformMatrix, SubSampleMatrix, stratifiedSample


# Arguments
# 1) Input filename
# 2) chr number (without chr)
# 3) resolution of the contact matrix
# 4) noisePercentage, percent noise to be injected
# 5) Random ligation noise percentage
# 6) Stratum Size, number of bins to make up each strata
# 7) Output filename


#chromosome to read
filename=sys.argv[1]
chr=sys.argv[2]
resolution=int(sys.argv[3])
perNoise = float(sys.argv[4])
perRLigation = float(sys.argv[5])
stratumSize = int(sys.argv[6])
outfilename = sys.argv[7]

inputMatrix = ParseInteractionBed ( filename, chr = chr, resolution = resolution, assembly = 'hg19' )
inputCoverage =  int(np.sum(np.triu(inputMatrix)))

GDnoiseMatrix = shuffleMatrix(inputMatrix)
RLnoiseMatrix = uniformMatrix(inputMatrix,inputCoverage,bias=True)


realSampleCount = int(inputCoverage * ( 1 - float(perNoise) ) )
sinputMatrix = SubSampleMatrix(inputMatrix, subSampleN = realSampleCount )

GDSampleCount = int(inputCoverage * float(perNoise) * float(1-perRLigation) )		
sGDnoiseMatrix = SubSampleMatrix(GDnoiseMatrix, subSampleN = GDSampleCount )

RLSampleCount = int(inputCoverage * float(perNoise) * float(perRLigation) ) 
sRLnoiseMatrix = SubSampleMatrix(RLnoiseMatrix, subSampleN = RLSampleCount )

noisedMatrix = sinputMatrix + sGDnoiseMatrix + sRLnoiseMatrix

OutInteractionFormat(noisedMatrix,outfilename,chr=chr,resolution=resolution)



