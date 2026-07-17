# Files

- README.md
- cancer_susceptibility_genes.csv
- md5sum.txt

# Origin

[Germline-focused analysis of tumour-detected variants in 49,264 cancer patients: ESMO Precision Medicine Working Group recommendations](https://doi.org/10.1016/j.annonc.2022.12.003)

# Method

The table in Box 1. in the paper was manually parsed into a machine-readable format by placing all gene names into the column `Gene`, the column `CSG actionability class` was translated (`Most`>`MA-CSG` (most actionable cancer susceptibility gene); `High`>`HA-CSG` (highly actionable cancer susceptibility gene); `Standard`>`SA-CSG` (standardly actionable cancer susceptibility gene)) and placed into the column `Actionability`, and the columns `All ages` and `Age <30` were translated to `Allages` and `Age<30`, respectively, and merged into the column `Age`. The table was sorted according to gene name.

# Responsible
@tinavisnovska
