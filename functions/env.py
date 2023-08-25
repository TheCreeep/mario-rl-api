import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym.wrappers import GrayScaleObservation
from gym_super_mario_bros.actions import COMPLEX_MOVEMENT, SIMPLE_MOVEMENT
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack

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
