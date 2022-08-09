## Script for truncating SAM files to a desired coverage ##
## Usage: python3 sam_trunc.py -i <input sam> -d <maximum coverage> -o <output file name>

## This script reads in reads sequentially from a SAM file and records how many times a position has been covered by the reads
## if the position has not been covered more times than the desired coverage, then the read is written to the output


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest="input", help="Input File")
parser.add_argument("-d", "--depth", dest="depth", help="Depth", type=int)
parser.add_argument("-o", "--output", dest="out", help="Output file")
args = parser.parse_args()

sam = args.input
max_d = args.depth
out = args.out
coverage = {} #dictionary to record coverage per position
with open(sam,'r') as old_file: #open sam file
    with open(out,'w') as new_file: #open output file
        for line in old_file:
            go = True #reset go value
            if line[0] != '@': #check if its a read
                chrom = line.split('\t')[2] #get chrom
                start = int(line.split('\t')[3]) #get read start position
                length = int(line.split('\t')[8]) #get read length
                if chrom in coverage: #if that chromosome has been recorded in the coverage dic
                    for pos in range(start, start+length+1): #for each position in the read
                        try:
                            coverage[chrom][pos] += 1 #record that the position has been covered
                            if coverage[chrom][pos] > max_d: #if that position has been covered more than max d times, turn go off
                                go = False
                        except KeyError: #if that position is new, set it to 1
                            coverage[chrom][pos] = 1
                else:
                    coverage[chrom] = {start:1} #if that chrom is new, create a new key in coverage dic and record those positions
                    for pos in range(start+1, start+length+1):
                        coverage[chrom][pos] = 1
            if go: #if go is on, then write the read line to the output
                new_file.write(line)

