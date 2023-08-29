# On importe tout le nécessaire pour faire tourner notre modèle
from stable_baselines3 import PPO
from functions.env import env
from functions.frame_gen import frame_gen
from flask import Flask, Response
import os
from routes.api import api_bp
from routes.models import models_bp


from warnings import filterwarnings
filterwarnings('ignore')

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_PATH)
app.register_blueprint(api_bp, url_prefix='/')
app.register_blueprint(models_bp, url_prefix='/api')

def render_browser(env_func):
    def wrapper(*args, **kwargs):
        @app.route('/render_feed')
        def render_feed():
            return Response(frame_gen(env_func, *args, **kwargs), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        app.run(host='0.0.0.0', port='5000', debug=False)

    return wrapper

best_model_steps = 6_650_000

# On commence par charger le dernier modèle
model = PPO.load(f"D:/MarioRL/train/best_model_{best_model_steps}")

@render_browser
def test_policy():
    # Start the game
    state = env.reset()
    while True:
        action, _ = model.predict(state)
        state, reward, done, info = env.step(action)
        yield env.render(mode='rgb_array'), reward, done, info
        
test_policy()

