from flask import Blueprint, jsonify, request
import psycopg2 as pg
from functions.connect_db import connect_db

models_bp = Blueprint('models_bp', __name__)

@models_bp.route('/models', methods=['GET', 'DELETE'])
def models():
    if request.method == 'GET':
        try:
            con = connect_db()
            cur = con.cursor()
            
            cur.execute("SELECT * FROM models LIMIT 563")

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
    elif request.method == 'DELETE':
        model_id = request.args.get('delete_model_id')
        
        try:
            con = connect_db()
            cur = con.cursor()
            
            sql = f"DELETE FROM models WHERE model_id = {model_id}"
            
            cur.execute(sql)
            
            con.commit()

            cur.close()
            con.close()

            return {'code': 200, 'message': "Le modèle a bien été supprimé"}

        except pg.Error as e:
            print(e)
            return jsonify({"error": str(e)})
