# hic-noise-simulator
Python code for simulating and injecting noise to hi-c contact matrices

This tool simulates noisy Hi-C interactions from real Hi-C contact matrices and mixes the real data to noise to simulate contact matrices with known levels of noise. Two types of noise models are used to simulate Hi-C noise: genomic distance effect noise and random ligation noise. These two types of noise models are combined to yield the simualted noise. The details can be found at https://www.biorxiv.org/content/early/2017/09/14/188755

To run the noise simulator run main.py with seven arguments:

1) Input filename

The input file is text file that contains pairs of loci and the total number of Hi-C contact between the two loci. The format is explained in detail here: https://noble.gs.washington.edu/proj/fit-hi-c/software/README-latest.txt

2) chr number (without chr)

This code is run on a single intra-chromosomal(cis) Hi-C matrix corresponding to the interactions for a given chromosome. Second argument specifies the name of the chromosome. E.g. if you are processing the 1st chromosome of a given organism, the 2nd argument is '1' (without 'chr')

3) resolution of the contact matrix

The resolution of the input Hi-C matrix, in bps.

4) noisePercentage, percent noise to be injected

This argument (a float between 0 and 1) specifies what percent of noise will be injected to the real Hi-C contact matrix. For example, if this argument is 0.5, 50% noise is injected. 

5) Random ligation noise percentage

Simualted noise is a mixture of genomic distance noise and random ligation noise. This argument (a float between 0 and 1) specifies what percent of simulated noise should  consist of random ligation noise.

6) Stratum Size, number of bins to make up each strata

The number of bins that make up each strata for stratified sampling. For 40kb, 100 bin is a reasonable choice.

7) Output filename

The name of the output file the noise injected Hi-C contact matrix will be output to. The format is the same as the input format.



