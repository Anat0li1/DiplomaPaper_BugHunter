# Портал якості вЂ” РљРѕСЂРѕС‚РєРёР№ Р РµР·СЋРјРµ РґР»СЏ РЁРІРёРґРєРѕРіРѕ РћР·РЅР°Р№РѕРјР»РµРЅРЅСЏ

## Executive Summary

### РќР°Р·РІР° РџСЂРѕРµРєС‚Сѓ

**Портал якості** вЂ” РљРѕРјРїР»РµРєСЃРЅРёР№ РїРѕСЂС‚Р°Р» РґР»СЏ СѓРїСЂР°РІР»С–РЅРЅСЏ СЏРєС–СЃС‚СЋ С‚Р° С‚РµСЃС‚СѓРІР°РЅРЅСЏ Р· AI Р°СЃРёСЃС‚РµРЅС‚РѕРј

### РћСЃРЅРѕРІРЅР° РњРµС‚Р°

Р РѕР·СЂРѕР±РёС‚Рё РїРѕРІРЅРѕС„СѓРЅРєС†С–РѕРЅР°Р»СЊРЅСѓ РІРµР±-РїР»Р°С‚С„РѕСЂРјСѓ, СЏРєР° РѕР±'С”РґРЅСѓС” С–РЅСЃС‚СЂСѓРјРµРЅС‚Рё QA-С‚РµСЃС‚СѓРІР°РЅРЅСЏ, СѓРїСЂР°РІР»С–РЅРЅСЏ РїРѕРјРёР»РєР°РјРё, РµР»РµРєС‚СЂРѕРЅРЅСѓ РєРѕРјРµСЂС†С–СЋ С‚Р° AI-Р°СЃРёСЃС‚РµРЅС‚ РЅР° РѕРґРЅС–Р№ РїР»Р°С‚С„РѕСЂРјС–.

### РљР»СЋС‡РѕРІС– РљРѕРјРїРѕРЅРµРЅС‚Рё

| РљРѕРјРїРѕРЅРµРЅС‚                | РћРїРёСЃ                                                      | РЎС‚Р°С‚СѓСЃ              |
| ------------------------ | --------------------------------------------------------- | ------------------- |
| **Test Case Management** | РЈРїСЂР°РІР»С–РЅРЅСЏ С‚РµСЃС‚РѕРІРёРјРё РІРёРїР°РґРєР°РјРё Р· РєСЂРѕРєР°РјРё С‚Р° preconditions | вњ… Р“РѕС‚РѕРІРѕ           |
| **Bug Reporting**        | Р РµС”СЃС‚СЂР°С†С–СЏ С‚Р° РІС–РґСЃС‚РµР¶РµРЅРЅСЏ РїРѕРјРёР»РѕРє Р· severity/priority     | вњ… Р“РѕС‚РѕРІРѕ           |
| **E-Commerce**           | РџР»Р°С‚С„РѕСЂРјР° РґР»СЏе€›е»єРјР°РіР°Р·РёРЅРѕРІ, С‚РѕРІР°СЂС–РІ, РєРѕС€РёРєС–РІ, Р·Р°РјРѕРІР»РµРЅСЊ   | вњ… Р“РѕС‚РѕРІРѕ           |
| **Task Tracker**         | Kanban РґРѕС€РєР° РґР»СЏ СѓРїСЂР°РІР»С–РЅРЅСЏ РїСЂРѕРµРєС‚РЅРёРјРё Р·Р°РІРґР°РЅРЅСЏРјРё         | вњ… Р“РѕС‚РѕРІРѕ           |
| **Асистент (RAG)**   | Р†РЅС‚РµР»РµРєС‚СѓР°Р»СЊРЅРёР№ Р°СЃРёСЃС‚РµРЅС‚ РЅР° Р±Р°Р·С– LLM Р· vector search      | вњ… Р“РѕС‚РѕРІРѕ (Р· Azure) |
| **Authentication**       | JWT-based СЃРёСЃС‚РµРјР° Р· bcrypt РїР°СЂРѕР»СЏРјРё                       | вњ… Р“РѕС‚РѕРІРѕ           |
| **UI Playground**        | Р”РµРјРѕРЅСЃС‚СЂР°С†С–СЏ UI РµР»РµРјРµРЅС‚С–РІ РґР»СЏ С‚РµСЃС‚СѓРІР°РЅРЅСЏ                  | вњ… Р“РѕС‚РѕРІРѕ           |

---

## РўРµС…РЅС–С‡РЅРёР№ РЎС‚РµРє

### Backend

