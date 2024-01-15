FROM python:3.8

# this path is different from your local path, should be correct this way
WORKDIR /usr/src/app

# copy the requirements.txt file into the container
COPY requirements.txt

# install the dependencies python 
RUN pip install --no-cache-dir -r requirements.txt

# Ambiente Completo: Copiando il codice nel container, ti assicuri che tutte le parti necessarie per eseguire il codice siano presenti.
# Questo è utile per la riproducibilità e per assicurarsi che non ci siano discrepanze tra ambienti di sviluppo e produzione.
COPY . .

# next step: nome-immagine e' il nome dell'immagine che voglio dare al container
# docker build -t nf-retrieve_info_mgnify .
# docker run --rm f-retrieve_info_mgnify

