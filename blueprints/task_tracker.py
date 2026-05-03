from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Board, Column, Task
from sqlalchemy import func

task_tracker_bp = Blueprint('task_tracker', __name__)

@task_tracker_bp.route('/task-tracker')
def list_boards():
    return render_template('task_tracker/boards.html')

@task_tracker_bp.route('/task-tracker/board/<id>')
def board_view(id):
    return render_template('task_tracker/board.html', board_id=id)

# API endpoints
@task_tracker_bp.route('/api/boards', methods=['GET'])
@jwt_required()
def api_list_boards():
    """
    Отримати список дошок
    ---
    tags:
      - Трекер задач
    security:
      - Bearer: []
    responses:
      200:
        description: Список дошок
    """
    user_id = get_jwt_identity()
    boards = Board.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': board.id,
        'title': board.title
    } for board in boards]), 200

@task_tracker_bp.route('/api/boards', methods=['POST'])
@jwt_required()
def api_create_board():
    """
    Створити нову дошку
    ---
    tags:
      - Трекер задач
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
    responses:
      201:
        description: Дошку створено
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    board = Board(
        title=data.get('title', ''),
        user_id=user_id
    )
    
    db.session.add(board)
    db.session.commit()
    
    return jsonify({'id': board.id}), 201

@task_tracker_bp.route('/api/boards/<id>', methods=['GET'])
@jwt_required()
def api_get_board(id):
    user_id = get_jwt_identity()
    board = Board.query.filter_by(id=id, user_id=user_id).first()
    
    if not board:
        return jsonify({'error': 'Дошку не знайдено'}), 404
    
    return jsonify({
        'id': board.id,
        'title': board.title
    }), 200

@task_tracker_bp.route('/api/boards/<id>', methods=['PUT'])
@jwt_required()
def api_update_board(id):
    user_id = get_jwt_identity()
    board = Board.query.filter_by(id=id, user_id=user_id).first()
    
    if not board:
        return jsonify({'error': 'Дошку не знайдено'}), 404
    
    data = request.get_json()
    board.title = data.get('title', board.title)
    
    db.session.commit()
    
    return jsonify({'message': 'Дошку оновлено'}), 200

@task_tracker_bp.route('/api/boards/<id>', methods=['DELETE'])
@jwt_required()
def api_delete_board(id):
    user_id = get_jwt_identity()
    board = Board.query.filter_by(id=id, user_id=user_id).first()
    
    if not board:
        return jsonify({'error': 'Дошку не знайдено'}), 404
    
    db.session.delete(board)
    db.session.commit()
    
    return jsonify({'message': 'Дошку видалено'}), 200

@task_tracker_bp.route('/api/boards/<board_id>/columns', methods=['GET'])
@jwt_required()
def api_list_columns(board_id):
    user_id = get_jwt_identity()
    board = Board.query.filter_by(id=board_id, user_id=user_id).first()
    
    if not board:
        return jsonify({'error': 'Дошку не знайдено'}), 404
    
    columns = Column.query.filter_by(board_id=board_id).order_by(Column.ordering).all()
    
    return jsonify([{
        'id': col.id,
        'title': col.title,
        'ordering': col.ordering,
        'tasks': [{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'doer': task.doer,
            'start_time': task.start_time.isoformat() if task.start_time else None,
            'end_time': task.end_time.isoformat() if task.end_time else None,
            'status': task.status,
            'priority': task.priority
        } for task in col.tasks]
    } for col in columns]), 200

@task_tracker_bp.route('/api/boards/<board_id>/columns', methods=['POST'])
@jwt_required()
def api_create_column(board_id):
    user_id = get_jwt_identity()
    board = Board.query.filter_by(id=board_id, user_id=user_id).first()
    
    if not board:
        return jsonify({'error': 'Дошку не знайдено'}), 404
    
    data = request.get_json()
    
    # Get max ordering.
    max_ordering = db.session.query(func.max(Column.ordering)).filter_by(board_id=board_id).scalar() or 0
    
    column = Column(
        board_id=board_id,
        title=data.get('title', ''),
        ordering=max_ordering + 1
    )
    
    db.session.add(column)
    db.session.commit()
    
    return jsonify({'id': column.id}), 201

@task_tracker_bp.route('/api/columns/<id>', methods=['PUT'])
@jwt_required()
def api_update_column(id):
    user_id = get_jwt_identity()
    column = Column.query.join(Board).filter(Column.id == id, Board.user_id == user_id).first()
    
    if not column:
        return jsonify({'error': 'Колонку не знайдено'}), 404
    
    data = request.get_json()
    column.title = data.get('title', column.title)
    
    if 'ordering' in data:
        column.ordering = data['ordering']
    
    db.session.commit()
    
    return jsonify({'message': 'Колонку оновлено'}), 200

@task_tracker_bp.route('/api/columns/<id>', methods=['DELETE'])
@jwt_required()
def api_delete_column(id):
    user_id = get_jwt_identity()
    column = Column.query.join(Board).filter(Column.id == id, Board.user_id == user_id).first()
    
    if not column:
        return jsonify({'error': 'Колонку не знайдено'}), 404
    
    db.session.delete(column)
    db.session.commit()
    
    return jsonify({'message': 'Колонку видалено'}), 200

@task_tracker_bp.route('/api/tasks', methods=['POST'])
@jwt_required()
def api_create_task():
    """
    Створити нову задачу
    ---
    tags:
      - Трекер задач
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - column_id
            - title
          properties:
            column_id:
              type: string
            title:
              type: string
            description:
              type: string
    responses:
      201:
        description: Задачу створено
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    column = Column.query.join(Board).filter(Column.id == data.get('column_id'), Board.user_id == user_id).first()
    
    if not column:
        return jsonify({'error': 'Колонку не знайдено'}), 404
    
    from datetime import datetime as dt
    
    task = Task(
        column_id=data.get('column_id'),
        title=data.get('title', ''),
        description=data.get('description'),
        doer=data.get('doer'),
        start_time=dt.fromisoformat(data['start_time']) if data.get('start_time') else None,
        end_time=dt.fromisoformat(data['end_time']) if data.get('end_time') else None,
        status=data.get('status'),
        priority=data.get('priority')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({'id': task.id}), 201

@task_tracker_bp.route('/api/tasks/<id>', methods=['GET'])
@jwt_required()
def api_get_task(id):
    user_id = get_jwt_identity()
    task = Task.query.join(Column).join(Board).filter(Task.id == id, Board.user_id == user_id).first()
    
    if not task:
        return jsonify({'error': 'Задачу не знайдено'}), 404
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'doer': task.doer,
        'start_time': task.start_time.isoformat() if task.start_time else None,
        'end_time': task.end_time.isoformat() if task.end_time else None,
        'status': task.status,
        'priority': task.priority,
        'column_id': task.column_id
    }), 200

