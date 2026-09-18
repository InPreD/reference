# Files

- README.md
- nomenclature.yaml
- md5sum.txt

# Origin

InPreD/IMPRESS

# Method

The `nomenclature.yaml` document contains rules on how to construct IDs for InPreD samples. The intention was to:

1. standardize all sample IDs within the InPreD project
2. ensure that the ID format embeds as much relevant meta-information as possible and practical
3. provide a format that would be short and yet human-readable

The file is manually curated and the lists of recognized value (`enum`) will be updated as necessary (e.g., whenever a new type of assay becomes adopted by InPreD). The file contains the sample ID `format` description, as well as Python regular expression(s) that match valid sample IDs. Each `element` of the sample ID `format` is represented by a unique `format_substring` and a set of valid recognized values (`enum`). In case of the `sample_type_code` element, `enum` is divided into two main categories (tumor/`T` and normal/`N`). The `tumor_site` element `enum` is based on values permissible for [PCGR](https://sigven.github.io/pcgr/articles/running.html#tumor-site)'s `--tumor_site` parameter. In the context of InPreD, value `0`/`00` is understood as `Cancer origo incerta` (rather than PCGR's `Any`). The nomenclature also allows for value of `XX` in cases where the tumor site is not known to the author of the sample ID at time of the sample ID creation (while `Cancer origo incerta` should be used in case of a lacking medical diagnosis).

# Responsible

@marrip @danielvo
