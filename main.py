# On importe tout le nécessaire pour faire tourner notre modèle
from stable_baselines3 import PPO
import time
from functions.env import env
from functions.render_decorator import render_browser, app

import warnings
warnings.filterwarnings("ignore")

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

@app.route('/api')
def api():
    return {'hello': 'world'}
