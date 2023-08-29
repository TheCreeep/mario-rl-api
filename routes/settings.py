from flask import Blueprint, jsonify

import psycopg2 as pg
from functions.connect_db import connect_db

settings_bp = Blueprint('settings_bp', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if settings_bp.request.method == 'POST':
        return "POST"
    else:
      try:
          con = connect_db()
          cur = con.cursor()
          
      except pg.Error as e:
          return jsonify({"error": str(e)})