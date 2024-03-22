# PopGenScripts

This repository contains a bunch of small scripts for various tasks related to population genetics and genomics analyses. The scripts were intended to be as generalized as possible, but may not work in all cases. Be sure to understand what the script is doing before fully trusting any output.

## LD Averager
Linkage disequilibrium (LD) between markers is a useful statistic for detecting evidence of selection or demographic processes in a genome. Vcftools --geno-r2 command outputs a large file of squared correlation coefficients between SNPs across a genomic window or whole genome. The ld_averager.py script takes and .geno.ld file as input and calculates the average correlation coefficient for all SNPs within a designated window size. LD averages can then be plotted along the genome.

## LD decay
Linkage disequilibrium decay, or the distribution of correlation between SNPs as a function of distance, is another useful statistic that is sensitive to demographic processes. It is also useful to calculate in order to determine a threshold of linkage for pruning SNP sets before certain analyses like PCA. Like ld_averager.py, ld_decay.py takes as input the .geno.ld file from vcftools' --geno-r2 command, and outputs the distribution of LD in 500 bp increments.

## Multimapper Density
One crucial step in the data processing steps for population genetics studies is mapping reads to a reference genome. 


--------------------------------------------------------------------------------------------------------------
## Dealing with strange ploisies

The folder MultiPloidy_VCF_tools contains scripts that handle vcf files containing individuals with various ploidies!