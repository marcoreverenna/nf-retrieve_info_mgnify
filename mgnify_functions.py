#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for retrieving data using MGnify

__author__ = Marco Reverenna
__copyright__ = Copyright 2023-2024
__version__ = 1.0
__maintainer__ = Marco Reverenna
__email__ = marcor@dtu.dk
__status__ = Dev
"""

import requests
import pandas as pd
import json

def fetch_studies_or_analyses_info(url, params):
    '''Compressed function to retrieve information from MGnify API.'''

    all_studies_or_analyses = []
    page = 1

    while True:
        print(f"Retrieving data for page {page}...")
        response = requests.get(url, params={**params, "page": page})

        if response.status_code != 200:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            break

        data = response.json()
        all_studies_or_analyses.extend(data.get("data", []))
        page_info = data.get("meta", {}).get("pagination", {})
        page += 1

        if page > page_info.get("pages", 0):
            break

    print("Data retrieval complete.")
    return all_studies_or_analyses


def fetch_data_from_api(url, params):
    '''Fetch data from API'''
    response = requests.get(url, params=params)
    return response.json()

def dump_data_to_json(data, file_path):
    '''Dump data to a JSON file'''
    with open(file_path, "w") as outfile:
        json.dump(data, outfile)

def create_study_df(data):
    '''Create DataFrame for study data'''
    study_list = [{
        "study_id": study["id"],
        "study_name": study["attributes"].get("study-name"),
        "n_samples": study["attributes"].get("samples-count"),
        "bioproject": study["attributes"].get("bioproject"),
        "centre_name": study["attributes"].get("centre-name"),
        "biomes": ", ".join([biome["id"] for biome in study["relationships"]["biomes"]["data"]]),
    } for study in data]
    return pd.DataFrame(study_list)

def create_analysis_df(data):
    '''Create DataFrame for analysis data'''
    analysis_list = [{
        "analysis_id": analysis["attributes"]["accession"],
        "sample_id": analysis["relationships"]["sample"]["data"]["id"] if "sample" in analysis["relationships"] else "",
        "assembly_run_id": analysis["relationships"]["run"]["data"]["id"] if "run" in analysis["relationships"] else "",
        "experiment_type": analysis["attributes"]["experiment-type"],
        "pipeline_version": analysis["attributes"]["pipeline-version"],
        "study_id": analysis["relationships"]["study"]["data"]["id"] if "study" in analysis["relationships"] else "",
        "instrument_platform": analysis["attributes"]["instrument-model"]
    } for analysis in data]
    return pd.DataFrame(analysis_list)

def get_studies_and_analyses_summary(biome_name, experiment_type):
    '''Function to obtain a summary of MGnify studies and analyses info for a given biome and data type'''
    # URLs for the API requests
    url_studies = "https://www.ebi.ac.uk/metagenomics/api/v1/studies"
    url_analyses = "https://www.ebi.ac.uk/metagenomics/api/v1/analyses"

    # Fetching studies data
    studies_data = fetch_data_from_api(url_studies, {'biome_name': biome_name})
    print("Studies request complete.")
    dump_data_to_json(studies_data, "../Output/Mgnify_studies.json")

    # Fetching analyses data
    analyses_params = {
        "biome_name": biome_name,
        "experiment_type": experiment_type,
        "include": "downloads"
    }
    analyses_data = fetch_data_from_api(url_analyses, analyses_params)
    print("Analyses request complete.")
    dump_data_to_json(analyses_data, "../Output/Mgnify_analyses.json")

    # Creating DataFrames
    df_studies = create_study_df(studies_data)
    df_analyses = create_analysis_df(analyses_data)

    # Merging the DataFrames
    df_analyses_def = df_analyses.merge(df_studies, on="study_id", how="left")

    # Rearrange the columns
    column_order = ['analysis_id',
                    'sample_id',
                    'assembly_run_id',
                    'experiment_type',
                    'pipeline_version',
                    'instrument_platform',
                    'study_id',
                    'bioproject',
                    'study_name',
                    'n_samples',
                    'centre_name',
                    'biomes'
                   ]
    df_analyses_def = df_analyses_def[column_order]
    return (df_analyses_def, df_studies)

def get_results_info_from_MGnifystudy(study_accession):
    '''Function to retrieve information about results for a given MGnify study
    Input: study_accession (str) - MGnify study accession for the GET request, e.g. "MGYS00001392"
    Output: results_MGnify_study (json) - json file with the information of the results for the MGnify study'''
    
    base_url = "https://www.ebi.ac.uk/metagenomics/api/v1/studies"
    endpoint = f"{base_url}/{study_accession}/downloads"

    print(f"Making GET request to: {endpoint}")
    response = requests.get(endpoint)

    if response.status_code == 200:
        results_MGnify_study = response.json()
        print("GET request successful.")

        return results_MGnify_study
    else:
        print(f"Error: {response.status_code}")
        return None

def download_and_save_MGnifystudy_results(url, file_name, download_folder):
    '''Function to download and save results for a given MGnify study
    Input: url (str) - URL for the GET request, 
           file_name (str) - results file name, e.g. taxonomic assignments
           download_folder (str) - path for the download folder
    Output: void function, it does not have a return value, but downloads and saves the desired results for the MGnify study'''

    file_path = os.path.join(download_folder, file_name)
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"File '{file_name}' downloaded and saved in '{download_folder}'.")
    else:
        print(f"Failed to download file from {url}. Status code: {response.status_code}")


def make_api_request(endpoint, params):
    '''Function to make an API request and return the JSON response'''
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def get_paginated_results(endpoint):
    '''Function to handle paginated results from an API request'''
    initial_response = make_api_request(endpoint, params={'page': 1})
    if initial_response:
        total_pages = initial_response["meta"]["pagination"]["pages"]
        all_samples = initial_response["data"]

        for page in range(2, total_pages + 1):
            print(f"Retrieving data for page {page}/{total_pages}")
            response = make_api_request(endpoint, params={'page': page})
            if response:
                all_samples.extend(response["data"])
            else:
                print(f"Failed to retrieve data for page {page}.")
                break

        return all_samples
    else:
        return []

def get_samples_metadata_from_MGnifystudy(study_accession):
    '''Function to retrieve metadata for all samples in a given MGnify study'''
    base_url = "https://www.ebi.ac.uk/metagenomics/api/v1/studies"
    endpoint = f"{base_url}/{study_accession}/samples"

    print(f"Making GET request to: {endpoint}")
    all_samples = get_paginated_results(endpoint)

    if all_samples:
        print("GET request successful. Data retrieval complete.")
    else:
        print("Failed to retrieve data.")

    return all_samples

# Usage
# samples_metadata = get_samples_metadata_from_MGnifystudy("MGYS00001392")

def extract_column_names(input_file, output_name, output_directory):
    """ This function creates a txt file with the IDs of a specific ACCESSION of MGnify.

    Args:
        input_file (_tsv_): file which contains the IDs of the ACCENSION
        output_name (_txt_): file name which contains all the IDs
        output_directory (str): directory to store the output file
    """

    full_output_path = os.path.join(output_directory, output_name)

    with open(input_file, 'r') as file:
        column_names = file.readline().strip().split('\t')[1:]
        # exclude the first column considering from the second and so on
        with open(full_output_path, 'w') as id_file:
            id_file.write('\n'.join(column_names))


def download_files_from_list(server, input_ids_file, remote_directory, local_directory):
    """ This function downloads fatsq file given a txt file wich contains the IDs.

    Args:
        server (_str_): server address (first part of the path)
        input_ids_file (_file_txt_): file which contains a list of IDs obtained from an ACCESSION
        remote_directory (_str_): path of the folder where are stored the fastq files
        local_directory (_str_): path to your local directory which contains script and data
    """

    try:
        ftp = FTP(server)
        ftp.login()

        with open(input_ids_file, 'r') as id_file:
            ids = id_file.readlines()

            for id_name in ids:
                id_name = id_name.strip()
                folder_name = id_name[:6] 
                
                remote_path = f"{remote_directory}/{folder_name}/{id_name}/"
                local_path = f"{local_directory}/{folder_name}/{id_name}/"
                
                os.makedirs(local_path, exist_ok=True)

                ftp.cwd(remote_path)

                files_to_download = ftp.nlst()

                for file in files_to_download:
                    with open(os.path.join(local_path, file), 'wb') as local_file:
                        ftp.retrbinary('RETR ' + file, local_file.write)
                    print(f"File {file} successfully downloaded in {local_path}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ftp.quit()
