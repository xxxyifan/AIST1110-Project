import gym
from gym import spaces
import numpy as np
from gym_game.envs.game_v0 import Gym_Game
import pygame

class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = Gym_Game()
        self.action_space = spaces.Discrete(120)
        self.observation_space = spaces.Box(np.zeros((4,)), np.full((4,), 9), dtype=np.int0)

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
        return obs[0], reward, done, False, {}

    def render(self):
        self.pygame.end()

    def close(self):
        pygame.display.quit()
        pygame.quit()
    