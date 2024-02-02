#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This python script downloads fastq file given an ACCESSION related to MGnify.

__author__ = Marco Reverenna
__copyright__ = Copyright 2024-2025
__date__ = 2 Dec 2023
__maintainer__ = Marco Reverenna
__email__ = marcor@dtu.dk
__status__ = Dev
"""

import os
import json
import argparse
from ftplib import FTP
#from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
# ftplib allows to transfer files between your computer and a server


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
            # writes all the columns on txt file

    print(f"Processing {input_file}, outputting {output_name} in {output_directory}")
    print(f"File created in {output_directory}")


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
                        # wb = write - binary 
                        ftp.retrbinary('RETR ' + file, local_file.write)
                        # retrbinary = download files in binary format (retrieve binary)
                    print(f"File {file} successfully downloaded in {local_path}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ftp.quit()





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract columns from a file")
    parser.add_argument("input_file", type=str, help="Input file path")
    parser.add_argument("output_name", type=str, help="Output file name")
    parser.add_argument("output_directory", type=str, help="Output directory")

    args = parser.parse_args()

    # Assicurarsi che la directory di output esista
    os.makedirs(args.output_directory, exist_ok=True)

    extract_column_names(args.input_file, args.output_name, args.output_directory)




if __name__ == "__main__":
    # example of server address = ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR977/ERR977413/ERR977413_1.fastq.gz
    server_address = 'ftp.sra.ebi.ac.uk'
    accession = 'MGYS00001392'
    erp_id = 'ERP011345'
    tsv_path = f'../Output/Unified_analyses/{accession}/{accession}_{erp_id}_taxonomy_abundances_v3.0.tsv'
    local_download_directory = f'../Output/Unified_analyses/{accession}/'

    # create a new folder for IDs
    path = os.path.join('../Output/', "IDs")
    if not os.path.exists(path):
        os.makedirs(path)

    # get a list of ERR ids for downloading fastq files
    extract_column_names(input_file= tsv_path, output_name = f'ERR_IDs_from_{accession}.txt', output_directory = path)

    # download FASTQ in local
    #download_files_from_list(server_address, f'../Output/IDs/ERR_IDs_from_{accession}.txt', '/vol1/fastq/', local_download_directory)

    # load personal credentials for Azure connection
    credentials = load_credentials('../credentials.json')

    # download fastq files and push them in the storage account
    download_files_push_store(server_address,
                              f'../Output/IDs/ERR_IDs_from_{accession}.txt',
                              '/vol1/fastq/',
                              local_download_directory,
                              azure_connection_string = f"DefaultEndpointsProtocol=https;AccountName={ credentials['storageAccountName']};AccountKey={credentials['storageAccountKey']};EndpointSuffix=core.windows.net",
                              azure_container_name = 'retrievefastq'
                              )
"""