# AI Assistant & RAG Setup (Azure) — Step-by-step (very simple)

This guide explains how to set up the AI Assistant in this project using Microsoft Azure services. It's written in a very simple, step-by-step style so you can follow it slowly. It also includes how to host the app on Azure and how to automatically re-index new PDF files after merging changes.

If anything is unclear, follow each step slowly and copy/paste commands exactly.

---

## Overview (one-sentence)
We will use Azure OpenAI to get embeddings and answers, Azure Cognitive Search (vector search) to store and retrieve document chunks (RAG), and a small indexer script to extract text from PDFs and push them into the search index.

---

## What you need before we start

- An Azure account. Make one at https://portal.azure.com if you do not have it.
- Permission to create resources (Cognitive Search and Azure OpenAI or OpenAI-like resource)
- The project code (this repo) on your machine.
- Python 3.10+ and a virtual environment.

---

## 1) Prepare your local project

1. Open PowerShell.
2. Go to the project folder. Example:

```powershell
cd "c:\Users\Admin\Desktop\MyDocs\University\Fourth course\Diploma preps\cursor-try-2"
```

3. Create and activate a virtual environment (Windows):

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1
```

4. Install requirements (we added azure packages, PyPDF2). Run:

```powershell
pip install -r requirements.txt
```

If you see an error about packages, install them manually:

```powershell
pip install azure-ai-openai azure-search-documents PyPDF2 python-dotenv
```

5. Create a `.env` file in the project root (copy `.env.example` if present) and add these values (you'll get them from Azure in the steps below):

```
AZURE_OPENAI_KEY=your_openai_key_here
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com

AZURE_SEARCH_KEY=your_search_admin_key_here
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_INDEX=rag-index

FLASK_SECRET_KEY=change-me
JWT_SECRET_KEY=change-me
```

Keep `.env` secret and do not commit it.

---

## Full setup: from zero to running the AI assistant with RAG (local PDFs)

Follow these exact steps to run everything locally, index PDF files from a folder, and use the AI chat UI with RAG.

1) Clone repo and create venv

```powershell
cd "c:\Users\Admin\Desktop\MyDocs\University\Fourth course\Diploma preps"
git clone <your-repo-url> cursor-try-2
cd cursor-try-2
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Prepare `.env` (copy `.env.example` to `.env` and edit)

Add these minimal values for local RAG (Qdrant + Azure OpenAI embeddings):

```
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com
AZURE_OPENAI_KEY=your_openai_key
VECTOR_DB=qdrant
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=rag-index
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bughunter
JWT_SECRET_KEY=change-me
SECRET_KEY=change-me
```

4) Start Qdrant locally (Docker)

If you don't have Docker, install Docker Desktop first. Then run:

```powershell
docker run -p 6333:6333 -v qdrant_storage:/qdrant/storage -d qdrant/qdrant
```

5) Create `data/pdfs/` and put PDF files there

```powershell
mkdir data\pdfs
# copy some .pdf files into data\pdfs
```

6) Create or start a PostgreSQL database for the app

For local dev you can run Postgres in Docker or use an existing DB. Example (Docker):

```powershell
docker run --name bughunter-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=bughunter -p 5432:5432 -d postgres:14
```

Update `DATABASE_URL` in `.env` accordingly if you changed credentials.

7) Initialize the database and create tables

Start the Flask app once to create tables (app.py has db.create_all in main):

```powershell
set FLASK_APP=app.py; flask run
```

You should see the app starting. Stop it after it finishes creating tables (Ctrl+C).

8) Create a test user (easy ways)

- Via web UI: open http://127.0.0.1:5000/login.html → Register tab → create a user.
- Or use the helper script (recommended for automation):

```powershell
python scripts\create_user.py tester tester@example.com P@ssw0rd1
```

9) Index your PDFs (create embeddings and push to Qdrant)

```powershell
python scripts\ai_indexer.py --index-folder data\pdfs
```

Watch the output for progress. The script will create a collection in Qdrant named by `QDRANT_COLLECTION` and upload vectors.

10) Run the app and use the AI Helper UI

Start the Flask app:

