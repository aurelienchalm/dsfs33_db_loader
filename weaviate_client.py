import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth



def connect_to_weaviate():


    load_dotenv()  # Charge les variables d'environnement à partir de .env

    weaviate_url = os.environ.get("WEAVIATE_URL")
    weaviate_api_key = os.environ.get("WEAVIATE_API_KEY")
    print("weaviate_url ",weaviate_url)
    print("weaviate_api_key ",weaviate_api_key)
    if not weaviate_url or not weaviate_api_key:
        raise ValueError("Variables d'environnement WEAVIATE_URL ou WEAVIATE_API_KEY manquantes.")

    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    )

    if not client.is_ready():
        raise ConnectionError("Impossible de se connecter à Weaviate.")
    return client