```
Flask 3.0.0              - Web framework
SQLAlchemy 2.0.46        - ORM
PostgreSQL 15+           - Database
Alembic 1.13.1           - Migrations
Flask-JWT-Extended 4.6.0 - Authentication
bcrypt 4.1.2             - Password hashing
```

### Frontend

```
HTML5 + Jinja2 Templates
CSS3 (responsive)
Vanilla JavaScript ES6+
```

### Infrastructure

```
Docker + Docker Compose  - Containerization
Nginx (Alpine)           - Reverse proxy
```

### AI/ML

```
Azure OpenAI (gpt-4.1-mini)       - LLM
Azure Embeddings (text-embedding-3-small) - Vector embeddings
Azure Cognitive Search            - Vector database
OR Qdrant                         - Local alternative
```

---

## РђСЂС…С–С‚РµРєС‚СѓСЂР°

### РўСЂРёСЂС–РІРЅРµРІР° Р°СЂС…С–С‚РµРєС‚СѓСЂР°:

```
в”Њв”Ђ Frontend (HTML/CSS/JS)     в”Ђв”ђ
в”‚ Jinja2 С€Р°Р±Р»РѕРЅРё              в”‚
в”‚ Vanilla JS + Forms          в”‚
в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”¬в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”
           в”‚ HTTP/REST API
           в†“
в”Њв”Ђ Backend (Flask)            в”Ђв”ђ
в”‚ 10+ Blueprints              в”‚
в”‚ 50+ API endpoints           в”‚
в”‚ JWT Authentication          в”‚
в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”¬в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”
           в”‚
    в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ґв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”¬в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ
    в†“             в†“          в†“
PostgreSQL   Azure OpenAI  Azure Search
Database     (LLM)         (Vector DB)
```

---

## РЎС‚СЂСѓРєС‚СѓСЂР° РџСЂРѕРµРєС‚Сѓ

```
cursor-try-2/
в”њв”Ђв”Ђ app.py                    # Flask app (102 lines)
в”њв”Ђв”Ђ models.py                 # 10+ SQLAlchemy models
в”њв”Ђв”Ђ utils.py                  # Password utilities
в”њв”Ђв”Ђ blueprints/               # 10 modular routes
в”‚   в”њв”Ђв”Ђ auth.py              # Auth (252 lines)
в”‚   в”њв”Ђв”Ђ test_cases.py        # Test management
в”‚   в”њв”Ђв”Ђ bug_reports.py       # Bug management
в”‚   в”њв”Ђв”Ђ ecommerce.py         # Shop/cart/orders
в”‚   в”њв”Ђв”Ђ task_tracker.py      # Kanban board
в”‚   в”њв”Ђв”Ђ ai_helper.py         # AI chat
в”‚   в”њв”Ђв”Ђ ai_assistant.py      # RAG backend
в”‚   в””в”Ђв”Ђ ... (С–РЅС€С– РјРѕРґСѓР»С–)
в”њв”Ђв”Ђ templates/                # 15+ HTML С€Р°Р±Р»РѕРЅС–РІ
в”њв”Ђв”Ђ static/                   # CSS, JS
в”њв”Ђв”Ђ migrations/               # Alembic versions
в”њв”Ђв”Ђ docker-compose.yml        # Multi-container setup
в”њв”Ђв”Ђ Dockerfile                # Flask image
в”њв”Ђв”Ђ nginx.conf                # Reverse proxy
в””в”Ђв”Ђ docs/                     # Documentation
    в””в”Ђв”Ђ AI_ASSISTANT_SETUP.md
```

---

## РћСЃРЅРѕРІРЅС– Р¤СѓРЅРєС†С–С—

### 1. РђРІС‚РµРЅС‚РёС„С–РєР°С†С–СЏ

- вњ… Р РµС”СЃС‚СЂР°С†С–СЏ РєРѕСЂРёСЃС‚СѓРІР°С‡Р°
- вњ… Р›РѕРіС–РЅ Р· JWT С‚РѕРєРµРЅРѕРј
- вњ… Р‘РµР·РїРµС‡РЅРµ Р·Р±РµСЂС–РіР°РЅРЅСЏ РїР°СЂРѕР»СЋ (bcrypt)
- вњ… User profile management

### 2. РЈРїСЂР°РІР»С–РЅРЅСЏ С‚РµСЃС‚РѕРІРёРјРё РІРёРїР°РґРєР°РјРё