```powershell
set FLASK_APP=app.py; flask run
```

Open http://127.0.0.1:5000/login.html, login with your test user, then open http://127.0.0.1:5000/ai-helper (or the AI Helper menu) and ask questions. The chat will query Qdrant, fetch context, and use Azure OpenAI to answer.

11) Re-index after adding new PDFs

Either run the indexer again locally:

```powershell
python scripts\ai_indexer.py --index-folder data\pdfs
```

Or use the app endpoint (requires login and token): POST `/ai/api/ai/reindex` (no body) to trigger the reindex step via the server.

---

If anything fails, copy the error message and paste it here and I will help debug. This end-to-end flow was tested conceptually against the code in the repo; actual Azure OpenAI keys and a running Qdrant instance are required for RAG to work.

---

## 2) Create Azure resources

I will assume you use the Azure Portal. Follow slowly.

1. Sign in to https://portal.azure.com.
2. Create an Azure OpenAI resource (if available in your subscription) or use OpenAI-compatible resource. Note its endpoint and key.
3. Create an Azure Cognitive Search resource. Note the admin key and the endpoint.

Important: For RAG with vector search you need the Search service to support vector fields. In many regions this is supported by default. If unsure, follow Azure doc for Vector Search.

---

## 3) Create the Cognitive Search index (simple)

We need an index that stores document text and a vector field. The `scripts/ai_indexer.py` includes helper to create the index. You can also use the REST API or Azure SDK.

Steps:

1. Open PowerShell and run:

```powershell
# activate venv first
.\venv\Scripts\Activate.ps1
python scripts\ai_indexer.py --create-index
```

This will try to create the index `rag-index` (or the one from `AZURE_SEARCH_INDEX`) using the admin key in `.env`.

If it fails, read the error and follow the message in the script — common reason: index already exists or your service doesn't support vectors.

---

Alternative (no Azure Cognitive Search): Qdrant or Chroma

If you cannot or prefer not to use Azure Cognitive Search, you can use another vector store. Two simple options:

- Qdrant (open-source vector DB) — you can run locally with Docker or use a managed cloud service.
- Chroma (local vector DB) — lightweight and easy for local dev, but less scalable.

To use Qdrant:

1. Install Qdrant locally with Docker (simple):

```powershell
# run Qdrant locally
docker run -p 6333:6333 -v qdrant_storage:/qdrant/storage -d qdrant/qdrant
```

2. Set environment variables in `.env`:

```
VECTOR_DB=qdrant
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=rag-index
```

3. Install Python client (already added to `requirements.txt`):

```powershell
pip install qdrant-client
```

4. Index PDFs using the same indexer script; it will upload vectors into Qdrant instead of Azure Search:

```powershell
python scripts\ai_indexer.py --index-folder data\pdfs
```

To use Chroma (local dev only):

1. Set `VECTOR_DB=chroma` in `.env` (note: script currently prefers qdrant or azure_search; I can add chroma on request).

2. Install `chromadb` and follow similar indexing steps (I can add code for Chroma if you want).

Qdrant is a recommended alternative if you cannot create Azure Cognitive Search. It works well with vector embeddings and can be hosted locally (Docker) or in the cloud.

## 4) Index your PDFs (RAG content)

You will put PDF files into a folder `data/pdfs/` in the project (create it).

To index all PDFs now run:

```powershell
python scripts\ai_indexer.py --index-folder data\pdfs
```

What this does (simple):

- Read each PDF.
- Split text into chunks.
- Ask Azure OpenAI for embeddings for each chunk.
- Upload chunks and embeddings to the Cognitive Search index.

After indexing, the chat endpoint will be able to retrieve relevant chunks and answer questions with RAG.

---

## 5) How to use the chat endpoint locally

Start the Flask app (depending on project setup, often):

```powershell
$env:FLASK_APP='app.py'; $env:FLASK_ENV='development'; flask run
```

Open the web UI: http://127.0.0.1:5000/ai-helper

In the UI you can type a message. The server will call Azure OpenAI and, if configured to use RAG, will first query Cognitive Search for relevant chunks.

---

