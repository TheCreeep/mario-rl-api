import datetime
from flask import Blueprint, jsonify, request
import gym_super_mario_bros
import psycopg2 as pg
from stable_baselines3 import PPO
from functions.connect_db import connect_db
from functions.get_settings import get_settings
from nes_py.wrappers import JoypadSpace
from gym.wrappers import GrayScaleObservation
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

models_bp = Blueprint('models_bp', __name__)
settings = get_settings()


@models_bp.route('/models', methods=['GET', 'DELETE', 'POST'])
def models():
    if request.method == 'GET':
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("SELECT * FROM models")

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
            return jsonify({"error": str(e)})

    elif request.method == 'POST':
        env = gym_super_mario_bros.make("SuperMarioBros-v0")
        env = JoypadSpace(env, SIMPLE_MOVEMENT)
        env = GrayScaleObservation(env, keep_dim=True)
        env = DummyVecEnv([lambda: env])
        env = VecFrameStack(env, n_stack=4, channels_order="last")

        model_params = request.get_json()
        epochs = model_params['nEpochs']
        steps = model_params['nSteps']
        learning_rate = model_params['learningRate']
        batch_size = model_params['batchSize']
        clip_range = model_params['clipRange']
        seed = model_params['seed']

        model_name = f"mario-v0-e{epochs}-l{learning_rate}-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}"

        # Create a new PPO model
        model = PPO('CnnPolicy', env, verbose=1,
                    batch_size=batch_size,
                    clip_range=clip_range,
                    tensorboard_log=f"{settings[1]}/{model_name}",
                    learning_rate=learning_rate,
                    n_steps=steps,
                    seed=seed)

        # Train the model
        model.learn(total_timesteps=epochs)

        # Save the model in the models folder
        model.save(f"{settings[0]}/{model_name}")

        # Save the trained model in the database
        try:
            con = connect_db()
            cur = con.cursor()

            sql = f"INSERT INTO models (model_name, creation_date, model_steps, learning_rate, max_fit) VALUES ('{model_name}', '{datetime.datetime.now()}', {epochs}, {learning_rate}, {10})"

            cur.execute(sql)

            con.commit()
            cur.close()
            con.close()
            return {'code': 200, 'message': "Le modèle a bien été créé et sauvegardé"}

        except pg.Error as e:
            return jsonify({'code': 500, "error": str(e)})
