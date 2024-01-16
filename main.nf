#!/usr/bin/env nextflow

nextflow.enable.dsl=2

// Define parameters
params.url_studies = "https://www.ebi.ac.uk/metagenomics/api/v1/studies"
params.url_analyses = "https://www.ebi.ac.uk/metagenomics/api/v1/analyses"
params.biome_name = 'example_biome'
params.experiment_type = 'example_experiment'
params.outputDir = './results'

// Process for Fetching Studies Data
process FetchStudiesData {
    output:
    path 'studies_data.json'

    script:
    """
    python process_data.py fetch --url $params.url_studies --params biome_name=$params.biome_name --output studies_data.json
    """
}

// Process for Fetching Analyses Data
process FetchAnalysesData {
    output:
    path 'analyses_data.json'

    script:
    """
    python process_data.py fetch --url $params.url_analyses --params biome_name=$params.biome_name,experiment_type=$params.experiment_type --output analyses_data.json
    """
}

// Process for Creating Study DataFrame
process CreateStudyDataFrame {
    input:
    path studiesData

    output:
    path 'studies_df.csv'

    script:
    """
    python process_data.py create_study_df --input studies_data.json --output studies_df.csv
    """
}

// Process for Creating Analysis DataFrame
process CreateAnalysisDataFrame {
    input:
    path analysesData

    output:
    path 'analyses_df.csv'

    script:
    """
    python process_data.py create_analysis_df --input analyses_data.json --output analyses_df.csv
    """
}

// Process for Merging DataFrames and Final Processing
process MergeAndProcessDataFrames {
    input:
    path studiesDf 
    path analysesDf

    output:
    path 'final_output.csv'

    script:
    """
    python process_data.py merge_and_process --studies_df studies_df.csv --analyses_df analyses_df.csv --output final_output.csv
    """
}

// Define workflow 

workflow {
    studiesData = FetchStudiesData()
    analysesData = FetchAnalysesData()

    CreateStudyDataFrame(studiesData)
    CreateAnalysisDataFrame(analysesData)
}

