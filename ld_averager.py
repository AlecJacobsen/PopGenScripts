## Program for averaging LD values in windows output by vcftools --geno-r2 command
## Inputs: input .ld file from vcftools, Window size for averageing values


import pandas as pd
import dask.dataframe as dd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest="input", help="input .ld file")
parser.add_argument("-o", "--output", dest="output", help="output file name")
parser.add_argument("-w", "--window", dest="window", help="window size")
args = parser.parse_args()

window = int(args.window)

ld_df = dd.read_csv(args.input,sep = '\t')

print('Getting windows')
ld_df['win_start'] = (ld_df['POS1']/window).astype(int)
ld_df['win_end'] = (ld_df['POS2']/window).astype(int)

print('Excluding out of window values')
ld_df = ld_df[ld_df['win_start'] == ld_df['win_end']]

print('Averaging within windows')
averages = ld_df.groupby(by=['CHR','win_start']).mean()['R^2'].reset_index()
averages['POS1'] = averages['win_start'] * window
averages['POS2'] = averages['POS1'] + window
averages_formatted = averages[['CHR','POS1','POS2','R^2']]

print('Writing output')
averages_formatted.to_csv(args.output,index = False,single_file = True)
