from flask import Flask, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flasgger import Swagger
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens don't expire
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/bughunter')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
jwt = JWTManager(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "BugHunter API",
        "description": "API documentation for BugHunter application",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

from models import db
db.init_app(app)
migrate = Migrate(app, db)

# Import blueprints
from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.test_cases import test_cases_bp
from blueprints.bug_reports import bug_reports_bp
from blueprints.ecommerce import ecommerce_bp
from blueprints.ui_playground import ui_playground_bp
from blueprints.task_tracker import task_tracker_bp
from blueprints.ai_helper import ai_helper_bp
from blueprints.ai_assistant import ai_bp as ai_assistant_bp
from blueprints.profile import profile_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(dashboard_bp)
app.register_blueprint(test_cases_bp)
app.register_blueprint(bug_reports_bp)
app.register_blueprint(ecommerce_bp)
app.register_blueprint(ui_playground_bp)
app.register_blueprint(task_tracker_bp)
app.register_blueprint(ai_helper_bp)
app.register_blueprint(ai_assistant_bp, url_prefix='/ai')
app.register_blueprint(profile_bp)

@app.route('/')
def index():
    return redirect('/api/auth/login')

@app.route('/login.html')
def login_redirect():
    return redirect('/api/auth/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

