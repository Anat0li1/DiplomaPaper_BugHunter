# """Simple PDF indexer for Azure Cognitive Search + Azure OpenAI embeddings.

# Usage examples (PowerShell):

# Activate venv first:
# .\venv\Scripts\Activate.ps1

# # Create index (best-effort)
# python scripts\ai_indexer.py --create-index

# # Index all PDFs in data/pdfs
# python scripts\ai_indexer.py --index-folder data\pdfs

# This script is intentionally simple and prints helpful messages.
# It expects these env vars in a .env file or environment:
# - AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT
# - AZURE_SEARCH_KEY, AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_INDEX

# If you get SDK import errors, install the required packages listed in docs/AI_ASSISTANT_SETUP.md.
# """
# import os
# import argparse
# from dotenv import load_dotenv
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# try:
#     from PyPDF2 import PdfReader
# except Exception:
#     PdfReader = None

# try:
#     # Azure Cognitive Search client and credential
#     from azure.search.documents import SearchClient
#     from azure.core.credentials import AzureKeyCredential
# except Exception:
#     SearchClient = None
#     AzureKeyCredential = None

# try:
#     # Azure OpenAI client (optional)
#     from azure.ai.openai import OpenAIClient
# except Exception:
#     OpenAIClient = None
# try:
#     # Qdrant client (optional alternative to Azure Cognitive Search)
#     from qdrant_client import QdrantClient
#     from qdrant_client.http import models as qdrant_models
# except Exception:
#     QdrantClient = None
#     qdrant_models = None

# import math

# CHUNK_SIZE = 800  # characters

# def extract_text_from_pdf(path: str) -> str:
#     if PdfReader is None:
#         raise RuntimeError("PyPDF2 not installed. Run pip install PyPDF2")
#     text = []
#     reader = PdfReader(path)
#     for page in reader.pages:
#         try:
#             page_text = page.extract_text() or ""
#         except Exception:
#             page_text = ""
#         text.append(page_text)
#     return "\n".join(text)

# def chunk_text(text: str, size: int = CHUNK_SIZE):
#     if not text:
#         return []
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = min(start + size, len(text))
#         chunks.append(text[start:end])
#         start = end
#     return chunks

# def _use_azure_openai():
#     return OpenAIClient is not None and os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_KEY")


# def embed_text(texts: list[str]):
#     """Return list of embeddings for the input texts.

#     This tries to use the azure-ai-openai SDK first. If it's not available,
#     it falls back to the `openai` package (if installed) configured for Azure.
#     """
#     model = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

#     # Try azure.ai.openai first (prefer deployment name for Azure)
#     if _use_azure_openai():
#         try:
#             azure_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") or os.getenv("AZURE_OPENAI_EMBEDDING_MODEL") or model
#             if not os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"):
#                 print("Warning: AZURE_OPENAI_EMBEDDING_DEPLOYMENT not set — Azure OpenAI usually requires a deployment name (not the base model). Create a deployment in the Azure Portal and set AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<deployment-name> in your .env.")
#             client = OpenAIClient(os.getenv("AZURE_OPENAI_ENDPOINT"), AzureKeyCredential(os.getenv("AZURE_OPENAI_KEY")))
#             # Some Azure SDK versions expect 'deployment' or 'engine' instead of 'model'
#             try:
#                 resp = client.get_embeddings(deployment=azure_deployment, input=texts)
#             except TypeError:
#                 resp = client.get_embeddings(model=azure_deployment, input=texts)
#             return [r.embedding for r in resp.data]
#         except Exception as e:
#             print("Azure OpenAI embedding error:", repr(e))

#     # Fallback to openai package
#     try:
#         # Map Azure env vars to new OpenAI client env var names if needed
#         if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_KEY"):
#             os.environ.setdefault("OPENAI_API_TYPE", os.getenv("OPENAI_API_TYPE", "azure"))
#             # Try azure.ai.openai first (require deployment name for Azure)
#             if _use_azure_openai():
#                 azure_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
#                 if not azure_deployment:
#                     raise RuntimeError("AZURE_OPENAI_EMBEDDING_DEPLOYMENT is required when using Azure OpenAI. Create a deployment in the Azure Portal and set AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<deployment-name> in your .env")
#                 try:
#                     client = OpenAIClient(os.getenv("AZURE_OPENAI_ENDPOINT"), AzureKeyCredential(os.getenv("AZURE_OPENAI_KEY")))
#                     # Some Azure SDK versions expect 'deployment' or 'model' parameter
#                     try:
#                         resp = client.get_embeddings(deployment=azure_deployment, input=texts)
#                     except TypeError:
#                         resp = client.get_embeddings(model=azure_deployment, input=texts)
#                     return [r.embedding for r in resp.data]
#                 except Exception as e:
#                     print("Azure OpenAI embedding error:", repr(e))
#             import traceback
#             print("OpenAI new-client embeddings error:\n", traceback.format_exc())

