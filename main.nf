#!/usr/bin/env nextflow

params.tsv = "data/MGYS00001392_ERP011345_taxonomy_abundances_v3.0.tsv"
//params.url = "https://www.ebi.ac.uk/metagenomics/api/v1/analyses"
params.outputDir = 'output' // Directory di output

params.input_file = 'path/to/default/input_file.csv'
params.output_name = 'default_output_name'
params.output_directory = 'path/to/output_directory'

// sarebbe opportuno compiere l'intero processo con almeno due accessioni in modo tale da vedere la parallellizzazione

// val
// Utilizza val per passare valori non associati a un file system, come stringhe, numeri o qualsiasi altro valore che non rappresenta un percorso di file o directory. Questi valori sono trattati come dati letterali e possono essere utilizzati per parametri di configurazione, nomi di file dinamici, ecc.
// è utile quando hai bisogno di passare informazioni configurabili o parametri specifici che influenzano l'esecuzione del tuo processo ma che non si riferiscono direttamente a un file fisico. Per esempio, potresti voler passare il nome di un output file che sarà generato o una directory di output come stringhe

// path
// Utilizza path per passare riferimenti a file o directory. Questo consente a Nextflow di gestire i file come parte del suo sistema di gestione dati, ottimizzando il trasferimento di file, l'esecuzione in ambienti distribuiti e garantendo che i file siano disponibili dove e quando sono necessari per l'esecuzione di un processo.
// indica a Nextflow che l'oggetto in questione è un percorso di file o directory. Questo consente a Nextflow di gestire automaticamente la localizzazione dei file (ad esempio, scaricarli o copiarli in una cache locale) prima di eseguire un processo. Questo è particolarmente utile in ambienti distribuiti o quando si utilizzano sistemi di storage remoto.

process ExtractIDs {

    input:
    val(input_file) from params.input_file
    val(output_name) from params.output_name
    val(output_directory) from params.output_directory

    output:
    path "IDs.txt" into idsForDownload

    script:
    """
    pwd
    script.py --input_file ${params.tsv} --output_name ${output_name} --output_directory $output_directory
    """
}

// Processo per scaricare i file FASTQ
process DownloadFastq {
    input:
    val id from idsForDownload.flatten()

    output:
    path "${params.outputDir}/*"
    // Modificare in base alla struttura desiderata

    script:
    """
    python download_files_from_list.py
    """
}

workflow {
    ExtractIDs()
    DownloadFastq()
}