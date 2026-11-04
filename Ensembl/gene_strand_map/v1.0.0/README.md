# Files

- README.md
- hg19_gene_strand_map.txt
- hg38_gene_strand_map.txt
- md5sum.txt
- src/get_human_pcg_annotation.py
- src/pyproject.toml
- src/uv.lock
- src/.gitignore

# Origin

Gene annotations retrieved from [Ensembl REST API](https://rest.ensembl.org/) via the [*pybiomart*](https://jrderuiter.github.io/pybiomart/) python package.

**NOTE:** it may happen that the Ensembl web service is down (for maintenance or any other inconvenience), it doesn't happen often but it is always better to check whether it is available. Check the status of the server [here](https://status.ensembl.org/).

# Method

We included the python script to retrieve the gene strands in human genome.
The script downloads the annotation of all protein coding genes in a given version 
of the human genome (hg19 or hg38).

Then we keep the gene name and strand columns, sort by gene name and remove duplicates.

The following chunk of code shows how to reproduce the results.

```bash
# Launch the script to get human protein coding gene (pcg) annotation
# The code assumes user is in the folder: Ensembl/gene_strand_map/v.1.0.0/src
# -g : genome version (hg19 or hg38)
# -c : include coordinates (chr, start, end, strand) in the output file

for hgv in hg19 hg38
do
    tmp_out=${hgv}_gene_strand_map.txt.tmp
    out_file=$(echo "${tmp_out}" | sed 's/\.tmp//')

    uv run get_human_pcg_annotation.py \
        -g ${hgv}                      \
        -c                             \
        -o ${tmp_out}

    # Parse the output file to create a gene strand file 
    more ${tmp_out} | cut -f4,10 | sort | uniq > ${out_file}

    # Move gene-strand file to the output directory
    rm ${tmp_out}
    mv ${out_file} ../
done
```

**NOTE:** the command above assumes the user runs the *python* script it via *uv*, see installation instructions [here](https://docs.astral.sh/uv/).

# Responsible

@jaimicore
