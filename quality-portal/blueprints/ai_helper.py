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
    Send chat message to AI
    ---
    tags:
      - AI Helper
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
        description: AI response
        schema:
          type: object
          properties:
            response:
              type: string
    """
    data = request.get_json()
    message = data.get('message', '')
    
    # Placeholder for LLM integration
    # In production, integrate with OpenAI, Anthropic, etc.
    response = f"AI Response (placeholder): You said '{message}'. This is a mock response. Configure your LLM API key in .env to enable real AI responses."
    
    return jsonify({'response': response}), 200

