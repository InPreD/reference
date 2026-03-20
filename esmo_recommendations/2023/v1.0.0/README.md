
This folder contains data from the "ESMO recommendations 2023 paper"
used by [tsoppy](https://github.com/InPreD/tsoppy) in the functionality
generating table of mutations present in cancer susceptibility genes.
At this point, variants in the 40 genes from Box1 on page 222 are used.

# Files

- README.md
- cancer_susceptibility_genes.csv
- md5sum.txt

# Origin

[Germline-focused analysis of tumour-detected variants in 49,264 cancer patients: ESMO Precision Medicine Working Group recommendations](https://doi.org/10.1016/j.annonc.2022.12.003)

# Method

The table in Box 1. in the paper was manually parsed into a machine-readable format by placing all gene names into the column `Gene`, the column `CSG actionability class` was translated (`Most`>`MA-CSG`; `High`>`HA-CSG`; `Standard`>`SA-CSG`) and placed into the column `Actionability`, and the columns `All ages` and `Age <30` were translated to `All` and `Age<30`, respectively, and merged into the column `Age`. The table was sorted according to gene name.

# Responsible
@tina
