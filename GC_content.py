#!python3
#########################################
# GC content through genome over window #
# DT 22/03/2024                         #
#########################################

# Import necessary modules
from Bio import SeqIO
import pandas as pd
import numpy as np
import argparse
from tqdm import tqdm

## >><<>><<>><<>><<>><<>><<>><<

# Create parser, Add arguments 

parser = argparse.ArgumentParser(description='Get the GC content of a genome in windows')
parser.add_argument('-G','--genome', type=str, help='Input reference fasta', required=True)
parser.add_argument('-w','--window',type=int, help='Window size', required=True)
parser.add_argument('-s','--step', type=int, help='Window step', required=True)
parser.add_argument('-o','--output', type=str, help='Output file name', required=True)
args = parser.parse_args()

# >><<>><<>><<>><<>><<>><<>><<

# Main body


#Define function(get series of sequences)
def chunks(seq, win, step):
	seqlen = len(seq)
	for i in range(0,seqlen,step):
		j = seqlen if i+win>seqlen else i+win
		yield seq[i:j]
		if j==seqlen:
			break
#open fasta
for reference in SeqIO.parse(args.genome, 'fasta'):
	seq = reference.seq
	#print(reference.id, file=open("EL10_2_final_polished_GC_cont_10kb.txt", "a"))
	for number, subseq in enumerate(chunks(seq, win=args.window, step=args.step)):
		X = subseq.count('C')
		Y = subseq.count('G')
		end=(number+1)*args.window
		start=end-(args.window - 1)
		k= (X + Y)/100
		print(reference.id,start,end,k,file=open(args.output, "a"), sep="\t")
	print('Number of windows per chromosome', 'lenhth of chromosome')
	print(number, len(seq))
