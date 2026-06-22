# BugHunter — Повнофункціональний портал управління QA

Комплексний full-stack застосунок для управління QA, тестування та інструментів розробки.

## Можливості

* **Система автентифікації**: автентифікація на основі JWT з керуванням користувачами
* **QA-інструменти**: менеджер тест-кейсів та менеджер звітів про помилки
* **Пісочниця електронної комерції**: керування власним магазином, товарами, кошиком і замовленнями
* **UI Playground**: велика колекція елементів інтерфейсу для тестування автоматизації
* **Трекер завдань**: дошка в стилі Kanban для керування проєктами
* **AI-помічник**: чат-інтерфейс для отримання допомоги на основі штучного інтелекту

## Технологічний стек

* **Бекенд**: Flask, SQLAlchemy, Flask-JWT-Extended, Alembic
* **База даних**: PostgreSQL
* **Фронтенд**: HTML, CSS, JavaScript (без фреймворків)
* **Розгортання**: Docker, Docker Compose, Nginx

## Налаштування

### Попередні вимоги

* Python 3.11+
* PostgreSQL 15+
* Docker та Docker Compose (для контейнеризованого розгортання)

### Локальна розробка

1. Клонуйте репозиторій.

2. Встановіть залежності:

   ```bash
   pip install -r requirements.txt
   ```

3. Налаштуйте змінні середовища:

   ```bash
   cp .env.example .env
   # Відредагуйте .env відповідно до вашої конфігурації
   ```

4. Ініціалізуйте базу даних:

   ```bash
   alembic upgrade head
   ```

5. Запустіть застосунок:

   ```bash
   python app.py
   ```

6. Відкрийте застосунок за адресою `http://localhost:5000`

### Розгортання через Docker

1. Зберіть та запустіть контейнери:

   ```bash
   docker-compose up -d
   ```

2. Відкрийте застосунок за адресою `http://localhost`

## Структура проєкту

```text
.
├── app.py                 # Основний застосунок Flask
├── models.py              # Моделі SQLAlchemy
├── utils.py               # Допоміжні функції
├── blueprints/            # Flask Blueprint-модулі
│   ├── auth.py
│   ├── dashboard.py
│   ├── test_cases.py
│   ├── bug_reports.py
│   ├── ecommerce.py
│   ├── ui_playground.py
│   ├── task_tracker.py
│   └── ai_helper.py
├── templates/             # Шаблони Jinja2
├── static/                # Статичні файли (CSS, JS)
├── migrations/            # Міграції Alembic
├── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

## API-ендпоінти

### Автентифікація

* `POST /api/auth/register` — Реєстрація нового користувача
* `POST /api/auth/login` — Вхід у систему
* `GET /api/auth/user` — Отримання даних поточного користувача
* `POST /api/auth/logout` — Вихід із системи
* `PUT /api/auth/update` — Оновлення даних користувача
* `POST /api/auth/change_role` — Перемикання ролі

### Тест-кейси

* `GET /api/test-cases` — Отримати список тест-кейсів
* `GET /api/test-cases/<id>` — Отримати тест-кейс
* `POST /api/test-cases` — Створити тест-кейс
* `PUT /api/test-cases/<id>` — Оновити тест-кейс
* `DELETE /api/test-cases/<id>` — Видалити тест-кейс

### Звіти про помилки

* `GET /api/bug-reports` — Отримати список звітів про помилки
* `GET /api/bug-reports/<id>` — Отримати звіт про помилку
* `POST /api/bug-reports` — Створити звіт про помилку
* `PUT /api/bug-reports/<id>` — Оновити звіт про помилку
* `DELETE /api/bug-reports/<id>` — Видалити звіт про помилку

### Електронна комерція

* `GET /api/shop` — Отримати дані магазину
* `POST /api/shop` — Створити магазин
* `PUT /api/shop` — Оновити магазин
* `GET /api/products` — Отримати список товарів
* `POST /api/products` — Створити товар
* `GET /api/cart` — Отримати кошик
* `POST /api/cart` — Додати товар до кошика
* `POST /api/checkout` — Оформити замовлення
* `GET /api/orders` — Отримати список замовлень

### Трекер завдань

* `GET /api/boards` — Отримати список дощок
* `POST /api/boards` — Створити дошку
* `GET /api/boards/<id>/columns` — Отримати список колонок
* `POST /api/boards/<id>/columns` — Створити колонку
* `POST /api/tasks` — Створити завдання
* `PUT /api/tasks/<id>` — Оновити завдання

### AI-помічник

* `POST /api/ai/chat` — Надіслати повідомлення в чат

## Безпека

* Усі API-ендпоінти (крім входу та реєстрації) вимагають JWT-автентифікації
* Паролі хешуються за допомогою bcrypt
* JWT-токени зберігаються в `localStorage`
* Контроль ролей реалізований на стороні сервера

## Ліцензія

MIT