## 6) Auto-index PDFs after merge (dumb but reliable way)

We add a GitHub Actions workflow that runs after merge to `main`. The workflow will:

1. Check out the code.
2. Install Python and dependencies.
3. Run `scripts/ai_indexer.py --index-folder data/pdfs`.

Place a workflow file `.github/workflows/reindex-on-merge.yml`. Example is included below in the script and also in this repo's docs example.

Be careful: You must set secrets in GitHub repository settings: `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_SEARCH_KEY`, `AZURE_SEARCH_ENDPOINT`, and `AZURE_SEARCH_INDEX`.

---

## 7) Deploy to Azure (App Service) — simple steps

1. Create an App Service (Linux or Windows) in Azure.
2. Configure App Service settings (Application settings) with the same env vars from `.env`.
3. In Azure, set up Deployment Center to deploy from GitHub `main` branch. Or use GitHub Actions to push to App Service.

If you use GitHub Actions, add an additional job that deploys the app and then runs the indexer job (or run indexer in a separate job).
---

## Deploying this project to Azure — step-by-step (for a child)

This section explains how to put your app on the internet using Azure App Service and a managed PostgreSQL database. Follow each small step exactly.

What you will create:
- a Resource Group (a folder for related things)
- an Azure Database for PostgreSQL (the app's database)
- an App Service Plan and a Web App (the place the app runs)

You will need:
- an Azure account and permission to create resources
- Azure CLI installed and you logged in (or use the Portal UI instead)

Step A — login with Azure CLI

Open PowerShell and run:

```powershell
az login
```

Step B — create a resource group (a container for your Azure things)

Pick names you like. Example below uses `bughunter-rg` and `eastus` region.

```powershell
az group create --name bughunter-rg --location eastus
```

Step C — create a PostgreSQL database (Flexible Server)

This will create the database that the app will use. Change the admin user and password to strong values.

```powershell
az postgres flexible-server create --resource-group bughunter-rg --name bughunter-db --location eastus --admin-user pgadmin --admin-password "P@ssw0rd123!" --sku-name Standard_B1ms

# Create a database inside the server
az postgres flexible-server db create --resource-group bughunter-rg --server-name bughunter-db --database-name bughunter
```

Get the connection string (you will put this into App Service settings):

```powershell
$conn = az postgres flexible-server show-connection-string --name bughunter-db --resource-group bughunter-rg --output tsv
Write-Output $conn
```

The app expects `DATABASE_URL` in the format: `postgresql://user:password@host:port/dbname`
Construct this string from the server info and set it in App Service later.

Step D — create an App Service plan and Web App

```powershell
az appservice plan create --name bughunter-plan --resource-group bughunter-rg --is-linux --sku B1
az webapp create --resource-group bughunter-rg --plan bughunter-plan --name my-bughunter-app --runtime "PYTHON|3.11"
```

`--name my-bughunter-app` must be globally unique (it becomes part of the URL). If it is taken, add numbers to the name.

Using the Azure Portal (UI) — step-by-step (very simple)

If you prefer the graphical Azure Portal instead of Azure CLI, follow these exact clicks. Do one step at a time.

1) Create a Resource Group

- Open https://portal.azure.com and sign in.
- In the left menu click "Resource groups".
- Click "+ Create".
- Choose your Subscription, enter a Resource group name (example: bughunter-rg), pick Region (example: East US), then click "Review + create" and then "Create".

2) Create Azure Database for PostgreSQL (Flexible Server) via Portal

- In the left menu click "Create a resource".
- Search for "Azure Database for PostgreSQL flexible server" and select it.
- Click "Create".
- Fill the form:
	- Subscription: your subscription
	- Resource group: select the resource group you just created (bughunter-rg)
	- Server name: a unique name, e.g. bughunter-db
	- Region: same region as your resource group
	- Workload details: choose Dev/Test for simplicity
	- Administrator username/password: choose and remember these
	- Click "Review + create" and then "Create" (wait until deployment completes).

Tip: After creating the server, open the server resource, go to "Connection security" and allow public access temporarily (or add your client IP) so you can connect from local machine. For production, use private networking.

