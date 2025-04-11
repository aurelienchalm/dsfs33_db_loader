import json
from pathlib import Path
from langchain_core.documents import Document

def load_json_documents(path: str) -> list[Document]:
    docs_path = Path(path)
    json_files = list(docs_path.glob("*.json"))
    print(f"\n{len(json_files)} fichiers JSON trouvés dans {path}.\n")

    all_docs = []

    for i, file_path in enumerate(json_files, 1):
        print(f"📄 [{i}/{len(json_files)}] Traitement de : {file_path.name}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                content = data.get("text", "").strip()
                if not content:
                    print("Document vide ignoré.\n")
                    continue

                raw_meta = data.get("metadata", {})
                pages = [int(p) for p in raw_meta.get("pages", [])]

                metadata = {
                    "title": raw_meta.get("title", "").strip(),
                    "authors": raw_meta.get("authors", "").strip(),
                    "creationDate": raw_meta.get("creationDate", ""),
                    "originalFile": raw_meta.get("originalFile", "").strip(),
                    "pages": pages,
                    "jsonFile": file_path.name
                }

                doc = Document(page_content=content, metadata=metadata)
                all_docs.append(doc)

                print(f"Ajouté : {metadata['title']} (pages : {pages})\n")

        except Exception as e:
            print(f"Erreur lors du traitement de {file_path.name} : {e}\n")

    print(f"\n{len(all_docs)} document(s) chargé(s) sur {len(json_files)} fichier(s) JSON.\n")
    return all_docs