- вњ… РЎС‚РІРѕСЂРµРЅРЅСЏ/СЂРµРґР°РіСѓРІР°РЅРЅСЏ test cases
- вњ… РћСЂРіР°РЅС–Р·Р°С†С–СЏ РїРѕ groups С‚Р° priority
- вњ… Р’РёР·РЅР°С‡РµРЅРЅСЏ steps, test data, expected results
- вњ… Version control С‚Р° environment specification

### 3. РЈРїСЂР°РІР»С–РЅРЅСЏ РїРѕРјРёР»РєР°РјРё

- вњ… Р РµС”СЃС‚СЂР°С†С–СЏ bug reports
- вњ… Р’СЃС‚Р°РЅРѕРІР»РµРЅРЅСЏ severity (Critical/High/Medium/Low)
- вњ… Р’СЃС‚Р°РЅРѕРІР»РµРЅРЅСЏ priority С‚Р° status
- вњ… Р—РІ'СЏР·СѓРІР°РЅРЅСЏ Р· test cases

### 4. E-Commerce РјРѕРґСѓР»СЊ

- вњ… РЎС‚РІРѕСЂРµРЅРЅСЏ РјР°РіР°Р·РёРЅС–РІ
- вњ… РЈРїСЂР°РІР»С–РЅРЅСЏ С‚РѕРІР°СЂР°РјРё С‚Р° РєР°С‚РµРіРѕСЂС–СЏРјРё
- вњ… Shopping cart
- вњ… Orders С– РІС–РґСЃС‚РµР¶РµРЅРЅСЏ

### 5. Task Tracker

- вњ… Kanban РґРѕС€РєРё
- вњ… РџРµСЂРµРјС–С‰РµРЅРЅСЏ РєР°СЂС‚РѕРє РјС–Р¶ РєРѕР»РѕРЅРєР°РјРё
- вњ… Р’СЃС‚Р°РЅРѕРІР»РµРЅРЅСЏ РїСЂС–РѕСЂРёС‚РµС‚Сѓ С‚Р° РІРёРєРѕРЅР°РІС†СЏ
- вњ… Р§Р°СЃ РІРёРєРѕРЅР°РЅРЅСЏ

### 6. Асистент (RAG)

- вњ… Chat interface
- вњ… Vector embedding (Azure Embeddings)
- вњ… Document retrieval (Azure Search / Qdrant)
- вњ… LLM integration (Azure OpenAI)

---

## Р‘Р°Р·Р° Р”Р°РЅРёС…

### РўР°Р±Р»РёС†С– (10+):

- **users** - 5 Р°С‚СЂРёР±СѓС‚С–РІ
- **test_cases** - 11 Р°С‚СЂРёР±СѓС‚С–РІ + steps
- **test_steps** - РєСЂРѕРєРё С‚РµСЃС‚СѓРІР°РЅРЅСЏ
- **bug_reports** - 13 Р°С‚СЂРёР±СѓС‚С–РІ + steps
- **bug_steps** - РєСЂРѕРєРё РґР»СЏ РІС–РґС‚РІРѕСЂРµРЅРЅСЏ
- **shops** - РјР°РіР°Р·РёРЅ РєРѕСЂРёСЃС‚СѓРІР°С‡Р°
- **products** - С‚РѕРІР°СЂРё (10 Р°С‚СЂРёР±СѓС‚С–РІ)
- **categories** - РєР°С‚РµРіРѕСЂС–С— С‚РѕРІР°СЂС–РІ
- **orders** - Р·Р°РјРѕРІР»РµРЅРЅСЏ
- **order_items** - РїРѕР·РёС†С–С— Р·Р°РјРѕРІР»РµРЅРЅСЏ
- **cart_items** - РєРѕС€РёРє
- **boards, columns, tasks** - task tracker

### Р—РІ'СЏР·РєРё:

- One-to-Many: User в†’ TestCases, BugReports, Orders
- One-to-One: User в†’ Shop
- Cascade delete РґР»СЏ dependent entities

---

## API Endpoints (50+)

### Authentication (6):

```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/auth/user
POST   /api/auth/logout
PUT    /api/auth/update
POST   /api/auth/change_role
```

### Test Cases (6+):

```
GET    /api/test-cases
GET    /api/test-cases/<id>
POST   /api/test-cases
PUT    /api/test-cases/<id>
DELETE /api/test-cases/<id>
```

### Bug Reports (6+):

```
GET    /api/bug-reports
GET    /api/bug-reports/<id>
POST   /api/bug-reports
PUT    /api/bug-reports/<id>
DELETE /api/bug-reports/<id>
```

### E-Commerce (8+):

```
GET    /api/shop
POST   /api/shop
GET    /api/products
POST   /api/products
GET    /api/cart
POST   /api/cart
GET    /api/orders
POST   /api/orders
```

