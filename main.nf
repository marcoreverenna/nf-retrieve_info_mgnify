#!/usr/bin/env nextflow

// Define parameters
params.url_studies = "https://www.ebi.ac.uk/metagenomics/api/v1/studies"
params.url_analyses = "https://www.ebi.ac.uk/metagenomics/api/v1/analyses"
params.biome_name = 'example_biome'
params.experiment_type = 'example_experiment'
params.outputDir = './results'

// Process for Fetching Studies Data
process FetchStudiesData {
    output:
    path 'studies_data.json' into studiesDataChannel

    script:
    """
    python process_data.py fetch --url $params.url_studies --params biome_name=$params.biome_name --output studies_data.json
    """
}

// Process for Fetching Analyses Data
process FetchAnalysesData {
    output:
    path 'analyses_data.json' into analysesDataChannel

    script:
    """
    python process_data.py fetch --url $params.url_analyses --params biome_name=$params.biome_name,experiment_type=$params.experiment_type --output analyses_data.json
    """
}

// Process for Creating Study DataFrame
process CreateStudyDataFrame {
    input:
    path studiesData from studiesDataChannel

    output:
    path 'studies_df.csv' into studiesDfChannel

    script:
    """
    python process_data.py create_study_df --input studies_data.json --output studies_df.csv
    """
}

// Process for Creating Analysis DataFrame
process CreateAnalysisDataFrame {
    input:
    path analysesData from analysesDataChannel

    output:
    path 'analyses_df.csv' into analysesDfChannel

    script:
    """
    python process_data.py create_analysis_df --input analyses_data.json --output analyses_df.csv
    """
}

// Process for Merging DataFrames and Final Processing
process MergeAndProcessDataFrames {
    input:
    path studiesDf from studiesDfChannel
    path analysesDf from analysesDfChannel

    output:
    path 'final_output.csv'

    script:
    """
    python process_data.py merge_and_process --studies_df studies_df.csv --analyses_df analyses_df.csv --output final_output.csv
    """
}

// Define workflow 
{
    FetchStudiesData()
    FetchAnalysesData()

    CreateStudyDataFrame(studiesDataChannel.collect())
    CreateAnalysisDataFrame(analysesDataChannel.collect())

    MergeAndProcessDataFrames(studiesDfChannel.collect(), analysesDfChannel.collect())
}

