from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv
import os

load_dotenv()

ai_helper_bp = Blueprint('ai_helper', __name__)

@ai_helper_bp.route('/ai-helper')
def ai_helper():
    return render_template('ai_helper/index.html')

@ai_helper_bp.route('/api/ai/chat', methods=['POST'])
@jwt_required()
def api_chat():
    """
    Надіслати повідомлення асистенту
    ---
    tags:
      - Асистент
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - message
          properties:
            message:
              type: string
    responses:
      200:
        description: Відповідь асистента
        schema:
          type: object
          properties:
            response:
              type: string
    """
    data = request.get_json()
    message = data.get('message', '')
    
    # Placeholder for future LLM integration.
    response = (
        f"Відповідь асистента (демо): ви написали «{message}». "
        "Це тестова відповідь. Налаштуйте ключ LLM у .env, щоб увімкнути реальні відповіді."
    )
    
    return jsonify({'response': response}), 200
