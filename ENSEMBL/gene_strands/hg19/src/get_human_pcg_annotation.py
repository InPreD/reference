#!/usr/bin/env python3
import argparse
import polars as pl
from pybiomart import Server
from typing import Optional


def get_human_annotations(hg_version      : str = "hg38",
                          output          : Optional[str] = None,
                          coord_include   : bool = False,
                          null_include    : bool = False,
                          length_include  : bool = False,
                          domains_include : bool = False) -> pl.DataFrame:
    """
    Retrieve human gene annotations from Ensembl BioMart.
    
    Parameters
    ----------
    hg_version : str
        Human genome version. Options: 'hg19' or 'hg38'
    output : str, optional
        Output file name to export the tables. If None, returns DataFrame without saving
    coord_include : bool, default False
        Should the output include gene coordinates (chr, start, end) ?
    null_include : bool, default False
        Should the output include entries without gene names (null) ?
    length_include : bool, default False
        Should the output include protein length information ?
    domains_include : bool, default False
        Should the output include Pfam domain information (domain IDs, start, end positions) ?
    
    Returns
    -------
    pl.DataFrame
        DataFrame with gene annotations
    
    Examples
    --------
    >>> # Use as a function
    >>> df = get_human_annotations('hg38', coord_include=True, length_include=True)
    >>> 
    >>> # Save to file with domains
    >>> df = get_human_annotations('hg38', output='annotations.txt', length_include=True, domains_include=True)
    """
    
    # ------------------- #
    # Map genome versions # 
    # ------------------- #
    
    # NOTE that the server differs according to the genome version.
    if hg_version == "hg19":
        grch_version = 37
        server = Server(host='http://grch37.ensembl.org')
    elif hg_version == "hg38":
        grch_version = 38
        server = Server(host='http://www.ensembl.org')
    else:
        raise ValueError("Invalid genome version. Use 'hg19' or 'hg38'.")

    # These queries will be restricted to human protein-coding genes.
    query_filters = {'biotype': 'protein_coding'}
    

    # ------------------ #
    # Connect to Ensembl #
    # ------------------ #
    dataset = (server.marts['ENSEMBL_MART_ENSEMBL']
                     .datasets['hsapiens_gene_ensembl']
              )
    
    
    # ------------------------------------ #
    # 1st query : gene IDs and coordinates #
    # ------------------------------------ #
    
    # Adapt this list to include the attributes you want to retrieve.
    # The attributes can be found in the Ensembl Biomart documentation.
    # NOTE: All attributes must be from the same "attribute page" in BioMart
    # Attributes like 'cds_length', 'cds_start', 'cds_end' are from a different page
    attributes = [ 'ensembl_gene_id',
                   'ensembl_transcript_id',
                   'ensembl_peptide_id',
                   'hgnc_symbol',
                   'strand',
                   'chromosome_name',
                   'transcript_start',
                   'transcript_end',
                   'gene_biotype',
                   'refseq_mrna',
                   'refseq_peptide'
                 ]    

    # First query - main attributes
    df = dataset.query(attributes = attributes,
                       filters    = query_filters
                      )
    
    # Process the main dataframe by adding proper null handling
    df = df.astype(str)
    df = pl.from_pandas(df)
    df = df.select([ pl.when(pl.col(c) == "nan")
                       .then(None)
                       .otherwise(pl.col(c))
                       .alias(c)
                    for c in df.columns
                  ])

    # Rename and select columns for 1st query dataframe
    df = df.rename({ 'Gene stable ID'           : 'gene_id',
                     'Transcript stable ID'     : 'transcript_id',
                     'Protein stable ID'        : 'peptide_id',
                     'HGNC symbol'              : 'hgnc_symbol',
                     'Chromosome/scaffold name' : 'chr',
                     'Transcript start (bp)'    : 'start',
                     'Transcript end (bp)'      : 'end',
                     'Gene type'                : 'gene_biotype',
                     'RefSeq mRNA ID'           : 'refseq_mrna',
                     'RefSeq peptide ID'        : 'refseq_peptide',
                     'Strand'                   : 'strand'})

    # Convert strand information from 1/-1 to +/-
    df = df.with_columns([
        pl.when(pl.col('strand') == '1')
          .then(pl.lit('+'))
          .otherwise(pl.lit('-'))
          .alias('strand')
    ])

    selected_cols = ['chr', 'start', 'end', 'hgnc_symbol', 'gene_id', 
                     'transcript_id', 'peptide_id',
                     'refseq_mrna', 'refseq_peptide', 'gene_biotype', 'strand']

    # ------------------------------------ #
    # 2nd query : CDS/sequence information #
    # ------------------------------------ #

    # When length_include is set to True we will calculate the protein length
    # from the CDS length (in nucleotides) retrieved from a different attribute page.
    # This is why we need a 2nd query
    if length_include:

        # Second query - CDS/sequence information (from different attribute page)
        
        attributes_seq = ['ensembl_transcript_id',
                          'cds_length'
                         ]
    
        df_seq = dataset.query(attributes = attributes_seq,
                            filters    = query_filters
                            )
        
        df_seq = df_seq.astype(str)
        df_seq = pl.from_pandas(df_seq)
        df_seq = df_seq.select([ pl.when(pl.col(c) == "nan")
                                .then(None)
                                .otherwise(pl.col(c))
                                .alias(c)
                                for c in df_seq.columns
                            ])
    
        # Rename the sequence dataframe columns
        df_seq = df_seq.rename({ 'Transcript stable ID' : 'transcript_id',
                                 'CDS Length'           : 'cds_length'
                              })
        
        # Join the two dataframes on transcript_id
        df = (df.join(df_seq, on='transcript_id', how='left')
                        .with_columns([
                            (pl.col('cds_length').cast(pl.Float64).cast(pl.Int64) // 3 - 1).alias('cds_length') ])
                    )
        
        # Update the list of selected columns
        selected_cols.append('cds_length') 


    # ----------------------------------- #
    # 3rd query : Pfam domain information #
    # ----------------------------------- #

    # When domains_include is set to True we will retrieve Pfam domain information
    # This includes domain IDs and their start/end positions on the protein
    if domains_include:

        # Third query - Pfam domain information (from different attribute page)
        
        attributes_pfam = ['ensembl_peptide_id',
                           'pfam',
                           'pfam_start',
                           'pfam_end'
                          ]
    
        df_pfam = dataset.query(attributes = attributes_pfam,
                                filters    = query_filters
                               )
        
        df_pfam = df_pfam.astype(str)
        df_pfam = pl.from_pandas(df_pfam)
        df_pfam = df_pfam.select([ pl.when(pl.col(c) == "nan")
                                   .then(None)
                                   .otherwise(pl.col(c))
                                   .alias(c)
                                   for c in df_pfam.columns
                                ])
    
        # Rename the Pfam dataframe columns
        df_pfam = df_pfam.rename({ 'Protein stable ID' : 'peptide_id',
                                   'Pfam ID'            : 'pfam_id',
                                   'Pfam start'         : 'pfam_start',
                                   'Pfam end'           : 'pfam_end'
                                })
        
        # Filter out null values before aggregating
        df_pfam = df_pfam.filter(pl.col('pfam_id').is_not_null())
        
        # Group by peptide_id and aggregate domain information into lists
        # This creates comma-separated strings of domain IDs, starts, and ends
        df_pfam_agg = (df_pfam.group_by('peptide_id')
                              .agg([
                                  pl.col('pfam_id').str.concat(delimiter=',').alias('pfam_ids'),
                                  pl.col('pfam_start').str.concat(delimiter=',').alias('pfam_starts'),
                                  pl.col('pfam_end').str.concat(delimiter=',').alias('pfam_ends')
                              ])
                      )
        
        # Join the domain information with the main dataframe
        df = df.join(df_pfam_agg, on='peptide_id', how='left')
        
        # Update the list of selected columns to include domain information
        selected_cols.extend(['pfam_ids', 'pfam_starts', 'pfam_ends'])


    # ----------------------- #
    # Filter and sort results #
    # ----------------------- #
    
    # Select and order columns
    df = df.select(selected_cols)

    # Filter to standard chromosomes
    valid_chromosomes = [str(i) for i in range(1, 23)] + ["X", "Y", "MT"]
    df = df.filter(pl.col("chr").is_in(valid_chromosomes))
    
    # Sort by chr and start pos
    df = df.sort(["chr", "start"])
    
    # Drop unwanted columns
    drop_cols = ["gene_biotype"]
    if not coord_include:
        drop_cols += ["chr", "start", "end", "strand"]
    
    df = df.drop(drop_cols)
    
    # Remove entries where refseq_mrna/refseq_peptide are empty
    if not null_include:
        df = df.drop_nulls()
    
    # -------------- #
    # Export results #
    # -------------- #
    if output is not None:
        df.write_csv(output, separator="\t")
        
    return df


def main():
    """
    Main function for CLI usage.
    """
    # -------------------- #
    # Parse CLI arguments  #
    # -------------------- #
    parser = argparse.ArgumentParser(description="Retrieve human gene annotations from Ensembl")
    
    parser.add_argument( "-g", "--hg_version",
                         required = True,
                         choices  = ["hg19", "hg38"],
                         help     = "Human genome version. Options: hg19 | hg38"
                        )
    
    parser.add_argument( "-c", "--coordinates",
                         required = False,
                         default  = False,
                         action   = "store_true",
                         help     = "Should the output include gene coordinates. Options: True | False"
                        )
    
    parser.add_argument( "-n", "--null_include",
                         required = False,
                         default  = False,
                         action   = "store_true",
                         help     = "Should the output include entries without gene names (null). Options: True | False"
                        )
    
    parser.add_argument( "-l", "--length_include",
                         required = False,
                         default  = False,
                         action   = "store_true",
                         help     = "Should the output include protein length information. Options: True | False"
                        )
    
    parser.add_argument( "-d", "--domains",
                         required = False,
                         default  = False,
                         action   = "store_true",
                         help     = "Should the output include Pfam domain information. Options: True | False"
                        )
    
    parser.add_argument( "-o", "--output",
                         required = True,
                         help = "Output file name to export the tables"
                       )
    
    args = parser.parse_args()
    
    # Call the main function with parsed arguments
    df = pl.DataFrame
    df = get_human_annotations(hg_version      = args.hg_version,
                               output          = args.output,
                               coord_include   = args.coordinates,
                               null_include    = args.null_include,
                               length_include  = args.length_include,
                               domains_include = args.domains
                              )


if __name__ == "__main__":
    main()