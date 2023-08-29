from flask import Blueprint, jsonify
import psycopg2 as pg
from functions.connect_db import connect_db

models_bp = Blueprint('models_bp', __name__)

@models_bp.route('/models', methods=['GET'])
def models():
    try:
        con = connect_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM models LIMIT 66")

        rows = cur.fetchall()
        
        result = []
        
        for row in rows:
            result.append({
                "id": row[0],
                "name": row[1],
                "date": row[2],
                "epoch": row[3],
                "lr": row[4]
            })
        
        cur.close()
        con.close()

        return jsonify(result)
    
    except pg.Error as e:
        return jsonify({"error": str(e)})
