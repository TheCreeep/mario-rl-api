from flask import Blueprint, jsonify, request

import psycopg2 as pg
from functions.connect_db import connect_db

settings_bp = Blueprint('settings_bp', __name__)


@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():

    if request.method == 'POST':

        request_data = request.get_json()

        try:
            con = connect_db()
            cur = con.cursor()

            models_path = request_data['modelsPath']
            log_path = request_data['logPath']
            save_model_frequency = request_data['saveModelFrequency']
            nb_env = request_data['nbEnv']

            cur.execute("DELETE FROM settings")

            sql = f"INSERT INTO settings(models_path, log_path, save_model_freq, nb_env) VALUES('{models_path}', '{log_path}', {save_model_frequency}, {nb_env})"

            cur.execute(sql)

            con.commit()

            cur.close()
            con.close()

            return {'code': 200, 'message': "Les paramètres ont bien été modifiés"}

        except pg.Error as e:
            return jsonify({"code": 500, "message": str(e)})
    else:
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("SELECT * FROM settings")
            row = cur.fetchone()

            if row is None:
                return jsonify({'code': 200,
                                'settings': {
                                    'modelsPath': '',
                                    'logPath': '',
                                    'saveModelFrequency': 0,
                                    'nbEnv': 0
                                }})

            models_path = row[0]
            log_path = row[1]
            save_model_frequency = row[2]
            nb_env = row[3]

            return jsonify({'code': 200,
                            'settings': {
                                'modelsPath': models_path,
                                'logPath': log_path,
                                'saveModelFrequency': save_model_frequency,
                                'nbEnv': nb_env
                            }})

        except pg.Error as e:
            return jsonify({"code": 500, "error": str(e)})
