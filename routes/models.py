from flask import Blueprint

models_bp = Blueprint('models_bp', __name__)

@models_bp.route('/models', methods=['GET'])
def models():
    return "Les modeles"