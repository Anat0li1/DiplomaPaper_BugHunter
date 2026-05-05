# BugHunter Setup Guide

## Quick Start

### Option 1: Docker (Recommended)

1. **Clone and navigate to the project directory**

2. **Create `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

3. **Start the application**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   - Frontend: http://localhost
   - Backend API: http://localhost:5000

5. **View logs**:
   ```bash
   docker-compose logs -f
   ```

6. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Option 2: Local Development

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database**:
   - Create a database named `bughunter`
   - Update `.env` with your database credentials

3. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Start the Flask application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   - Frontend: http://localhost:5000
   - Login page: http://localhost:5000/api/auth/login

## First Time Setup

1. **Register a new user**:
   - Navigate to the login page
   - Click "Register" tab
   - Fill in username, email, and password
   - Click "Register"

2. **Login**:
   - Use your registered email and password
   - You'll be redirected to the dashboard

3. **Explore the modules**:
   - **Dashboard**: Overview and navigation
   - **QA Tools**: Test Cases and Bug Reports
   - **E-commerce**: Create your shop and manage products
   - **UI Playground**: Practice automation testing
   - **Task Tracker**: Create Kanban boards
   - **AI Helper**: Chat interface

## Database Migrations

### Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
alembic upgrade head
```

### Rollback migration:
```bash
alembic downgrade -1
```

## Environment Variables

Key environment variables in `.env`:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Flask secret key (change in production!)
- `JWT_SECRET_KEY`: JWT signing key (change in production!)
- `FLASK_ENV`: Set to `production` for production deployment

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -U postgres -l`

### Migration Issues
- Ensure database is accessible
- Check `alembic.ini` configuration
- Try: `alembic current` to see current migration state

### Docker Issues
- Check container logs: `docker-compose logs backend`
- Rebuild containers: `docker-compose up -d --build`
- Reset database: `docker-compose down -v` (WARNING: deletes data)

## Production Deployment

1. **Update `.env`** with production values:
   - Strong `SECRET_KEY` and `JWT_SECRET_KEY`
   - Production database URL
   - Set `FLASK_ENV=production`

2. **Update `docker-compose.yml`**:
   - Remove port mappings if using Nginx
   - Set proper resource limits
   - Configure volumes for persistence

3. **Configure Nginx**:
   - Update `nginx.conf` with your domain
   - Set up SSL certificates
   - Configure proper headers

4. **Run migrations**:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

## API Documentation

All API endpoints require JWT authentication (except login/register).

Include the JWT token in the Authorization header:
```
Authorization: Bearer <your-token>
```

Tokens are stored in browser localStorage after login.

## Support

For issues or questions, check the README.md file or review the code documentation.

