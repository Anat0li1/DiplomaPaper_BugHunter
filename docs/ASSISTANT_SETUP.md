# Налаштування асистента та RAG в Azure

Цей документ описує базове підключення асистента до Azure OpenAI та Azure AI Search.

## Що потрібно

- Azure-акаунт із правами на створення ресурсів.
- Ресурс Azure OpenAI із deployment для embeddings і chat completion.
- Ресурс Azure AI Search та індекс для фрагментів документів.
- Заповнені змінні середовища в `.env`.

## Змінні середовища

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=
AZURE_OPENAI_CHAT_DEPLOYMENT=
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_API_KEY=
AZURE_SEARCH_INDEX=bughunter-index
RAG_MAX_CONTEXT_CHARS=2000
RAG_TOP_K=5
```

## Індексація PDF

Покладіть PDF-файли у локальну папку `data/pdfs` і запустіть:

```bash
python scripts/ai_indexer.py --index-folder data/pdfs
```

PDF-файли не варто комітити в репозиторій, якщо вони містять приватні або навчальні матеріали.

## Перевірка чату

Після запуску застосунку відкрийте сторінку `/ai-helper`. Якщо змінні середовища не задані, інтерфейс поверне дружнє повідомлення про відсутню конфігурацію.
