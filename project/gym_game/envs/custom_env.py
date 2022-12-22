import gym
from gym import spaces
import numpy as np
from Gym_game import Gym_Game

class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = Gym_Game()
        self.action_space = spaces.Discrete(120, start=30)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0]), np.array([10, 10, 10, 10, 10]), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = Gym_Game()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view()
        
    def close(self):
        pass
