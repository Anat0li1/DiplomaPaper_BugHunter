# from flask import Blueprint, render_template, request, jsonify, current_app
# from flask_jwt_extended import jwt_required
# from dotenv import load_dotenv
# import os
# import subprocess
# import tempfile

# load_dotenv()

# ai_bp = Blueprint('ai_assistant', __name__)


# @ai_bp.route('/ai-helper')
# def ui():
#     return render_template('ai_helper/index.html')


# @ai_bp.route('/api/ai/chat', methods=['POST'])
# @jwt_required()
# def api_chat():
#     data = request.get_json() or {}
#     message = data.get('message', '')
#     use_rag = data.get('use_rag', True)

#     # If Azure SDKs are available and configured, you can implement real RAG here.
#     # For now we provide a safe placeholder plus a helpful message.
#     AZ_OAI = os.getenv('AZURE_OPENAI_ENDPOINT')
#     AZ_OAI_KEY = os.getenv('AZURE_OPENAI_API_KEY')
#     AZ_SEARCH = os.getenv('AZURE_SEARCH_ENDPOINT')
#     if not (AZ_OAI and AZ_OAI_KEY):
#         response = f"AI placeholder: you said '{message}'.\n\nTo enable real AI, set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in .env and install azure-ai-openai. See docs/AI_ASSISTANT_SETUP.md"
#         return jsonify({'response': response}), 200

#     # Try to perform reply using Azure OpenAI and optional RAG (Qdrant or Azure Search)
#     try:
#         from azure.ai.openai import OpenAIClient
#         from azure.core.credentials import AzureKeyCredential
#         openai = OpenAIClient(AZ_OAI, AzureKeyCredential(AZ_OAI_KEY))

#         embedding_model = os.getenv('AZURE_OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')
#         chat_model = os.getenv('AZURE_OPENAI_CHAT_MODEL', 'gpt-35-turbo')

#         # If RAG enabled, retrieve top-k relevant chunks from the selected vector DB
#         context_chunks = []
#         if use_rag:
#             vector_db = os.getenv('VECTOR_DB', 'qdrant')
#             # create query embedding for the user message
#             emb_resp = openai.get_embeddings(model=embedding_model, input=[message])
#             query_emb = emb_resp.data[0].embedding

#             if vector_db == 'qdrant':
#                 try:
#                     from qdrant_client import QdrantClient
#                 except Exception:
#                     return jsonify({'response': 'qdrant-client not installed on server. Install qdrant-client.'}), 500

#                 qdrant_url = os.getenv('QDRANT_URL', 'http://localhost:6333')
#                 qdrant_api_key = os.getenv('QDRANT_API_KEY')
#                 collection_name = os.getenv('QDRANT_COLLECTION', 'rag-index')
#                 qclient = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
#                 # search
#                 try:
#                     hits = qclient.search(collection_name=collection_name, query_vector=query_emb, limit=5, with_payload=True)
#                 except Exception:
#                     current_app.logger.exception('Qdrant search failed')
#                     hits = []

#                 for h in hits:
#                     payload = getattr(h, 'payload', None) or {}
#                     content = None
#                     if isinstance(payload, dict):
#                         content = payload.get('content') or payload.get('text')
#                     else:
#                         content = payload
#                     if content:
#                         context_chunks.append(content)

#             elif vector_db == 'azure_search' or os.getenv('AZURE_SEARCH_ENDPOINT'):
#                 try:
#                     from azure.search.documents import SearchClient
#                     from azure.core.credentials import AzureKeyCredential as AzureCred
#                 except Exception:
#                     return jsonify({'response': 'azure-search-documents not installed on server. Install azure-search-documents.'}), 500

#                 search_endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
#                 search_key = os.getenv('AZURE_SEARCH_KEY')
#                 index_name = os.getenv('AZURE_SEARCH_INDEX')
#                 search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=AzureCred(search_key))

#                 # Azure Search vector query
#                 try:
#                     results = search_client.search(search_text="*", vector={"value": query_emb, "fields": "content_vector", "k": 5})
#                     for r in results:
#                         # `r` is a SearchResult with fields; prefer attribute access
#                         content = getattr(r, 'content', None) or (r.get('content') if isinstance(r, dict) else None)
#                         if content:
#                             context_chunks.append(content)
#                 except Exception:
#                     current_app.logger.exception('Azure Search vector search failed')

#         # assemble context (limit total chars)
#         max_context_chars = int(os.getenv('RAG_MAX_CONTEXT_CHARS', '2000'))
#         context = ''
#         for chunk in context_chunks:
#             if len(context) + len(chunk) > max_context_chars:
#                 break
#             context += '\n' + chunk

#         # Build chat messages
#         system_prompt = os.getenv('RAG_SYSTEM_PROMPT', 'You are a helpful assistant. Use the provided context to answer the user. If the answer is not in the context, reply concisely and honestly that you do not know.')
#         messages = [
#             {"role": "system", "content": system_prompt + ("\nContext:\n" + context if context else '')},
#             {"role": "user", "content": message}
#         ]

#         resp = openai.get_chat_completions(model=chat_model, messages=messages)
#         text = resp.choices[0].message.content if resp.choices else 'No response'
#         return jsonify({'response': text}), 200

#     except Exception as e:
#         current_app.logger.exception('OpenAI/RAG call failed')
#         return jsonify({'response': f'AI call failed: {e}'}), 500


# @ai_bp.route('/api/ai/upload-pdf', methods=['POST'])
# @jwt_required()
# def upload_pdf():
#     # Save uploaded PDF to data/pdfs and trigger indexer for that file
#     f = request.files.get('file')
#     if not f:
#         return jsonify({'error': 'no file uploaded'}), 400
#     save_dir = os.path.join(os.getcwd(), 'data', 'pdfs')
#     os.makedirs(save_dir, exist_ok=True)
#     filename = f.filename
#     save_path = os.path.join(save_dir, filename)
#     f.save(save_path)

