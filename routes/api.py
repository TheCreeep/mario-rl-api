from flask import Blueprint

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/api')
def api():
    return "Bienvenue sur l'API de MarioRL !"
