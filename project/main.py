import sys
import numpy as np
import math
import random
import pygame

import gym
import gym_game

from cmdargs import args

def simulate(GAME_MODE):
    global epsilon, epsilon_decay
    for episode in range(MAX_EPISODES):

        # Init environment
        state = env.reset()
        state = tuple(state[0])
        total_reward = 0

        # if GAME_MODE == "human":
        #     # change_value = 0
        #     # action = -1
        #     # while action < 0:
        #     #     env.render()
        #     #     #move the pointer
        #     #     degree = 90
        #     #     degree += change_value
        #     #     if degree > 150:
        #     #         degree = 150
        #     #     if degree < 30:
        #     #         degree = 30
        #     #     for event in pygame.event.get():
        #     #         if event.type == pygame.KEYDOWN:
        #     #             #change the angle 
        #     #             if event.key == ord("a"):
        #     #                 is_degree_change = True
        #     #                 change_value = 2
        #     #             if event.key == ord("d"):
        #     #                 is_degree_change = True
        #     #                 change_value = -2
        #     #             #shoot
        #     #             if event.key == ord("w"):
        #     #                 action = degree - 30
        #     #                 break

        #         # if event.type == QUIT:
        #         #     pass
        #     pass
        # else:
        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):

            # In the beginning, do random action to learn
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state])

            if action >= 120:
                action = 119
            # Do action and get result
            next_state, reward, done, _ , a = env.step(action)
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table[tuple(state)][action]
            best_q = np.max(q_table[tuple(next_state)])

            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            q_table[tuple(state)][action] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

            # Set up for the next iteration
            state = next_state

            # Draw games
            if GAME_MODE == "ai":
                # print("Non-CLI")
                env.render()

            # When episode is done, print reward
            if done or t >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                break

        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay
    env.close()


if __name__ == "__main__":
    env = gym.make("pygame-v0")
    MAX_EPISODES = args.episodes
    MAX_TRY = 1000
    GAME_MODE = args.mode
    epsilon = 1
    epsilon_decay = 0.999
    learning_rate = 0.1
    gamma = 0.6
    num_box = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
    print(num_box)
    print(num_box + (env.action_space.n,))
    q_table = np.zeros(num_box + (env.action_space.n,))
    if GAME_MODE == "human":
        exec(open("game.py").read())
    else:
        simulate(GAME_MODE)
    # simulate(GAME_MODE)