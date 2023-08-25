import os
import cv2
from flask import Flask, render_template, Response

# On importe tout le nécessaire pour faire tourner notre modèle
import gym_super_mario_bros
from gym.wrappers import GrayScaleObservation
from gym_super_mario_bros.actions import COMPLEX_MOVEMENT, SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from stable_baselines3 import PPO
import time

import warnings
warnings.filterwarnings("ignore")

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_PATH)

best_model_steps = 6_650_000

# On commence par charger le dernier modèle
model = PPO.load(f"D:/MarioRL/train/best_model_{best_model_steps}")

# Reprenons avec un nouvel environnement
env = gym_super_mario_bros.make("SuperMarioBros-v0")
# On lui applique les controles
env = JoypadSpace(env, SIMPLE_MOVEMENT)
# On lui applique le wrapper GrayScale
env = GrayScaleObservation(env, keep_dim=True)
# On Wrap notre environnement dans un Dummy Environnement
env = DummyVecEnv([lambda: env])
# Et enfin on ajoute le Wrapper pour nous permettre de retenir les 4 dernieres frames
env = VecFrameStack(env, n_stack=4, channels_order="last")

def frame_gen(env_func, *args, **kwargs):
    get_frame = env_func(*args, **kwargs)
    while True:
        frame = next(get_frame, None)
        if frame is None:
            break
        imageRGB = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #ADDED TO CONVERT FROM BGR TO RGB
        _, frame = cv2.imencode('.png', imageRGB)
        frame = frame.tobytes()
        yield (b'--frame\r\n' + b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

def render_browser(env_func):
    def wrapper(*args, **kwargs):
        @app.route('/render_feed')
        def render_feed():
            return Response(frame_gen(env_func, *args, **kwargs), mimetype='multipart/x-mixed-replace; boundary=frame')

        print("Starting rendering, check `server_ip:5000`.")
        app.run(host='0.0.0.0', port='5000', debug=False)

    return wrapper

@app.route('/render_mario')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    return {'hello': 'world'}


@render_browser
def test_policy():
    # Start the game
    state = env.reset()
    print(state)
    while True:
        action, _ = model.predict(state)
        state, reward, done, info = env.step(action)
        yield env.render(mode='rgb_array')
        
test_policy()
