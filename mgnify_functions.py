#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for retrieving data using MGnify

__author__ = Marco Reverenna, Sebastian Alaya Ruano 
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


def fetch_and_process_studies(url, params):
    '''Fetch and process studies data.'''
    
    all_studies_data = fetch_studies_or_analyses_info(url, params)
    print("Studies request complete.")

    # Export to JSON
    with open("../Output/Mgnify_studies.json", "w") as outfile:
        json.dump(all_studies_data, outfile)

    # Process data into DataFrame
    study_list = [{
        "study_id": study["id"],
        "study_name": study["attributes"].get("study-name"),
        "n_samples": study["attributes"].get("samples-count"),
        "bioproject": study["attributes"].get("bioproject"),
        "centre_name": study["attributes"].get("centre-name"),
        "biomes": ", ".join([biome["id"] for biome in study["relationships"]["biomes"]["data"]])
    } for study in all_studies_data]

    return pd.DataFrame(study_list)

