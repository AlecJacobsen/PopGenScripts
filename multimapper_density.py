## Program for calculating multimapper density in windows from bam files
## Requires samtools to be installed and in PATH variable
## Inputs: list of bam files, window size, output file name
## Optional inputs: Region to calculate windows within, output an average across bams
## Region format: chr:start-end

import pandas as pd
import glob
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input bams", required = True, nargs='+')
parser.add_argument("-r", "--region", help="Region to calculate density within")
parser.add_argument("-w", "--window", help="Window size", required = True)
parser.add_argument("-o", "--output", help="Output file name", required = True)
parser.add_argument("-a", "--average", action = "store_true", help="When included, the average across samples is output - default output is counts per individual")
args = parser.parse_args()

window = int(args.window)

bam_files = args.input
for i, file in enumerate(bam_files):
    print(file)
    if args.region:
        positions = subprocess.check_output(['samtools view %s "%s" | grep "XA:Z" | cut -f 3-4' % (file,args.region)], shell = True).decode()
    else:
        positions = subprocess.check_output(['samtools view %s | grep "XA:Z" | cut -f 3-4' % file], shell = True).decode()
    chrom = []
    pos = []
    for line in positions.strip('\n').split('\n'):
        try:
            chrom.append(line.split('\t')[0])
            pos.append(line.split('\t')[1])
        except IndexError:
            print(line)
    df = pd.DataFrame({'chrom':chrom,'pos':pos})
    df['window'] = [int(x/window)*window for x in df.pos.astype(int)]
    counts = df.groupby(['chrom','window'],as_index = False).count().rename({'pos':file.split('.')[0]}, axis = 1)
    if i == 0:
        counts_df = counts
    else:
        counts_df = pd.merge(counts_df, counts, how = 'outer', on = ['window','chrom']).fillna(0)
if args.average:
    counts_df = pd.DataFrame({'chrom':counts_df.chrom,'window':counts_df.window,'average':counts_df.iloc[:,2:].mean(axis = 1)})

counts_df.to_csv(args.output, index = None)

