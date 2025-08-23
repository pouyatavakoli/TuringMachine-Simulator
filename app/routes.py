from flask import Blueprint,render_template, jsonify, request
main_bp = Blueprint('routes', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# api endpoint routes:

@main_bp.route('/api/init', methods=['POST'])
def initialize_machine():
    # TODO: implementation
    return jsonify({"status": "initialized"})
