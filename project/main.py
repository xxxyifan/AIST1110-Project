import sys
import numpy as np
import math
import random
import pygame
import time
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
        
        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):

            # In the beginning, do random action to learn
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state[0]*10+state[1]])

            if action >= 120:
                action = 119
            # Do action and get result
            next_state, reward, done, _ , a = env.step(action)
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table[state[0]*10+state[1]][action]
            best_q = np.max(q_table[next_state[0]*10+state[1]])

            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            q_table[state[0]*10+state[1]][action] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

            # Set up for the next iteration
            state = next_state

            # Draw games
            # if GAME_MODE == "ai":
            #     print("Non-CLI")
            #     env.render()

            # When episode is done, print reward
            if done or t >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                with open("result.txt", "a") as f:
                    f.write(f"Episode {episode},step {t},reward {total_reward},epsilon {epsilon}")
                    f.write("\n")
                break

        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay
    
    # Save Q-Table to Text File
    np.savetxt("q_table.csv", q_table, delimiter=" ")

    env.close()

def Ai_play(q_table, FPS):

    def bgm():
        pygame.mixer.init()
        # pygame.mixer.set_num_channels(2)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("files/bgm/12 final battle.ogg"))

    game_state = 1 # 0 = end , 1 = start
    clock = pygame.time.Clock()
    state = env.reset()
    state = tuple(state[0])

    start_time = time.time()
    bgm()

    while True:
        clock.tick(FPS)
        end_music = time.time()

        if end_music - start_time > 290:
            bgm()
        start_time = time.time()

        if game_state == 1:
            action = np.argmax(q_table[state[0]*10+state[1]])
            next_state, reward, done, _ , a = env.step(action)
            state = next_state
            if done:
                game_state = 0
        else:
            env.render()

def Ran_player(FPS):

    def bgm():
        pygame.mixer.init()
        # pygame.mixer.set_num_channels(2)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("files/bgm/12 final battle.ogg"))
        
    game_state = 1 # 0 = end , 1 = start
    clock = pygame.time.Clock()
    state = env.reset()
    state = tuple(state[0])

    start_time = time.time()
    bgm()

    while True:
        clock.tick(FPS)
        end_music = time.time()

        if end_music - start_time > 290:
            bgm()
        start_time = time.time()

        if game_state == 1:
            action = random.randint(0, 120)
            next_state, reward, done, _ , a = env.step(action)
            state = next_state
            if done:
                game_state = 0
        else:
            env.render()

if __name__ == "__main__":
    env = gym.make("pygame-v0")
    MAX_EPISODES = args.episodes
    MAX_TRY = 1000
    GAME_MODE = args.mode
    FPS = args.fps
    epsilon = 1
    epsilon_decay = 0.999
    learning_rate = 0.1
    gamma = 0.45
    num_box = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
    q_table = np.zeros((num_box[0]*num_box[1], env.action_space.n))
    # Import Q_table
    if args.file is not None:
        q_table = np.loadtxt(open(args.file), delimiter=" ")
        GAME_MODE = "ai-play"
    if GAME_MODE == "human":
        exec(open("game.py").read())
    elif GAME_MODE == "ai-play":
        Ai_play(q_table, FPS)
    elif GAME_MODE == "ran-player":
        Ran_player(FPS)
    else:
        simulate(GAME_MODE)
    # simulate(GAME_MODE)