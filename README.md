# BugHunter - Full-Stack QA Management Portal

A comprehensive full-stack application for QA management, testing, and development tools.

## Features

- **Authentication System**: JWT-based authentication with user management
- **QA Tools**: Test Case Manager and Bug Report Manager
- **E-commerce Sandbox**: Personal shop management with products, cart, and orders
- **UI Playground**: Comprehensive collection of UI elements for automation testing
- **Task Tracker**: Kanban-style board for project management
- **AI Helper**: Chat interface for AI-powered assistance

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-JWT-Extended, Alembic
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Deployment**: Docker, Docker Compose, Nginx

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker and Docker Compose (for containerized deployment)

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```bash
   alembic upgrade head
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application at `http://localhost:5000`

### Docker Deployment

1. Build and start containers:
   ```bash
   docker-compose up -d
   ```

2. Access the application at `http://localhost`

## Project Structure

```
.
├── app.py                 # Main Flask application
├── models.py              # SQLAlchemy models
├── utils.py               # Utility functions
├── blueprints/            # Flask blueprints
│   ├── auth.py
│   ├── dashboard.py
│   ├── test_cases.py
│   ├── bug_reports.py
│   ├── ecommerce.py
│   ├── ui_playground.py
│   ├── task_tracker.py
│   └── ai_helper.py
├── templates/             # Jinja2 templates
├── static/                # Static files (CSS, JS)
├── migrations/            # Alembic migrations
├── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/user` - Get current user
- `POST /api/auth/logout` - Logout
- `PUT /api/auth/update` - Update user
- `POST /api/auth/change_role` - Toggle role

### Test Cases
- `GET /api/test-cases` - List test cases
- `GET /api/test-cases/<id>` - Get test case
- `POST /api/test-cases` - Create test case
- `PUT /api/test-cases/<id>` - Update test case
- `DELETE /api/test-cases/<id>` - Delete test case

### Bug Reports
- `GET /api/bug-reports` - List bug reports
- `GET /api/bug-reports/<id>` - Get bug report
- `POST /api/bug-reports` - Create bug report
- `PUT /api/bug-reports/<id>` - Update bug report
- `DELETE /api/bug-reports/<id>` - Delete bug report

### E-commerce
- `GET /api/shop` - Get shop
- `POST /api/shop` - Create shop
- `PUT /api/shop` - Update shop
- `GET /api/products` - List products
- `POST /api/products` - Create product
- `GET /api/cart` - Get cart
- `POST /api/cart` - Add to cart
- `POST /api/checkout` - Checkout
- `GET /api/orders` - List orders

### Task Tracker
- `GET /api/boards` - List boards
- `POST /api/boards` - Create board
- `GET /api/boards/<id>/columns` - List columns
- `POST /api/boards/<id>/columns` - Create column
- `POST /api/tasks` - Create task
- `PUT /api/tasks/<id>` - Update task

### AI Helper
- `POST /api/ai/chat` - Send chat message

## Security

- All API endpoints (except login/register) require JWT authentication
- Passwords are hashed using bcrypt
- JWT tokens stored in localStorage
- Server-side role enforcement

## License

MIT

