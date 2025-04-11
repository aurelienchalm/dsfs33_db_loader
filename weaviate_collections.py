import weaviate.classes as wvc


def suppr_collections(client):
    # Supprime uniquement la collection Article (plus besoin de Magazine)
    if client.collections.exists("Article"):
        client.collections.delete("Article")

def setup_collections(client):
    # Créer uniquement la collection Article, avec toutes les métadonnées intégrées
    if not client.collections.exists("Article"):
        print("Collection Article n'existe pas, création...")
        client.collections.create(
            name="Article",
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
            properties=[
                wvc.config.Property(name="text", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="chunk_index", data_type=wvc.config.DataType.INT),

                # Métadonnées héritées de "Magazine"
                wvc.config.Property(name="title", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="authors", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="creationDate", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="originalFile", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="pages", data_type=wvc.config.DataType.INT_ARRAY),
                wvc.config.Property(name="jsonFile", data_type=wvc.config.DataType.TEXT),
            ]
        )