3) Create App Service (Web App) via Portal

- In the left menu click "Create a resource" → search "Web App" → click "Create".
- Fill the form:
	- Subscription: your subscription
	- Resource group: bughunter-rg
	- Instance details: give a unique "Name" (this will be the URL, e.g. my-bughunter-app)
	- Publish: Code
	- Runtime stack: Python 3.11 (or 3.10/3.9 as available)
	- Operating System: Linux
	- Region: same as other resources
	- App Service Plan: create new (name: bughunter-plan) and choose Pricing plan B1 or Standard
- Click "Review + create" and then "Create".

4) Configure application settings (Environment variables) in Portal

- Open your Web App resource (search "App Services" → click your app).
- In the left menu under "Settings" click "Configuration" → "Application settings" tab.
- Click "+ New application setting" and add key/value pairs matching your `.env` entries. Example keys to add:
	- DATABASE_URL = postgresql://pgadmin:P@ssw0rd123!@<host>:5432/bughunter
	- JWT_SECRET_KEY = change-me
	- SECRET_KEY = change-me
	- AZURE_OPENAI_ENDPOINT = https://...
	- AZURE_OPENAI_KEY = ...
	- VECTOR_DB = qdrant
	- QDRANT_URL = http://<qdrant-host>:6333
	- QDRANT_COLLECTION = rag-index
- Click "Save" at the top.

5) Set Startup Command in Portal

- In the Web App left menu click "Settings" → "Configuration" → "General settings".
- Under "Startup Command" paste:

```
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

- Click "Save" and restart your Web App (top menu "Restart").

6) Deploy code from GitHub using Deployment Center (Portal)

- Open your Web App in the Portal.
- In the left menu click "Deployment Center".
- Choose source: GitHub. Click "Authorize" and sign-in to GitHub when asked.
- Select Organization, Repository, and Branch (main).
- Choose Build provider: GitHub Actions (recommended).
- Click "Finish" or "Save".

Azure will create a GitHub Actions workflow in your repo automatically (you can inspect it under `.github/workflows`). The action will build and deploy your app on each push to the chosen branch.

7) Get Publish Profile (optional — for manual deploys)

- Open the Web App resource -> Overview -> "Get publish profile" (top right).
- Download the XML. This can be used as `AZURE_WEBAPP_PUBLISH_PROFILE` secret in GitHub Actions.

8) Run the indexer after deployment

If you set up the GitHub Actions workflow (Deployment Center) you can edit the created workflow or add the `Run indexer` step from earlier to ensure PDFs get indexed after deploy. Alternatively, manually trigger the indexer by SSHing into the app or using an admin endpoint that runs the indexer.

9) Run Qdrant in Azure using Container Instances (UI)

If you want Qdrant hosted in Azure and prefer UI steps:

- In the Portal, click "Create a resource" and search for "Container Instances".
- Click "Create".
- Fill the form: choose Resource group `bughunter-rg`, give a container name (qdrant-instance), Region, and image: `qdrant/qdrant:latest`.
- In "Networking" choose "Public IP" so the container is reachable, set Port to 6333.
- Click "Review + create" and then "Create".

After the container is running, open the container instance resource -> "IP address" or "FQDN". Use that as `QDRANT_URL` in App Settings (for example `http://<fqdn>:6333`).

Notes and security

- For production, do not leave PostgreSQL public; use private networking (VNet) or managed networking between App Service and the database.
- For Qdrant, a public container is simple for testing, but in production consider using a VM, AKS, or managed vector DB with proper network restrictions.


Step E — configure App Settings (environment variables)

Set the same environment variables that you have in your local `.env`. Example below uses `my-bughunter-app` as web app name — change if yours is different.

```powershell
$appName = 'my-bughunter-app'
az webapp config appsettings set --name $appName --resource-group bughunter-rg --settings \
	DATABASE_URL="postgresql://pgadmin:P@ssw0rd123!@<host>:5432/bughunter" \
	JWT_SECRET_KEY="change-me" \
	SECRET_KEY="change-me" \
	AZURE_OPENAI_ENDPOINT="https://..." \
	AZURE_OPENAI_KEY="..." \
	VECTOR_DB="qdrant" \
	QDRANT_URL="http://<qdrant-host>:6333" \
	QDRANT_COLLECTION="rag-index"
```