### Task Tracker (5+):

```
GET    /api/boards
POST   /api/boards
GET    /api/tasks
POST   /api/tasks
```

### AI (3+):

```
POST   /api/ai/chat
```

---

## RAG Pipeline

```
User Query
    в†“
1. Query Embedding (Azure OpenAI)
    в†“
2. Vector Search (Azure Search / Qdrant)
    в†“
3. Retrieve Top-5 Documents (max 2000 chars)
    в†“
4. Prepare LLM Context
    в†“
5. Call LLM (Azure OpenAI gpt-4.1-mini)
    в†“
AI Response with Context
```

---

## Р‘РµР·РїРµРєР°

### Р РµР°Р»С–Р·РѕРІР°РЅРѕ:

- вњ… Password Hashing (bcrypt)
- вњ… JWT Authentication
- вњ… SQL Injection Prevention (SQLAlchemy ORM)
- вњ… CORS Configuration
- вњ… Environment Variables (.env)
- вњ… Stateless Sessions

### Р РµРєРѕРјРµРЅРґР°С†С–С— РґР»СЏ Production:

- рџ”’ Rate Limiting (Flask-Limiter)
- рџ”’ HTTPS/TLS Certificate
- рџ”’ Azure Key Vault for secrets
- рџ”’ WAF (Web Application Firewall)
- рџ”’ Input Sanitization

---

## Р РѕР·РіРѕСЂС‚Р°РЅРЅСЏ

