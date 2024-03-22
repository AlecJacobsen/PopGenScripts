# MultiPloidy_VCF_tools

These scripts were designed to deal with vcf that contain individuals with different ploidies!



## set_hetero_haploid_to_missing

This tool deals sets the heterozygous positions of haploid indivisuals to missing.
Necessary inputs:

 * A VCF file

 * A list of the haploid individuals in the vcf file. One individual per line.
  
 * The number of header lines in the vcf file.
  
Usage: set_hetero_haploid_to_missing.py -vcf file.vcf -l list_of_haploids_in_vcf.txt -r number_of_vcf_heder_lines_minus_1

Comments:

This script can handle multiallelic positions. However The vcf file should have only the genotype values ( bcftools query can be used to optain such a vcf file). 
