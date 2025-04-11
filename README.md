# Projet final de la fullstack, db loader

## Si besoin suppression d'un environnement : 

conda deactivate

conda remove --name my_projet --all

## Création de l'environnement : 

conda create -n projet_dsfs33_env python=3.11

conda activate projet_dsfs33_env

conda install pip

conda activate projet_dsfs33_env

conda env list

## requirement.txt

pip install -r requirements.txt

Fichier .env contenant les variables : 

WEAVIATE_URL=https://mon-cluster.weaviate.network
WEAVIATE_API_KEY=ma-cle-api-secrete

## Execution pour le loader

python main_loader.py

## Modules

data_loader.py → charge les fichiers JSON
weaviate_client.py → connecte au cluster Weaviate
weaviate_collections.py → crée les collections
weaviate_inserter.py → insère les données dans Weaviate