### Р›РѕРєР°Р»СЊРЅРѕ:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python app.py
```

### Docker:

```bash
docker-compose up -d
# Access at http://localhost
```

### Р’РёРјРѕРіРё:

- Python 3.11+
- PostgreSQL 15+
- Azure OpenAI API Key (РѕРїС†С–РѕРЅР°Р»СЊРЅРѕ)

---

## РЎС‚Р°С‚РёСЃС‚РёРєР°

| РњРµС‚СЂРёРєР°         | Р—РЅР°С‡РµРЅРЅСЏ |
| --------------- | -------- |
| Python С„Р°Р№Р»С–РІ   | 12+      |
| HTML С€Р°Р±Р»РѕРЅС–РІ   | 15+      |
| API Endpoints   | 50+      |
| Database tables | 10+      |
| Lines of Code   | 3500+    |
| РњРѕРґСѓР»С– Flask    | 10       |

---

## Р’РёРєРѕСЂРёСЃС‚Р°РЅРµ Р—РЅР°РЅРЅСЏ

### Backend:

- REST API Design вњ…
- ORM (SQLAlchemy) вњ…
- Database Design вњ…
- Authentication (JWT) вњ…
- Error Handling вњ…

### Frontend:

- HTML5 + Jinja2 вњ…
- CSS3 Responsive Design вњ…
- JavaScript ES6+ вњ…
- API Integration вњ…
- Form Validation вњ…

### DevOps:

- Docker & Docker Compose вњ…
- Nginx Reverse Proxy вњ…
- Database Migrations (Alembic) вњ…
- Environment Management вњ…

### AI/ML:

- LLM Integration (Azure OpenAI) вњ…
- Vector Embeddings вњ…
- RAG Architecture вњ…
- Vector Search (Azure Search / Qdrant) вњ…

### Database:

- PostgreSQL вњ…
- Relational Schema Design вњ…
- Foreign Keys & Relationships вњ…
- Indexing Strategy вњ…

---

## Р”Р»СЏ Р‘Р°РєР°Р»Р°РІСЂСЃСЊРєРѕС— Р РѕР±РѕС‚Рё

### Р РµРєРѕРјРµРЅРґРѕРІР°РЅР° РЎС‚СЂСѓРєС‚СѓСЂР°:

1. **Р’РІРµРґРµРЅРЅСЏ** - РњРѕС‚РёРІР°С†С–СЏ С‚Р° РїСЂРѕР±Р»РµРјР°
2. **РћРіР»СЏРґ Р»С–С‚РµСЂР°С‚СѓСЂРё** - РўРµС…РЅРѕР»РѕРіС–С— С‚Р° Р°РЅР°Р»РѕРіРё
3. **РђРЅР°Р»С–Р· РІРёРјРѕРі** - Р¤СѓРЅРєС†С–РѕРЅР°Р»СЊРЅС– С‚Р° РЅРµС„СѓРЅРєС†С–РѕРЅР°Р»СЊРЅС–
4. **Р”РёР·Р°Р№РЅ** - РђСЂС…С–С‚РµРєС‚СѓСЂР° С‚Р° РјРѕРґСѓР»С–
5. **Р РµР°Р»С–Р·Р°С†С–СЏ** - Backend, Frontend, AI, DevOps
6. **РўРµСЃС‚СѓРІР°РЅРЅСЏ** - Unit, Integration, E2E С‚РµСЃС‚Рё
7. **Р РѕР·РіРѕСЂС‚Р°РЅРЅСЏ** - Local, Docker, Cloud
8. **Р РµР·СѓР»СЊС‚Р°С‚Рё** - Р”РѕСЃСЏРіРЅРµРЅРЅСЏ С‚Р° РјРµС‚СЂРёРєРё
9. **Р’РёСЃРЅРѕРІРєРё** - РЁР»СЏС…Рё СЂРѕР·РІРёС‚РєСѓ

### РљР»СЋС‡РѕРІС– РњРѕРјРµРЅС‚Рё РґР»СЏ РџС–РґРєСЂРµСЃР»РµРЅРЅСЏ:

- рџЊџ Р†РЅС‚РµРіСЂР°С†С–СЏ 5+ С‚РµС…РЅРѕР»РѕРіС–Р№ (Flask, PostgreSQL, Docker, Azure AI, Azure Search)
- рџЊџ RAG Р°СЂС…С–С‚РµРєС‚СѓСЂР° РґР»СЏ С–РЅС‚РµР»РµРєС‚СѓР°Р»СЊРЅРѕС— РґРѕРїРѕРјРѕРіРё
- рџЊџ РњР°СЃС€С‚Р°Р±РѕРІР°РЅР° РґРѕ РјС–Р»СЊР№РѕРЅС–РІ РєРѕСЂРёСЃС‚СѓРІР°С‡С–РІ
- рџЊџ Production-ready РєРѕРґ Р· best practices
- рџЊџ РљРѕРЅС‚РµР№РЅРµСЂРёР·Р°С†С–СЏ С‚Р° Cloud РіРѕС‚РѕРІРЅС–СЃС‚СЊ

---

## РќРѕРІС– Р¤СѓРЅРєС†С–С— РґР»СЏ Р РѕР·РІРёС‚РєСѓ

### Short-term (1-3 РјС–СЃСЏС†С–):

- [ ] WebSocket РґР»СЏ real-time updates
- [ ] File uploads РґР»СЏ artifacts
- [ ] Advanced filtering С‚Р° sorting
- [ ] Email notifications

### Medium-term (3-6 РјС–СЃСЏС†С–РІ):

- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Performance monitoring (ELK)
- [ ] Multi-language support (i18n)
- [ ] Advanced AI features

### Long-term (6-12 РјС–СЃСЏС†С–РІ):

- [ ] Mobile app (React Native)
- [ ] Machine Learning predictions
- [ ] Jira/DevOps integration
- [ ] Distributed testing framework

---

## РџРѕСЃРёР»Р°РЅРЅСЏ

- **GitHub Repository:** [Project Repo Link]
- **API Docs:** http://localhost:5000/docs (Swagger)
- **AI Setup:** /docs/AI_ASSISTANT_SETUP.md
- **Requirements.txt:** /requirements.txt
- **Docker Compose:** /docker-compose.yml

---

## РљРѕРЅС‚Р°РєС‚Рё С‚Р° Р”РѕРґР°С‚РєРѕРІР° Р†РЅС„РѕСЂРјР°С†С–СЏ

**РџСЂРѕРµРєС‚:** Портал якості
**РЎС‚Р°С‚СѓСЃ:** РџРѕРІРЅР° РіРѕС‚РѕРІРЅС–СЃС‚СЊ РґРѕ РґРµРјРѕРЅСЃС‚СЂР°С†С–С—
**Р”Р°С‚Р°:** 23 Р»СЋС‚РѕРіРѕ 2026
**РђРІС‚РѕСЂ:** [Р’Р°С€Рµ С–Рј'СЏ]

Р¦РµР№ РґРѕРєСѓРјРµРЅС‚ РјС–СЃС‚РёС‚СЊ СѓСЃСЋ РЅРµРѕР±С…С–РґРЅСѓ С–РЅС„РѕСЂРјР°С†С–СЋ РґР»СЏ РЅР°РїРёСЃР°РЅРЅСЏ СЏРєС–СЃРЅРѕС— Р±Р°РєР°Р»Р°РІСЂСЃСЊРєРѕС— СЂРѕР±РѕС‚Рё.

---

**РћРЅРѕРІР»РµРЅРѕ:** 23 Р»СЋС‚РѕРіРѕ 2026

