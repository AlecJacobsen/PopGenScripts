# Script for generating a freq file for treemix from plink format files
# Inputs: the prefix for the plink files, the number of threads to use
# Assumes that individual ids follow the form [population]-[individual_number] - i.e. RosFM-1 or PlouSL-3 

import argparse
import pandas as pd
import numpy as np
from pandas_plink import read_plink1_bin
from concurrent.futures import ThreadPoolExecutor
import gzip

def gt_counts(array):
    ref = len(np.where(array == 0)[0])
    het = len(np.where(array == 1)[0])
    alt = len(np.where(array == 2)[0])
    return '%d,%d' % ((ref*2)+het,(alt*2)+het)

def counts_line(snp):
    gt_array = snps.sel(variant = snp).values
    tmp = np.empty(len(pops),dtype='U5')
    for i, pop in enumerate(pops):
        tmp[i] = gt_counts(gt_array[pops[pop]])
    return ' '.join(list(tmp)) + '\n'

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="file", help="plink file prefix")
parser.add_argument("-o", "--out", dest="out", help="output prefix")
parser.add_argument("-t", "--threads", dest="threads", help="number of threads")
args = parser.parse_args()

bed = args.file + '.bed'
bim = args.file + '.bim'
fam = args.file + '.fam'
out = args.out + '.treemix.frq.gz'
threads = int(args.threads)

print('Reading in plink file')
snps = read_plink1_bin(bed, bim, fam, verbose=False)
print('Done')

print('Parsing populations')
pops = {}
indvs = pd.Series(snps.sample.values).str.replace("\-[0-9]+$", "", regex = True)
for pop in indvs.unique():
    pops[pop] = np.where(indvs == pop)
print('Done')

print('Calculating Frequencies')
with ThreadPoolExecutor(max_workers=threads) as executor:
    freqs = executor.map(counts_line,snps.variant.values)
print('Done')

print('Writing output')
with gzip.open(out,'wb') as nf:
    nf.write((' '.join(pops.keys()) + '\n').encode())
    for freq in freqs:
        nf.write(freq.encode())
print('Done')