#     # Trigger indexer for this file (synchronously). You can run async or background in production.
#     try:
#         script = os.path.join(os.getcwd(), 'scripts', 'ai_indexer.py')
#         # Use python to run indexer for folder containing this file
#         subprocess.run([os.getenv('PYTHON', 'python'), script, '--index-folder', save_dir], check=True)
#     except Exception as e:
#         current_app.logger.exception('Indexing failed')
#         return jsonify({'error': 'saved but indexing failed', 'details': str(e)}), 500

#     return jsonify({'status': 'ok', 'path': save_path}), 200


# @ai_bp.route('/api/ai/reindex', methods=['POST'])
# @jwt_required()
# def reindex():
#     # Trigger full reindex of data/pdfs
#     folder = os.path.join(os.getcwd(), 'data', 'pdfs')
#     if not os.path.exists(folder):
#         return jsonify({'error': 'pdf folder not found'}), 404
#     try:
#         script = os.path.join(os.getcwd(), 'scripts', 'ai_indexer.py')
#         subprocess.run([os.getenv('PYTHON', 'python'), script, '--pdf-folder', folder], check=True)
#         return jsonify({'status': 'ok', 'indexed_folder': folder}), 200
#     except Exception as e:
#         current_app.logger.exception('Reindex failed')
#         return jsonify({'error': str(e)}), 500

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv
import os

load_dotenv()

ai_bp = Blueprint("ai_assistant", __name__)


@ai_bp.route("/ai-helper")
def ui():
    return render_template("ai_helper/index.html")


@ai_bp.route("/api/ai/chat", methods=["POST"])
@jwt_required()
def api_chat():
    data = request.get_json() or {}
    message = data.get("message", "")
    use_rag = data.get("use_rag", True)

    # --------------------------------------------------
    # ENV
    # --------------------------------------------------
    AZ_OAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZ_OAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    EMB_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

    AZ_SEARCH_EP = os.getenv("AZURE_SEARCH_ENDPOINT")
    AZ_SEARCH_KEY = os.getenv("AZURE_SEARCH_API_KEY")
    INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX")

    if not all([AZ_OAI_ENDPOINT, AZ_OAI_KEY, EMB_DEPLOYMENT, CHAT_DEPLOYMENT]):
        return jsonify({
            "response": (
                f"AI not configured.\n\n"
                f"AZURE_OPENAI_ENDPOINT={'set' if AZ_OAI_ENDPOINT else 'missing'}\n"
                f"AZURE_OPENAI_API_KEY={'set' if AZ_OAI_KEY else 'missing'}\n"
                f"AZURE_OPENAI_EMBEDDING_DEPLOYMENT={EMB_DEPLOYMENT or 'missing'}\n"
                f"AZURE_OPENAI_CHAT_DEPLOYMENT={CHAT_DEPLOYMENT or 'missing'}"
            )
        }), 200

    try:
        # --------------------------------------------------
        # Azure OpenAI client (CORRECT)
        # --------------------------------------------------
        from openai import AzureOpenAI

        aoai = AzureOpenAI(
            api_key=AZ_OAI_KEY,
            azure_endpoint=AZ_OAI_ENDPOINT,
            api_version="2024-02-15-preview"
        )

        context_chunks = []
        sources = []

        # --------------------------------------------------
        # RAG: Azure Search
        # --------------------------------------------------
        if use_rag and AZ_SEARCH_EP and AZ_SEARCH_KEY and INDEX_NAME:
            from azure.search.documents import SearchClient
            from azure.core.credentials import AzureKeyCredential

            search_client = SearchClient(
                endpoint=AZ_SEARCH_EP,
                index_name=INDEX_NAME,
                credential=AzureKeyCredential(AZ_SEARCH_KEY),
            )

            # Query embedding
            emb = aoai.embeddings.create(
                model=EMB_DEPLOYMENT,   # DEPLOYMENT NAME
                input=message
            ).data[0].embedding

            k = int(os.getenv("RAG_TOP_K", 5))

            try:
                results = search_client.search(
                    search_text="*",
                    vector={
                        "value": emb,
                        "fields": "content_vector",
                        "k": k
                    }
                )

                for r in results:
                    content = getattr(r, "content", None)
                    if content:
                        context_chunks.append(content)

                    file_name = getattr(r, "file_name", None)
                    if file_name:
                        sources.append(file_name)

            except Exception:
                current_app.logger.exception("Azure Search vector query failed")

        # --------------------------------------------------
        # Assemble context
        # --------------------------------------------------
        max_chars = int(os.getenv("RAG_MAX_CONTEXT_CHARS", 2000))
        context_text = ""
        for c in context_chunks:
            if len(context_text) + len(c) > max_chars:
                break
            context_text += "\n" + c

        system_prompt = os.getenv(
            "RAG_SYSTEM_PROMPT",
            "You are a helpful assistant. Use the provided context to answer the user. "
            "If the answer is not in the context, say you do not know."
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt + ("\nContext:\n" + context_text if context_text else "")
            },
            {"role": "user", "content": message}
        ]

        # --------------------------------------------------
        # Chat completion
        # --------------------------------------------------
        resp = aoai.chat.completions.create(
            model=CHAT_DEPLOYMENT,   # DEPLOYMENT NAME
            messages=messages,
            temperature=0.2,
        )

        answer = resp.choices[0].message.content

        return jsonify({
            "response": answer,
            "sources": list(set(sources))
        }), 200

    except Exception as e:
        current_app.logger.exception("OpenAI/RAG call failed")
        return jsonify({"response": f"AI call failed: {e}"}), 500
