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
- [Acknowledgments](#acknowledgement) - Credits and thanks to those who helped with the project

## About <a name = "about"></a>
The repository presents a comprehensive workflow for ...

## Getting started <a name = "getting-started"></a>
The following instructions are designed to guide users in extracting information and download FASTQ files considering a list of IDs. Originally, the pipeline was implemented using python scripts from retrieve info from MGnify repository (Sebastian). Presently, it is undergoing a transition to be re-implemented as a [Nextflow](https://nextflow.io) workflow. This update aims to enhance the reproducibility and efficiency of the analysis process.

## Prerequisites and installing <a name = "prerequisites-and-installing"></a>
This workflow is configured to be executed through Docker and Azure Batch, leveraging cloud computing resources and containerized environments.
No additional installation steps are required for the workflow itself, as it relies on cloud-based resources and Docker containers.
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
1. Functions_getInfo_MGnify_studies_analyses.py to retrieve a summary of MGnify studies and analyses for a given biome and data type (amplicon, shotgun metagenomics, metatranscriptomic, or assembly). 
2. Functions_get_results_from_MGnifystudy.py to obtain abundance and functional tables, as well as other results for a MGnify study.
3. Functions_get_samplesMetadata_from_MGnifystudy.py to obtain metadata for the samples of a MGnify study
4. get_fastq_from_list_ids.py to obtain FASTQ files from MGnify studies.  

## Repository structure <a name="repository-structure"></a>
The table below provides an overview of the key files and directories in this repository, along with a brief description of each.
|File  |Description            |
|:----:|-----------------------|
|[nextflow.config](nextflow.config)|Configuration file which contains a nextflow configuration for running the bioinformatics workflow, including parameters for processing genomic data on Azure cloud service|
|[nextflow_config_full_draft.txt](nextflow_config_full_draft.txt)|Text file which contains a configuration for nextflow workflow specifying resources requirements for each program used|

## References <a name = references"></a>
- [Docker](https://www.docker.com)
- [Azure](https://azure.microsoft.com/it-it)
- [Nextflow](https://www.nextflow.io)

## Authors <a name = "authors"></a>
- [marcor@dtu.dk](https://github.com/marcoreverenna)
- [sebastain@dtudk](https://github.com/salayaruano)

## Acknowledgements <a name = "acknowledgement"></a>
We would like to extend our heartfelt gratitude to [DTU Biosustain](https://www.biosustain.dtu.dk/) and the Novo Nordisk Foundation 
Center for Biosustainability for providing the essential resources and support that have been 
fundamental in the development and success of the [DSP (Data Science 
Platform)](https://www.biosustain.dtu.dk/informatics/data-science-platform) and [MoNA (Multi-omics Network 
Analysis)](https://www.biosustain.dtu.dk/research/research-groups/multi-omics-network-analytics-alberto-santos-delgado) projects.
