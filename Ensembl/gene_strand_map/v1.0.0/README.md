# Files

- README.md
- hg19_gene_strand.txt
- md5sum.txt
- src7/create_gene_strand_file.sh
- src/get_human_pcg_annotation.py
- src/pyproject.toml
- src/uv.lock

# Origin

Gene annotations taken from ENSEMBL API

# Method

We included a python script to retrieve the gene strands.
The script downloads the annotation of all protein coding genes in a given version 
of the human genome (hg19 or hg38).

Then we keep the gene name and strand columns, sort by gene name and remove duplicates.

The script ```src/create_gene_strand_file.sh``` does this process automatically.

```
src/create_gene_strand_file.sh

# Output: ./hg19_gene_strand.txt
```

The resulting file, ```hg19_gene_strand.txt```, can be used to create the fusviz input table.

# Responsible

@jaimicore
