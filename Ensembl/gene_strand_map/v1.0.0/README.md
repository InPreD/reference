# Files

- README.md
- hg19_gene_strand.txt
- md5sum.txt
- src7/create_gene_strand_file.sh
- src/get_human_pcg_annotation.py
- src/pyproject.toml
- src/uv.lock

# Origin

Gene annotations retrieved from [Ensembl REST API](https://rest.ensembl.org/) via the [*pybiomart*](https://jrderuiter.github.io/pybiomart/) python package.

# Method

We included a python script to retrieve the gene strands in human genome.
The script downloads the annotation of all protein coding genes in a given version 
of the human genome (hg19 or hg38).

Then we keep the gene name and strand columns, sort by gene name and remove duplicates.

The script ```src/create_gene_strand_file.sh``` does this process automatically.



```
# Launch the script to get human protein coding gene (pcg) annotation
# -g : genome version (hg19 or hg38)
# -c : include coordinates (chr, start, end, strand) in the output file


for hgv in hg19 hg38
do
    tmp_out=${hgv}_gene_strand_map.txt.tmp

    # Remove the tmp suffix
    gs_out=${hgv}

    uv run get_human_pcg_annotation.py \
        -g ${hgv}                      \
        -c                             \
        -o ${tmp_out}

    # Parse the output file to create a gene strand file 
    more ${tmp_out} | cut -f4,10 | sort | uniq > hg19_gene_strand.txt

    # Move gene-strand file to the output directory
    rm hg19_pcg_annotation.txt
    mv hg19_gene_strand.txt ../
done




```

**NOTE:** the command above assumes user run it via *uv*, see installation instructions [here]().

# Responsible

@jaimicore