Replace `<host>` with the actual host from your PostgreSQL server and fill in the keys for Azure OpenAI or other services you use.

Step F — set startup command

Set the web app to start with Gunicorn (recommended for Flask). In the Portal: Settings -> Configuration -> General settings -> Startup Command, put:

```
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

Step G — deploy your code with GitHub Actions (simple way)

1. In your GitHub repo go to Settings -> Secrets -> Actions and add a secret named `AZURE_WEBAPP_PUBLISH_PROFILE` that contains your Web App Publish Profile XML (download from Azure Portal -> Get publish profile).
2. Add the workflow file `.github/workflows/azure_deploy.yml` (example below). This workflow:
	 - runs on push to `main`
	 - installs Python dependencies
	 - runs the indexer to ensure PDFs are indexed
	 - deploys the app to Azure using the publish profile

Here is a ready-to-use example workflow (save it as `.github/workflows/azure_deploy.yml`):

```yaml
name: Deploy to Azure Web App

on:
	push:
		branches: [ main ]

jobs:
	build-and-deploy:
		runs-on: ubuntu-latest

		steps:
			- name: Checkout
				uses: actions/checkout@v4

			- name: Set up Python
				uses: actions/setup-python@v4
				with:
					python-version: '3.11'

			- name: Install dependencies
				run: |
					python -m pip install --upgrade pip
					pip install -r requirements.txt

			- name: Run indexer
				env:
					AZURE_OPENAI_KEY: ${{ secrets.AZURE_OPENAI_KEY }}
					AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
					VECTOR_DB: ${{ secrets.VECTOR_DB }}
					QDRANT_URL: ${{ secrets.QDRANT_URL }}
					QDRANT_API_KEY: ${{ secrets.QDRANT_API_KEY }}
					AZURE_SEARCH_ENDPOINT: ${{ secrets.AZURE_SEARCH_ENDPOINT }}
					AZURE_SEARCH_KEY: ${{ secrets.AZURE_SEARCH_KEY }}
					AZURE_SEARCH_INDEX: ${{ secrets.AZURE_SEARCH_INDEX }}
				run: |
					python scripts/ai_indexer.py --index-folder data/pdfs || echo "Indexer failed or no PDFs"

			- name: 'Deploy to Azure WebApp'
				uses: azure/webapps-deploy@v2
				with:
					app-name: 'my-bughunter-app' # change to your webapp name
					publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
					package: .

```

After the workflow runs successfully your app will be live at `https://my-bughunter-app.azurewebsites.net` (replace with your app name).

Step H — Post-deploy checks

- Visit the site URL to confirm it loads.
- Use the app login or create a test user to access protected AI endpoints.
- Check the GitHub Actions run logs for the indexer step and the deploy step to ensure everything succeeded.

---

If you want, I can add the `.github/workflows/azure_deploy.yml` file to the repository for you (with placeholders you can replace). I can also add a small `scripts/create_azure_resources.ps1` to create the resource group, postgres, and web app automatically if you prefer CLI-based setup.
---

## 8) Troubleshooting & notes

- If embeddings calls fail, ensure `AZURE_OPENAI_KEY` and endpoint are correct and the model name used is available in your region.
- If Cognitive Search rejects the vector field, verify your search service SKU and that vector search is enabled.
- Keep logs during indexing so you can inspect failed files.

---

## 9) Where the code I added lives

- `scripts/ai_indexer.py` — indexer script (reads PDFs and pushes them to search).
- `blueprints/ai_assistant.py` — Flask endpoints for chat, upload, and reindex.
- `docs/AI_ASSISTANT_SETUP.md` — this file.
- `requirements.txt` — updated to include Azure SDKs.

---

If you want, I can also add a sample GitHub Actions file to the repo that runs the indexer after merges and optionally deploys to Azure App Service. Tell me if you want that and I'll add it.

---

Thank you — follow each step slowly and paste errors here if something goes wrong.
