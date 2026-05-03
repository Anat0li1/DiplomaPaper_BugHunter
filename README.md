# Портал якості

Full-stack застосунок для QA-процесів, тестування інтерфейсів, керування дефектами, задачами та тестовим магазином.

## Можливості

- **Автентифікація**: JWT-вхід, реєстрація, профіль і зміна пароля.
- **QA-інструменти**: керування тест-кейсами та баг-репортами.
- **Тестовий магазин**: власний магазин, товари, категорії, кошик і замовлення.
- **UI-полігон**: набір елементів для тренування автоматизованого тестування.
- **Трекер задач**: Kanban-дошки, колонки та задачі.
- **Асистент**: чат-інтерфейс із підтримкою RAG через Azure OpenAI/Azure AI Search, якщо задані відповідні змінні середовища.

## Технології

- **Backend**: Flask, SQLAlchemy, Flask-JWT-Extended, Alembic.
- **База даних**: PostgreSQL.
- **Frontend**: HTML, CSS, JavaScript.
- **Деплой**: Docker, Docker Compose, Nginx, GitHub Actions, Azure Web App.

## Локальний запуск

1. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```

2. Створіть `.env` на основі `.env.example` і заповніть потрібні значення.

3. Застосуйте міграції:
   ```bash
   alembic upgrade head
   ```

4. Запустіть застосунок:
   ```bash
   python app.py
   ```

5. Відкрийте `http://localhost:5000`.

## Docker

```bash
docker-compose up -d
```

Після старту застосунок доступний на `http://localhost`.

## Міграції

Створити нову міграцію:

```bash
alembic revision --autogenerate -m "короткий опис змін"
```

Застосувати міграції:

```bash
alembic upgrade head
```

CI виконує `alembic upgrade head` на PostgreSQL-сервісі та `alembic check`, тому зміни моделей без міграцій не мають проходити перевірку.

## Основні API

- `POST /api/auth/register` - реєстрація.
- `POST /api/auth/login` - вхід.
- `GET /api/auth/user` - поточний користувач.
- `PUT /api/auth/update` - оновлення профілю або пароля.
- `GET/POST /api/test-cases` - список і створення тест-кейсів.
- `GET/PUT/DELETE /api/test-cases/<id>` - робота з тест-кейсом.
- `GET/POST /api/bug-reports` - список і створення баг-репортів.
- `GET/PUT/DELETE /api/bug-reports/<id>` - робота з баг-репортом.
- `GET/POST/PUT /api/shop` - магазин користувача.
- `GET/POST /api/products` - товари.
- `GET/POST /api/cart` - кошик.
- `POST /api/checkout` - оформлення замовлення.
- `GET/POST /api/boards` - Kanban-дошки.
- `POST /api/tasks` - створення задачі.
- `POST /ai/api/ai/chat` - чат асистента.

## Безпека

- Усі API, крім входу та реєстрації, потребують JWT.
- Паролі хешуються через bcrypt.
- Вихід додає JWT до blocklist.
- `.env`, `venv`, кеші Python і локальні артефакти не мають потрапляти в репозиторій.
