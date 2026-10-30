#!/bin/bash
set -e

# Launch the script to get human protein coding gene (pcg) annotation
# -g : genome version (hg19 or hg38)
# -c : include coordinates (chr, start, end, strand) in the output file
uv run get_human_pcg_annotation.py \
    -g hg19                        \
    -c                             \
    -o hg19_pcg_annotation.txt

# Parse the output file to create a gene strand file 
more hg19_pcg_annotation.txt | cut -f4,10 | sort | uniq > hg19_gene_strand.txt

# Move gene-strand file to the output directory
rm hg19_pcg_annotation.txt
mv hg19_gene_strand.txt ../