@task_tracker_bp.route('/api/tasks/<id>', methods=['PUT'])
@jwt_required()
def api_update_task(id):
    """
    Оновити задачу, зокрема перемістити в іншу колонку
    ---
    tags:
      - Трекер задач
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            column_id:
              type: string
            title:
              type: string
    responses:
      200:
        description: Задачу оновлено
    """
    user_id = get_jwt_identity()
    task = Task.query.join(Column).join(Board).filter(Task.id == id, Board.user_id == user_id).first()
    
    if not task:
        return jsonify({'error': 'Задачу не знайдено'}), 404
    
    data = request.get_json()
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.doer = data.get('doer', task.doer)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    
    if 'column_id' in data:
        task.column_id = data['column_id']
    
    if 'start_time' in data:
        from datetime import datetime as dt
        task.start_time = dt.fromisoformat(data['start_time']) if data['start_time'] else None
    
    if 'end_time' in data:
        from datetime import datetime as dt
        task.end_time = dt.fromisoformat(data['end_time']) if data['end_time'] else None
    
    db.session.commit()
    
    return jsonify({'message': 'Задачу оновлено'}), 200

@task_tracker_bp.route('/api/tasks/<id>', methods=['DELETE'])
@jwt_required()
def api_delete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.join(Column).join(Board).filter(Task.id == id, Board.user_id == user_id).first()
    
    if not task:
        return jsonify({'error': 'Задачу не знайдено'}), 404
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Задачу видалено'}), 200
