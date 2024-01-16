import requests
import json
import pandas as pd

# Your functions here (fetch_data_from_api, dump_data_to_json, 
create_study_df, etc.)

def main(biome_name, experiment_type):
    # Your logic for calling the functions and processing the data
    # For example: get_studies_and_analyses_summary(biome_name, 
experiment_type)

if __name__ == "__main__":
    import sys
    biome_name = sys.argv[1]
    experiment_type = sys.argv[2]
    main(biome_name, experiment_type)

