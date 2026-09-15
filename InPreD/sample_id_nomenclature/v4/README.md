# Files

- README.md
- nomenclature.yaml
- md5sum.txt

# Origin

InPreD/IMPRESS

# Method

`nomenclature.yaml` contains rules on how to name samples within InPreD/IMPRESS depending on any information deemed relevant by the different InPreD nodes (hospitals). The file is manually curated and will be updated if any of the selected `choices` are extended. The file contains the sample id `format`, regular expression for python and the different `choices` for each part of the sample id `format`. Each part contains the `format` letter `code` and parts with distinct choices all of the possible choices. For `sample_type_code`, the choices are divided into two main categories with subcategories. The `tumor_site` code is based on [PCGR](https://sigven.github.io/pcgr/articles/running.html#tumor-site) which was extended with `00` corresponding to `Cancer origo incerta` and `XX` for `Unknown`. The value `0` was excluded.

# Responsible

@marrip @danielvo
