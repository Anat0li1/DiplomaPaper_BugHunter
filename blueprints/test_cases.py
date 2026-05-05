from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, TestCase, TestStep, User
from sqlalchemy import or_, func

test_cases_bp = Blueprint('test_cases', __name__)

@test_cases_bp.route('/test-cases')
def list_test_cases():
    return render_template('test_cases/list.html')

@test_cases_bp.route('/test-cases/new')
def new_test_case():
    return render_template('test_cases/form.html')

@test_cases_bp.route('/test-cases/edit/<id>')
def edit_test_case(id):
    return render_template('test_cases/form.html', test_case_id=id)

@test_cases_bp.route('/test-cases/view/<id>')
def view_test_case(id):
    return render_template('test_cases/view.html', test_case_id=id)

# API endpoints
@test_cases_bp.route('/api/test-cases', methods=['GET'])
@jwt_required()
def api_list_test_cases():
    """
    Get list of test cases
    ---
    tags:
      - Test Cases
    security:
      - Bearer: []
    responses:
      200:
        description: List of test cases
    """
    user_id = get_jwt_identity()
    test_cases = TestCase.query.filter(
        or_(TestCase.is_system == True, TestCase.user_id == user_id)
    ).order_by(TestCase.given_id).all()
    
    return jsonify([{
        'id': tc.id,
        'given_id': str(tc.given_id) if tc.given_id else None,
        'title': tc.title,
        'priority': tc.priority,
        'application_group': tc.application_group,
        'version': tc.version
    } for tc in test_cases]), 200

@test_cases_bp.route('/api/test-cases/<id>', methods=['GET'])
@jwt_required()
def api_get_test_case(id):
    """
    Get test case by ID
    ---
    tags:
      - Test Cases
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: string
        required: true
    responses:
      200:
        description: Test case details
      404:
        description: Test case not found
    """
    user_id = get_jwt_identity()
    test_case = TestCase.query.filter_by(id=id).first()
    
    if not test_case:
        return jsonify({'error': 'Test case not found'}), 404
    
    if not test_case.is_system and test_case.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({
        'id': test_case.id,
        'given_id': str(test_case.given_id) if test_case.given_id else None,
        'application_group': test_case.application_group,
        'title': test_case.title,
        'description': test_case.description,
        'priority': test_case.priority,
        'is_system': test_case.is_system,
        'preconditions': test_case.preconditions,
        'postconditions': test_case.postconditions,
        'version': test_case.version,
        'environment': test_case.environment,
        'comments': test_case.comments,
        'steps': [{
            'id': step.id,
            'number': step.number,
            'step_name': step.step_name,
            'test_data': step.test_data,
            'expected_result': step.expected_result
        } for step in test_case.steps]
    }), 200

@test_cases_bp.route('/api/test-cases', methods=['POST'])
@jwt_required()
def api_create_test_case():
    """
    Create a new test case
    ---
    tags:
      - Test Cases
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
            given_id:
              type: string
            title:
              type: string
            description:
              type: string
            priority:
              type: integer
            steps:
              type: array
    responses:
      201:
        description: Test case created
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get next given_id if not provided
    given_id = data.get('given_id')
    if not given_id:
        # Auto-generate numeric ID
        try:
            # Get all numeric given_ids and find max
            all_cases = TestCase.query.filter(TestCase.given_id.isnot(None)).all()
            numeric_ids = []
            for tc in all_cases:
                try:
                    numeric_ids.append(int(tc.given_id))
                except (ValueError, TypeError):
                    pass
            if numeric_ids:
                given_id = str(max(numeric_ids) + 1)
            else:
                given_id = "1"
        except:
            given_id = "1"
    
    test_case = TestCase(
        given_id=given_id,
        application_group=data.get('application_group'),
        title=data.get('title', ''),
        description=data.get('description'),
        priority=data.get('priority', 2),
        is_system=data.get('is_system', False),
        preconditions=data.get('preconditions'),
        postconditions=data.get('postconditions'),
        version=data.get('version'),
        environment=data.get('environment'),
        user_id=user_id,
        comments=data.get('comments')
    )
    
    db.session.add(test_case)
    db.session.flush()
    
    # Add steps
    for step_data in data.get('steps', []):
        step = TestStep(
            test_case_id=test_case.id,
            number=step_data['number'],
            step_name=step_data['step_name'],
            test_data=step_data.get('test_data'),
            expected_result=step_data.get('expected_result')
        )
        db.session.add(step)
    
    db.session.commit()
    
    return jsonify({'id': test_case.id, 'given_id': test_case.given_id}), 201

@test_cases_bp.route('/api/test-cases/<id>', methods=['PUT'])
@jwt_required()
def api_update_test_case(id):
    """
    Update test case
    ---
    tags:
      - Test Cases
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
    responses:
      200:
        description: Test case updated
    """
    user_id = get_jwt_identity()
    test_case = TestCase.query.filter_by(id=id).first()
    
    if not test_case:
        return jsonify({'error': 'Test case not found'}), 404
    
    if not test_case.is_system and test_case.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    if 'given_id' in data:
        test_case.given_id = data.get('given_id') or test_case.given_id
    test_case.application_group = data.get('application_group', test_case.application_group)
    test_case.title = data.get('title', test_case.title)
    test_case.description = data.get('description', test_case.description)
    test_case.priority = data.get('priority', test_case.priority)
    test_case.preconditions = data.get('preconditions', test_case.preconditions)
    test_case.postconditions = data.get('postconditions', test_case.postconditions)
    test_case.version = data.get('version', test_case.version)
    test_case.environment = data.get('environment', test_case.environment)
    test_case.comments = data.get('comments', test_case.comments)
    
    # Delete old steps and add new ones
    TestStep.query.filter_by(test_case_id=test_case.id).delete()
    for step_data in data.get('steps', []):
        step = TestStep(
            test_case_id=test_case.id,
            number=step_data['number'],
            step_name=step_data['step_name'],
            test_data=step_data.get('test_data'),
            expected_result=step_data.get('expected_result')
        )
        db.session.add(step)
    
    db.session.commit()
    
    return jsonify({'message': 'Test case updated'}), 200

@test_cases_bp.route('/api/test-cases/<id>', methods=['DELETE'])
@jwt_required()
def api_delete_test_case(id):
    """
    Delete test case
    ---
    tags:
      - Test Cases
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: string
        required: true
    responses:
      200:
        description: Test case deleted
    """
    user_id = get_jwt_identity()
    test_case = TestCase.query.filter_by(id=id).first()
    
    if not test_case:
        return jsonify({'error': 'Test case not found'}), 404
    
    if not test_case.is_system and test_case.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(test_case)
    db.session.commit()
    
    return jsonify({'message': 'Test case deleted'}), 200

