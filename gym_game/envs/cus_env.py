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
        self.observation_space = spaces.Box(np.zeros((2,)), np.full((2,), 10), dtype=np.int0)
        # self.observation_space = spaces.Box(np.zeros((10,)), np.full((10,), 10), dtype=np.float64)

    def reset(self):
        del self.pygame
        self.pygame = Gym_Game()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        # print("action start, action = ", action)
        self.pygame.action(action)
        # print("action finish, observe start")
        obs = self.pygame.observe()
        # print("observe finish, evaluate start")
        reward = self.pygame.evaluate()
        # print("evaluate finish, is_done start, reward = ", reward)
        done = self.pygame.is_done()
        # print("is_done finish, return to main")
        return obs[0], reward, done, False, {}

    def render(self, close=False):
        self.pygame.view()

    def close(self):
        pygame.display.quit()
        pygame.quit()