# Files

- README.md
- tso500_file_paths.yaml
- md5sum.txt

# Origin

https://github.com/InPreD/tsoppy/discussions/13
https://github.com/InPreD/tsoppy/discussions/14
https://github.com/InPreD/tsoppy/discussions/15
https://github.com/InPreD/tsoppy/discussions/17
https://github.com/InPreD/tsoppy/discussions/19
https://support.illumina.com/content/dam/illumina-support/documents/documentation/software_documentation/trusight/trusight-oncology-500/1000000137777_02_tso-500-local-app-v2_2_1-user-guide.pdf
https://help.tso500software.illumina.com/dragen-tso-500-guides/dragen-tso-500-v2.6/analysis-output

# Method

According to the [discussion on github](https://github.com/InPreD/tsoppy/discussions), the output files from the different workflow types and versions were grouped into categories if the format and contained information were the same or similar. In case of information being stored differently for different workflow types and versions, the files were given their own category. Category names were generated following these rules:

1. [PascalCase](https://stringcase.org/cases/pascal/) and [camelCase](https://stringcase.org/cases/camel/) is converted to [snake_case](https://stringcase.org/cases/snake/). (e.g. `SampleSheet` -> `sample_sheet`)
1. Convert upper case abbreviations to lower case. (e.g. `TMB` -> `tmb`)
1. Non-alphanumeric characters are converted to `_`. (e.g. `.` -> `_`)
1. Leading and trailing `_` are removed. (e.g. `_cnv_vcf_gz` -> `cnv_vcf_gz`)
1. If the file name for all workflow type and version combinations is the same it is used as the category name. (e.g. `metrics_output_tsv`)
1. If the file suffix (after sample id) for all workflow type and version combinations is the same it is used as the category name. (e.g. `all_fusions_csv`)
1. If the file suffix (after sample id) for all workflow type and version combinations contains the same substrings the substrings are concatenated using `_` and they are used as the category name. (e.g. `sample_sheet_csv`)
1. If the file suffix (after sample id) for all workflow type and version combinations is shorter than 10 characters the second level directory name is considered, treated similar to the suffix and used as the category name. (e.g. `rna_splice_variant_calling_tsv`)
1. If none of the rules can be applied a descriptive category in snake_case is used based on the content and format of the files. (e.g. `small_variant_genome_vcf`)

Each category contains the relevant workflow type and version identifiers as keys and the relative file path (starting from the workflow's main output directory) as values, either represented as glob strings (precise path or glob pattern) or format strings (containing `{sample_id}` or `{pair_id}` as placeholders for the sample or pair id, respectively). The corresponding type (`glob_string`, `format_string`) is specified under `type`. 

# Responsible

@marrip @danielvo
