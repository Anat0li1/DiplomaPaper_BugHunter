"""Створити користувача напряму в базі даних Flask-застосунку.

Використання з кореня проєкту з активованим venv:

python scripts\create_user.py username email password [role]

Скрипт імпортує Flask-застосунок і записує користувача в налаштовану базу.
"""
import sys
import os

# Make sure the app package is importable.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User
from utils import hash_password


def create_user(username, email, password, role='user'):
    with app.app_context():
        if User.query.filter_by(email=email).first():
            print('Користувач вже існує:', email)
            return
        u = User(username=username, email=email, password_hash=hash_password(password), active_role=role)
        db.session.add(u)
        db.session.commit()
        print('Користувача створено:', email)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Використання: python scripts/create_user.py username email password [role]')
        sys.exit(1)
    _, username, email, password, *rest = sys.argv
    role = rest[0] if rest else 'user'
    create_user(username, email, password, role)
