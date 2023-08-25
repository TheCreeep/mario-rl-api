# On importe tout le nécessaire pour faire tourner notre modèle
import gym_super_mario_bros
from gym.wrappers import GrayScaleObservation
from gym_super_mario_bros.actions import COMPLEX_MOVEMENT, SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from stable_baselines3 import PPO
import time
from main import render_browser

import warnings
warnings.filterwarnings("ignore")

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


# Loop through the game
@render_browser
def test_policy():
    # Start the game
    state = env.reset()
    print(state)
    while True:
        action, _ = model.predict(state)
        state, reward, done, info = env.step(action)
        yield env.render(mode='rgb_array')
        