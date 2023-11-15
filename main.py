# On importe tout le nécessaire pour faire tourner notre modèle
from stable_baselines3 import PPO
from functions.env import env
from functions.frame_gen import frame_gen
from flask import Flask, Response, request
from flask_cors import CORS
import os
from routes.api import api_bp
from routes.models import models_bp
from routes.settings import settings_bp
from functions.get_settings import get_settings

from warnings import filterwarnings
filterwarnings('ignore')

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_bp, url_prefix='/')
app.register_blueprint(models_bp, url_prefix='/api')
app.register_blueprint(settings_bp, url_prefix='/api')


def render_browser(env_func):
    def wrapper(*args, **kwargs):
        @app.route('/render_feed')
        def render_feed():
            query = request.args.to_dict()
            
            if 'model' not in query:
                return Response("No model selected", mimetype='text/html')
            
            global selected_model
            selected_model = query['model']
            return Response(frame_gen(env_func, *args, **kwargs), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        app.run(host='0.0.0.0', port='5000', debug=False, use_reloader=True)

    return wrapper


settings = get_settings()
models_path = settings[0]

@render_browser
def test_policy():
    model = None
    if selected_model is not None:
        chemin_complet = os.path.join(models_path, selected_model)
        print(os.path.exists(chemin_complet))

    if chemin_complet:
        model = PPO.load(f"D:/MarioRL/train/{selected_model}")
        print("Starting the game with model : ", selected_model)
        model_exists = True
    else:
        print("No model found, playing random inputs")
        model_exists = False
        
    
    """ model_exists = True
    selected_model = "model_step_110000"
    model = PPO.load(f"D:/MarioRL/train/{selected_model}") """
        
    
    state = env.reset()
    done = False
    while done == False:
        if model is None:
            action = [env.action_space.sample()]
        else:
            action, _ = model.predict(state)
        state, reward, done, info = env.step(action)
        yield env.render(mode='rgb_array'), reward, done, info, action, model_exists
        
test_policy()