from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, BugReport, BugStep, TestCase
from sqlalchemy import or_, func

bug_reports_bp = Blueprint('bug_reports', __name__)

@bug_reports_bp.route('/bug-reports')
def list_bug_reports():
    return render_template('bug_reports/list.html')

@bug_reports_bp.route('/bug-reports/new')
def new_bug_report():
    return render_template('bug_reports/form.html')

@bug_reports_bp.route('/bug-reports/edit/<id>')
def edit_bug_report(id):
    return render_template('bug_reports/form.html', bug_report_id=id)

@bug_reports_bp.route('/bug-reports/view/<id>')
def view_bug_report(id):
    return render_template('bug_reports/view.html', bug_report_id=id)

# API endpoints
@bug_reports_bp.route('/api/bug-reports', methods=['GET'])
@jwt_required()
def api_list_bug_reports():
    """
    Get list of bug reports
    ---
    tags:
      - Bug Reports
    security:
      - Bearer: []
    responses:
      200:
        description: List of bug reports
    """
    user_id = get_jwt_identity()
    bug_reports = BugReport.query.filter(
        or_(BugReport.is_system == True, BugReport.user_id == user_id)
    ).order_by(BugReport.given_id).all()
    
    return jsonify([{
        'id': br.id,
        'given_id': br.given_id,
        'title': br.title,
        'severity': br.severity,
        'priority': br.priority,
        'status': br.status
    } for br in bug_reports]), 200

@bug_reports_bp.route('/api/bug-reports/<id>', methods=['GET'])
@jwt_required()
def api_get_bug_report(id):
    """
    Get bug report by ID
    ---
    tags:
      - Bug Reports
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: string
        required: true
    responses:
      200:
        description: Bug report details
      404:
        description: Bug report not found
    """
    user_id = get_jwt_identity()
    bug_report = BugReport.query.filter_by(id=id).first()
    
    if not bug_report:
        return jsonify({'error': 'Bug report not found'}), 404
    
    if not bug_report.is_system and bug_report.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({
        'id': bug_report.id,
        'given_id': bug_report.given_id,
        'title': bug_report.title,
        'description': bug_report.description,
        'preconditions': bug_report.preconditions,
        'postconditions': bug_report.postconditions,
        'actual_result': bug_report.actual_result,
        'expected_result': bug_report.expected_result,
        'severity': bug_report.severity,
        'priority': bug_report.priority,
        'status': bug_report.status,
        'system_and_browser_inf': bug_report.system_and_browser_inf,
        'version': bug_report.version,
        'environment': bug_report.environment,
        'test_case_id': bug_report.test_case_id,
        'comments': bug_report.comments,
        'steps': [{
            'id': step.id,
            'number': step.number,
            'step_name': step.step_name
        } for step in bug_report.steps]
    }), 200

@bug_reports_bp.route('/api/bug-reports', methods=['POST'])
@jwt_required()
def api_create_bug_report():
    """
    Create a new bug report
    ---
    tags:
      - Bug Reports
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
            severity:
              type: string
            priority:
              type: string
            test_case_given_id:
              type: string
    responses:
      201:
        description: Bug report created
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get next given_id
    max_id = db.session.query(func.max(BugReport.given_id)).scalar() or 0
    given_id = max_id + 1
    
    # Find test case by given_id if provided
    test_case_id = None
    test_case_given_id = data.get('test_case_given_id')
    if test_case_given_id:
        test_case = TestCase.query.filter_by(given_id=test_case_given_id).first()
        if test_case:
            test_case_id = test_case.id
    
    bug_report = BugReport(
        given_id=given_id,
        title=data.get('title', ''),
        description=data.get('description'),
        preconditions=data.get('preconditions'),
        postconditions=data.get('postconditions'),
        actual_result=data.get('actual_result'),
        expected_result=data.get('expected_result'),
        severity=data.get('severity', 'Medium'),
        priority=data.get('priority', 'Medium'),
        status=data.get('status', 'New'),
        system_and_browser_inf=data.get('system_and_browser_inf'),
        version=data.get('version'),
        environment=data.get('environment'),
        user_id=user_id,
        test_case_id=test_case_id or data.get('test_case_id'),
        is_system=data.get('is_system', False),
        comments=data.get('comments')
    )
    
    db.session.add(bug_report)
    db.session.flush()
    
    # Add steps
    for step_data in data.get('steps', []):
        step = BugStep(
            bug_report_id=bug_report.id,
            number=step_data['number'],
            step_name=step_data['step_name']
        )
        db.session.add(step)
    
    db.session.commit()
    
    return jsonify({'id': bug_report.id, 'given_id': bug_report.given_id}), 201

@bug_reports_bp.route('/api/bug-reports/<id>', methods=['PUT'])
@jwt_required()
def api_update_bug_report(id):
    """
    Update bug report
    ---
    tags:
      - Bug Reports
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
        description: Bug report updated
    """
    user_id = get_jwt_identity()
    bug_report = BugReport.query.filter_by(id=id).first()
    
    if not bug_report:
        return jsonify({'error': 'Bug report not found'}), 404
    
    if not bug_report.is_system and bug_report.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    bug_report.title = data.get('title', bug_report.title)
    bug_report.description = data.get('description', bug_report.description)
    bug_report.preconditions = data.get('preconditions', bug_report.preconditions)
    bug_report.postconditions = data.get('postconditions', bug_report.postconditions)
    bug_report.actual_result = data.get('actual_result', bug_report.actual_result)
    bug_report.expected_result = data.get('expected_result', bug_report.expected_result)
    bug_report.severity = data.get('severity', bug_report.severity)
    bug_report.priority = data.get('priority', bug_report.priority)
    bug_report.status = data.get('status', bug_report.status)
    bug_report.system_and_browser_inf = data.get('system_and_browser_inf', bug_report.system_and_browser_inf)
    bug_report.version = data.get('version', bug_report.version)
    bug_report.environment = data.get('environment', bug_report.environment)
    
    # Handle test_case_given_id
    test_case_given_id = data.get('test_case_given_id')
    if test_case_given_id:
        test_case = TestCase.query.filter_by(given_id=test_case_given_id).first()
        if test_case:
            bug_report.test_case_id = test_case.id
    elif 'test_case_id' in data:
        bug_report.test_case_id = data.get('test_case_id', bug_report.test_case_id)
    
    bug_report.comments = data.get('comments', bug_report.comments)
    
    # Delete old steps and add new ones
    BugStep.query.filter_by(bug_report_id=bug_report.id).delete()
    for step_data in data.get('steps', []):
        step = BugStep(
            bug_report_id=bug_report.id,
            number=step_data['number'],
            step_name=step_data['step_name']
        )
        db.session.add(step)
    
    db.session.commit()
    
    return jsonify({'message': 'Bug report updated'}), 200

@bug_reports_bp.route('/api/bug-reports/<id>', methods=['DELETE'])
@jwt_required()
def api_delete_bug_report(id):
    """
    Delete bug report
    ---
    tags:
      - Bug Reports
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: string
        required: true
    responses:
      200:
        description: Bug report deleted
    """
    user_id = get_jwt_identity()
    bug_report = BugReport.query.filter_by(id=id).first()
    
    if not bug_report:
        return jsonify({'error': 'Bug report not found'}), 404
    
    if not bug_report.is_system and bug_report.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(bug_report)
    db.session.commit()
    
    return jsonify({'message': 'Bug report deleted'}), 200