#             # Fallback to legacy openai package interface (pre-1.0)
#             try:
#                 import openai as openai_legacy
#                 # Configure legacy client for Azure if needed
#                 if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_KEY"):
#                     openai_legacy.api_type = os.getenv("OPENAI_API_TYPE", "azure")
#                     openai_legacy.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
#                 azure_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

#                 # Legacy client: Azure expects 'engine' (deployment) parameter
#                 try:
#                     resp = openai_legacy.Embedding.create(engine=azure_deployment, input=texts)
#                     return [d['embedding'] for d in resp['data']]
#                 except Exception:
#                     # Try with model name as a fallback
#                     resp = openai_legacy.Embedding.create(model=model, input=texts)
#                     return [d['embedding'] for d in resp['data']]
#             except Exception as e_legacy:
#                 import traceback
#                 print("Legacy openai client error:\n", traceback.format_exc())
#                 raise RuntimeError(f"No working OpenAI client available for embeddings: new_client_error={repr(e_new)}, legacy_error={repr(e_legacy)}")
#     except Exception as e:
#         raise RuntimeError("No working OpenAI client available for embeddings: " + str(e))

# def get_search_client():
#     if SearchClient is None:
#         raise RuntimeError("azure-search-documents is not installed. Install via pip.")
#     endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
#     key = os.getenv("AZURE_SEARCH_KEY")
#     index = os.getenv("AZURE_SEARCH_INDEX")
#     if not (endpoint and key and index):
#         raise RuntimeError("Set AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, and AZURE_SEARCH_INDEX in .env")
#     return SearchClient(endpoint=endpoint, index_name=index, credential=AzureKeyCredential(key))


# def index_folder(folder: str):
#     print(f"Indexing PDFs from: {folder}")
#     files = []
#     for root, _, filenames in os.walk(folder):
#         for fn in filenames:
#             if fn.lower().endswith('.pdf'):
#                 files.append(os.path.join(root, fn))

#     if not files:
#         print("No PDF files found.")
#         return

#     vector_db = os.getenv('VECTOR_DB', os.getenv('AZURE_SEARCH_INDEX') and 'azure_search' or 'qdrant')
#     qdrant_client = None
#     search_client = None

#     if vector_db == 'azure_search':
#         search_client = get_search_client()
#     elif vector_db == 'qdrant':
#         if QdrantClient is None:
#             raise RuntimeError('qdrant-client not installed. Install via pip install qdrant-client')
#         # QDRANT_HOST can be e.g. http://localhost:6333 or QDRANT cloud URL
#         qdrant_url = os.getenv('QDRANT_URL', 'http://localhost:6333')
#         qdrant_api_key = os.getenv('QDRANT_API_KEY')
#         qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
#         collection_name = os.getenv('QDRANT_COLLECTION', os.getenv('AZURE_SEARCH_INDEX', 'rag-index'))
#         # Ensure collection exists with proper vector size later after we know embedding size
#     else:
#         raise RuntimeError(f'Unsupported VECTOR_DB setting: {vector_db}')

#     for path in files:
#         print("Processing:", path)
#         try:
#             text = extract_text_from_pdf(path)
#             chunks = chunk_text(text)
#             print(f" - extracted {len(chunks)} chunks")
#             # get embeddings in batches
#             embeddings = []
#             batch_size = 16
#             for i in range(0, len(chunks), batch_size):
#                 batch = chunks[i:i+batch_size]
#                 emb = embed_text(batch)
#                 embeddings.extend(emb)

#             # prepare documents for Azure Search
#             docs = []
#             for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
#                 doc = {
#                     "id": f"{os.path.basename(path)}::{idx}",
#                     "source_file": os.path.basename(path),
#                     "content": chunk,
#                     # The name of the vector field must match the index mapping in Azure Search.
#                     # Many setups use 'content_vector' as the vector field name.
#                     "content_vector": emb
#                 }
#                 docs.append(doc)

#             if vector_db == 'azure_search':
#                 print(f" - uploading {len(docs)} docs to Azure Cognitive Search index")
#                 result = search_client.upload_documents(documents=docs)
#                 print(" - upload result sample:", result[0] if result else "(no result)")
#             elif vector_db == 'qdrant':
#                 print(f" - uploading {len(docs)} docs to Qdrant collection '{collection_name}'")
#                 # Create collection if not exists. Determine vector size from embedding length
#                 if len(docs) > 0:
#                     vector_size = len(docs[0]['content_vector'])
#                     if collection_name not in [c.name for c in qdrant_client.get_collections().collections]:
#                         qdrant_client.recreate_collection(
#                             collection_name=collection_name,
#                             vectors_config=qdrant_models.VectorParams(size=vector_size, distance=qdrant_models.Distance.COSINE)
#                         )

