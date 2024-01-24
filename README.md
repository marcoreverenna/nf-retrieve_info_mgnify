# Nextflow retrieve info MGnify
<p align="left">
Metagenomics pipeline to retrieve info from MGnify using IDs.
</p>

---

## Table of contents

- [About](#about) - Overview of the project's purpose and goals
- [Getting Started](#getting-started) - Instructions on how to begin with this project
- [Prerequisites and installing](#prerequisites-and-installing) - Required software and installation steps 
- [Step by step](#step-by-step) - Detailed guide to each stage of the project
- [Repository structure](#repository-structure) - A layout of the repository's architecture, describing the purpose of each file or directory
- [References](#references) - Tools used in the project
- [Authors](#authors) - List of contributors to the project
- [Acknowledgments](#acknowledgments) - Credits and thanks to those who helped with the project

## About <a name = "about"></a>
This repository is designed to efficiently fetch and analyze data from MGnify studies, focusing on specific biomes and study types.
It extends the work initiated by [sayalaruano](https://github.com/sayalaruano) utilizing the MGnify API for effective data retrieval.
The project leverages Nextflow, an advanced and flexible platform for constructing computational pipelines. Moreover, the workflow is thoughtfully crafted to 
be compatible with another pipeline developed by [apalleja](https://github.com/apalleja), highlighting its adaptability and relevance in a variety of research scenarios.

## Getting started <a name = "getting-started"></a>
The following instructions are designed to guide users in extracting information and download FASTQ files considering a list of IDs. Originally, the pipeline was implemented using python scripts from retrieve info from MGnify repository (Sebastian). Presently, it is undergoing a transition to be re-implemented as a [Nextflow](https://nextflow.io) workflow. This update aims to enhance the reproducibility and efficiency of the analysis process.

## Prerequisites and installing <a name = "prerequisites-and-installing"></a>

### Azure setting
This workflow is configured to be executed through Azure Batch and Docker, leveraging cloud computing resources and containerized environments.
It is recommended to follow these [instructions](https://seqera.io/blog/nextflow-and-azure-batch-part-1-of-2/#about-azure-batch) to set Azure up.
Remember also to change the name of the container which is not specified in this guide. This guide download Java and Nextflow so it is not necessary to follow the following instructions.
Going through steps:
1. Generating a batch account
2. Generating a storage account
3. Generating a container (the concept of container in Azure is different from Docker)
4. [Generating a Virtual Machine](https://portal.azure.com/#create/Microsoft.VirtualMachine-ARM)

### Connecting with GitHub
Using the SSH protocol, you can connect and authenticate to remote servers. For more details please have a look at this [page](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh).
Going through steps:
1. [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
2. [Checking for existing SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys)
3. [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
4. [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)

If you get this message [error-permission-denied-publickey](https://docs.github.com/en/authentication/troubleshooting-ssh/error-permission-denied-publickey):
1. Copy and paste your private key in VM
2. Modifing the permissions: `chmod 600 ~/.ssh/id_rsa`
3. Adding your private key and entering your passphrase: `ssh-add ~/path/id_rsa`

Once you have completed all these steps you can try to clone a repository from GitHub.

### Upload samples into the VM

**Uploading samples into the VM**
1. Using SCP command
2. Using `azcopy` command: follow this [guide](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10); this should be the command: `azureuser@marcorVM:~/test-meta$ azcopy copy 'https://[profile].blob.core.windows.net/metanfnewsample/ERR9777403?sp=rwd&st=2024-01-23T12:54:38Z&se=2024-01-23T20:54:38Z&sv=2022-11-02&sr=b&sig=yebbX8kGGVBwSJCSMuGmVtF1IYFs8TzTkeRMVbYzO4A%3D´ "path/"` 
3. Using Azure Blob Storage

---

Make sure Docker is installed and properly set up, configure your Azure Blob Storage and Azure Batch accounts, and install Nextflow following [Nextflow information guide](https://www.nextflow.io/docs/latest/getstarted.html) if you haven't done it yet.
Once these prerequisites are in place, you can clone the repository and run the analysis.

The following instructions consider macOS systems.
### Installing Java
1. [Download Java](https://www.java.com/en/download/) if it is not already installed in your laptop.
2. Double click on downloaded `.dmg` file
3. If the java version in not included between 11 and 21 Nextflow could not work so [download updated version of Java](https://download.oracle.com/java/21/latest/jdk-21_macos-x64_bin.dmg)
4. Check your Java version with this command `java -version` in your terminal
### Installing Docker
1. [Download Docker](https://www.docker.com/products/docker-desktop/) if it is not already installed in your laptop.
2. Double click on downloaded `.dmg` file
3. Check your Docker version with this command `docker --version` in your terminal
### Installing Nextflow
1. Install Nextflow using this simple command in your terminal `curl -s https://get.nextflow.io | bash`
2. Move Nextflow in a specific directory `sudo mv nextflow /usr/local/bin`
3. Check your Nextflow version with this command `nextflow -version` in your terminal

## Step by step <a name = "step-by-step"></a>
This pipeline considers functions from the repository called **Retrieve_info_MGnifyAPI**. Functions has been modified to make them more simple and readable for a workflow. A file named `mgnify_functions.py` contains all the remade functions able to get info from MGnify and also download FASTQ files:
1. `Functions_getInfo_MGnify_studies_analyses.py` to retrieve a summary of MGnify studies and analyses for a given biome and data type (amplicon, shotgun metagenomics, metatranscriptomic, or assembly). 
2. `Functions_get_results_from_MGnifystudy.py` to obtain abundance and functional tables, as well as other results for a MGnify study.
3. `Functions_get_samplesMetadata_from_MGnifystudy.py` to obtain metadata for the samples of a MGnify study
4. `get_fastq_from_list_ids.py` to obtain FASTQ files from MGnify studies.  

To run this Nextflow script, use the command `nextflow run main.nf --url_studies "https://www.ebi.ac.uk/metagenomics/api/v1/studies" --url_analyses "https://www.ebi.ac.uk/metagenomics/api/v1/analyses" --biome_name "example_biome" --experiment_type "example_experiment"`.


## Repository structure <a name="repository-structure"></a>
The table below provides an overview of the key files and directories in this repository, along with a brief description of each.
|File  |Description            |
|:----:|-----------------------|
|[nextflow.config](nextflow.config)|Configuration file which contains a nextflow configuration for running the bioinformatics workflow, including parameters for processing genomic data on Azure cloud service|
|[nextflow_config_full_draft.txt](nextflow_config_full_draft.txt)|Text file which contains a configuration for nextflow workflow specifying resources requirements for each program used|
|[Dockerfile](Dockerfile)|Docker file containing the necessary commands to assemble a docker image|
|[requirements.txt](requirements.txt)|Text file containing all the dependencies to run the analysis|
|[mgnify_functions.py](mgnify_functions.py)|Python script which contains all the fuctions to retrieve info from MGnify and get FASTQ file to run the second pipeline|

## References <a name = "references"></a>
- [Docker](https://www.docker.com)
- [Azure](https://azure.microsoft.com)
- [Nextflow](https://www.nextflow.io)

## Authors <a name = "authors"></a>
- [marcor@dtu.dk](https://github.com/marcoreverenna)
- [sebastain@dtudk](https://github.com/salayaruano)

## Acknowledgments <a name = "acknowledgments"></a>
We would like to extend our heartfelt gratitude to [DTU Biosustain](https://www.biosustain.dtu.dk/) and the Novo Nordisk Foundation 
Center for Biosustainability for providing the essential resources and support that have been 
fundamental in the development and success of the [DSP (Data Science 
Platform)](https://www.biosustain.dtu.dk/informatics/data-science-platform) and [MoNA (Multi-omics Network 
Analysis)](https://www.biosustain.dtu.dk/research/research-groups/multi-omics-network-analytics-alberto-santos-delgado) projects.
