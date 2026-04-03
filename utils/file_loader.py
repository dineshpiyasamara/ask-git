import os
from langchain_community.document_loaders import TextLoader
from utils.config import EXCLUDED_DIRS, EXCLUDED_EXTENSIONS

def load_files(repo_path):
    documents = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        if any(ex_dir in root.split(os.sep) for ex_dir in EXCLUDED_DIRS):
            continue

        for file in files:
            _, ext = os.path.splitext(file.lower())
            if ext in EXCLUDED_EXTENSIONS:
                continue

            path = os.path.join(root, file)
            
            try:
                loader = TextLoader(path, encoding="utf-8")
                docs = loader.load()

                for d in docs:
                    d.metadata["source"] = os.path.relpath(path, repo_path)
                    d.metadata["full_path"] = path

                documents.extend(docs)
            except (UnicodeDecodeError, Exception) as e:
                pass
    return documents