#                 # Prepare points for upsert
#                 points = []
#                 for d in docs:
#                     pt = qdrant_models.PointStruct(
#                         id=d['id'],
#                         vector=d['content_vector'],
#                         payload={
#                             'source_file': d.get('source_file'),
#                             'content': d.get('content')
#                         }
#                     )
#                     points.append(pt)

#                 # Upsert in batches
#                 batch_size = 64
#                 for i in range(0, len(points), batch_size):
#                     batch = points[i:i+batch_size]
#                     qdrant_client.upsert(collection_name=collection_name, points=batch)
#                 print(' - qdrant upload finished')
#         except Exception as e:
#             print("Failed to index", path, e)


import argparse
import os
import sys
import uuid
from typing import List

from dotenv import load_dotenv
from PyPDF2 import PdfReader

from openai import AzureOpenAI

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SearchField,
)

# ============================================================
# ENV
# ============================================================
def load_and_validate_env():
    load_dotenv()

    required = [
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_API_KEY",
        "AZURE_SEARCH_INDEX_NAME",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
    ]

    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    return (
        os.getenv("AZURE_SEARCH_ENDPOINT"),
        os.getenv("AZURE_SEARCH_API_KEY"),
        os.getenv("AZURE_SEARCH_INDEX_NAME"),
        os.getenv("AZURE_OPENAI_ENDPOINT"),
        os.getenv("AZURE_OPENAI_API_KEY"),
        os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    )


# ============================================================
# PDF
# ============================================================
def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


# ============================================================
# CHUNKING
# ============================================================
def chunk_text(text: str, size=800, overlap=100) -> List[str]:
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


# ============================================================
# SEARCH INDEX
# ============================================================
def create_index_if_not_exists(endpoint, key, index_name):
    index_client = SearchIndexClient(endpoint, AzureKeyCredential(key))

    if index_name in [i.name for i in index_client.list_indexes()]:
        print(f"[INFO] Index '{index_name}' already exists")
        return

    print(f"[INFO] Creating index '{index_name}'")

    index = SearchIndex(
        name=index_name,
        fields=[
            SimpleField(name="id", type="Edm.String", key=True),
            SearchableField(name="content", type="Edm.String"),
            SearchField(
                name="content_vector",
                type="Collection(Edm.Single)",
                searchable=True,
                vector_search_dimensions=1536,
                vector_search_profile_name="vector-profile",
            ),
            SimpleField(name="file_name", type="Edm.String", filterable=True),
        ],
        vector_search=VectorSearch(
            profiles=[
                VectorSearchProfile(
                    name="vector-profile",
                    algorithm_configuration_name="hnsw",
                )
            ],
            algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
        ),
    )

    index_client.create_index(index)


# ============================================================
# INDEXING
# ============================================================
def index_pdfs(
    folder,
    search_ep,
    search_key,
    index_name,
    aoai_ep,
    aoai_key,
    emb_dep,
):
    search_client = SearchClient(
        endpoint=search_ep,
        index_name=index_name,
        credential=AzureKeyCredential(search_key),
    )

    aoai = AzureOpenAI(
        api_key=aoai_key,
        azure_endpoint=aoai_ep,
        api_version="2024-12-01-preview",
    )

    documents = []

    for root, _, files in os.walk(folder):
        for file in files:
            if not file.lower().endswith(".pdf"):
                continue

            path = os.path.join(root, file)
            print(f"[INFO] Processing {path}")

            text = extract_text_from_pdf(path)
            if not text.strip():
                continue

            for chunk in chunk_text(text):
                emb = aoai.embeddings.create(
                    model=emb_dep,
                    input=chunk,
                ).data[0].embedding

                documents.append(
                    {
                        "id": str(uuid.uuid4()),
                        "file_name": file,
                        "content": chunk,
                        "content_vector": emb,
                    }
                )

    if not documents:
        print("[INFO] No content to index")
        return

    for i in range(0, len(documents), 100):
        batch = documents[i : i + 100]
        search_client.upload_documents(batch)
        print(f"[INFO] Uploaded batch {i // 100 + 1}")


# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Index local PDF files into Azure AI Search with Azure OpenAI embeddings"
    )
    parser.add_argument("--pdf-folder", required=True)
    args = parser.parse_args()

    folder = os.path.abspath(args.pdf_folder)
    if not os.path.isdir(folder):
        raise RuntimeError(f"Folder not found: {folder}")

    (
        search_ep,
        search_key,
        index_name,
        aoai_ep,
        aoai_key,
        emb_dep,
    ) = load_and_validate_env()

    create_index_if_not_exists(search_ep, search_key, index_name)

    index_pdfs(
        folder,
        search_ep,
        search_key,
        index_name,
        aoai_ep,
        aoai_key,
        emb_dep,
    )

    print("[DONE] Indexing complete")


if __name__ == "__main__":
    main()

