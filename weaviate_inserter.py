from collections import defaultdict
import weaviate.classes.query as wvq

def clean_and_truncate(value, max_length=None):
    """
    Retourne None si la valeur est 'inconnu' ou vide, 
    sinon retourne la chaîne tronquée si nécessaire.
    """
    if not value or value.strip().lower() == "inconnu":
        return None
    value = value.strip()
    if max_length:
        return value[:max_length]
    return value

def insert_into_weaviate(client, splitted_docs):
    article_col = client.collections.get("Article")

    chunks_by_file = defaultdict(list)
    for chunk in splitted_docs:
        chunks_by_file[chunk.metadata["originalFile"]].append(chunk)

    total_chunks, skipped_files = 0, 0

    for original_file, chunks in chunks_by_file.items():
        meta = chunks[0].metadata

        # Vérifie si le fichier a déjà été inséré
        existing = article_col.query.fetch_objects(
            filters=wvq.Filter.by_property("jsonFile").equal(original_file)
        )
        """
        if len(existing.objects) > 0:
            print(f"Articles déjà présents pour : {original_file} — insertion ignorée.")
            skipped_files += 1
            continue
        """
        #Propriétés: [authors: authors, title: title, filename: filename, pages: pages, date : date]
        
        print(f"\nInsertion des chunks pour : {original_file} — {meta.get('title', 'Titre inconnu')}")
        for idx, chunk in enumerate(chunks):
            try:
                article_col.data.insert(
                    properties={
                        #"text": chunk.page_content,
                        "text": (
                            f"[authors: {chunk.metadata.get('authors', 'inconnu')}, "
                            f"title: {chunk.metadata.get('title', 'inconnu')}, "
                            f"filename: {chunk.metadata.get('originalFile', 'inconnu')}, "
                            f"pages: {chunk.metadata.get('pages', 'non spécifiées')}, "
                            f"date: {chunk.metadata.get('creationDate', 'inconnue')}]\n\n"
                            f"{chunk.page_content}"
                        ),
                        "chunk_index": idx,
                        "pages": chunk.metadata["pages"],
                        "authors": clean_and_truncate(chunk.metadata.get("authors")),
                        "title": clean_and_truncate(chunk.metadata.get("title"), max_length=100),
                        "creationDate": chunk.metadata.get("creationDate"),
                        "originalFile": chunk.metadata["originalFile"],
                        "jsonFile": chunk.metadata["jsonFile"]
                    }
                )
                total_chunks += 1
                #print(f"Chunk {idx} inséré (pages : {chunk.metadata['pages']})")

            except Exception as e:
                print(f"Échec insertion chunk {idx} ({chunk.metadata['jsonFile']}) : {e}")

        print(f"{len(chunks)} chunk(s) inséré(s) pour {original_file}")

    print("\nInsertion terminée :")
    print(f"   - {total_chunks} chunk(s) inséré(s)")
    print(f"   - {skipped_files} fichier(s) ignoré(s) (déjà existants dans Weaviate)")
