#!/usr/bin/env nextflow

params.url = "https://www.ebi.ac.uk/metagenomics/api/v1/analyses"
params.biome_name = ""

process FetchData {

    input:
    val url
    val biome_name

    output:
    path "studies_or_analyses.json"

    script:
    """
    python fetch_data.py --url $url --biome_name $biome_name > studies_or_analyses.json
    """
}

workflow {
    FetchData(params.url, params.biome_name)
}

