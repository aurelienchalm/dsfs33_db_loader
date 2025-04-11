# main.py
from data_loader import load_json_documents
from weaviate_client import connect_to_weaviate
from weaviate_collections import setup_collections, suppr_collections
from weaviate_inserter import insert_into_weaviate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
import warnings

warnings.simplefilter("ignore", ResourceWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

#log
logging.basicConfig(
    level=logging.INFO,  # Niveau minimal des messages à afficher
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format du log
    filename='logs/loader.log',  # (Optionnel) Fichier de sortie
    filemode='a'  # 'a' pour ajouter, 'w' pour écraser
)
logging.info("Début du chargement des documents dans la DB")

client = None

try:

    # Connexion 
    print("Connexion à Weaviate...")
    client = connect_to_weaviate()
    print("Weaviate prêt :", client.is_ready())

    # Nettoyage + création des collections
    print("(Re)création des collections...")
    #Pour le Test 
    suppr_collections(client)

    setup_collections(client)
    
    # Chargement des documents JSON
    print("Chargement des documents JSON...")
    all_docs = load_json_documents("docs")
    print(f"Documents chargés : {len(all_docs)}")

    # Split des documents
    # Split des documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Split avec conservation des métadonnées
    splitted_docs = []
    for doc in all_docs:
        splits = splitter.split_documents([doc])
        for chunk in splits:
            chunk.metadata = doc.metadata.copy()
        splitted_docs.extend(splits)

    print(f"Nombre de documents d'origine : {len(all_docs)}")
    print(f"Nombre de documents splittés : {len(splitted_docs)}")

    # Vérification (optionnelle)
    for i, chunk in enumerate(splitted_docs[:3]):
        print(f"Chunk {i+1} → file_name: {chunk.metadata.get('file_name')} | originalFile: {chunk.metadata.get('originalFile')}")
        #print(f"Nombre de documents d'origine:{len(all_docs)}\nNombre de documents splittés: {len(splitted_docs)}")

    # Insertion dans Weaviate
    print("Insertion dans Weaviate...")
    insert_into_weaviate(client, splitted_docs)
    
except Exception as e:
    print("Une erreur est survenue :", e)

finally:
    if client:
        client.close()
        print("Connexion à Weaviate fermée.")