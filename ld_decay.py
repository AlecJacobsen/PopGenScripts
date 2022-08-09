# Script for generating the distribution of LD versus distance between sites
# Input: .ld file from vcftools 

import dask.dataframe as dd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest="input", help="input .ld file")
parser.add_argument("-o", "--output", dest="output", help="output file name")
args = parser.parse_args()

print('LD decay for ',args.input)
print('Reading File')
ld_df = dd.read_csv(args.input,sep = '\t')
print('Calculating Averages')
ld_df['diff'] = ((ld_df['POS2'] - ld_df['POS1'])/500).astype(int)*500
averages = ld_df.groupby(by = 'diff').mean()['R^2'].reset_index()
print('Writing Output')
averages.to_csv(args.output,index = False, single_file = True)
