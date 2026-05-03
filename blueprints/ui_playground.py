from flask import Blueprint, render_template

ui_playground_bp = Blueprint('ui_playground', __name__)

@ui_playground_bp.route('/ui-playground')
def ui_playground():
    return render_template('ui_playground/index.html')

