# Налаштування Порталу якості

## Швидкий старт через Docker

1. Скопіюйте `.env.example` у `.env` і заповніть значення.
2. Запустіть контейнери:
   ```bash
   docker-compose up -d
   ```
3. Застосуйте міграції, якщо база ще порожня:
   ```bash
   docker-compose exec web alembic upgrade head
   ```
4. Відкрийте застосунок:
   - веб-інтерфейс: `http://localhost`
   - API напряму: `http://localhost:5000`

## Локальний запуск без Docker

1. Встановіть Python 3.11+ і PostgreSQL 15+.
2. Створіть базу, наприклад `bughunter`.
3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
4. Налаштуйте `DATABASE_URL` у `.env`.
5. Застосуйте міграції:
   ```bash
   alembic upgrade head
   ```
6. Запустіть застосунок:
   ```bash
   python app.py
   ```

## Міграції

Нова міграція:

```bash
alembic revision --autogenerate -m "опис змін"
```

Застосування:

```bash
alembic upgrade head
```

Перевірка синхронізації моделей і міграцій:

```bash
alembic check
```

## Production

Для GitHub Actions потрібні секрети:

- `AZURE_WEBAPP_NAME`
- `AZURE_CREDENTIALS`
- `AZURE_RESOURCE_GROUP`
- `DATABASE_URL`

CI/CD спершу перевіряє код і міграції на тестовій PostgreSQL-базі, а перед деплоєм застосовує міграції production-бази. Якщо міграції не проходять, деплой зупиняється.
