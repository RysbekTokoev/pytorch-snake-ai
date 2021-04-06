import torch
import random
import numpy as np
from collections import deque
from game import Game
from model import Net, Trainer
import sys
import matplotlib.pyplot as plt

plt.ion()
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self, load_path=''):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.load_path = load_path
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Net(11, 256, 3)

        if load_path:
            self.model.load_state_dict(torch.load(load_path))
        self.trainer = Trainer(self.model, LR, self.gamma)

    def get_state(self, game):
        # 0          1         2        3
        # U          L         R        D
        # [[1, -10], [0, -10], [0, 10], [1, 10]]
        head = game.snake_pos
        near_head = [
            [head[0], head[1] - 10],
            [head[0] - 10, head[1]],
            [head[0] + 10, head[1]],
            [head[0], head[1] + 10],
        ]

        directions = [
            game.direction == 0,
            game.direction == 1,
            game.direction == 2,
            game.direction == 3,
        ]

        state = [
            (directions[0] and game.is_colision(near_head[0])) or
            (directions[1] and game.is_colision(near_head[1])) or
            (directions[2] and game.is_colision(near_head[2])) or
            (directions[3] and game.is_colision(near_head[3])),

            (directions[0] and game.is_colision(near_head[1])) or
            (directions[1] and game.is_colision(near_head[3])) or
            (directions[2] and game.is_colision(near_head[0])) or
            (directions[3] and game.is_colision(near_head[2])),

            (directions[0] and game.is_colision(near_head[2])) or
            (directions[1] and game.is_colision(near_head[0])) or
            (directions[2] and game.is_colision(near_head[3])) or
            (directions[3] and game.is_colision(near_head[1])),

            game.food_pos[0] < head[0],
            game.food_pos[0] > head[0],
            game.food_pos[1] < head[1],
            game.food_pos[1] > head[1],
        ] + directions
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)


    def get_action(self, state):
        if not self.load_path:
            self.epsilon = 80 - self.n_games

        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train(model_path=''):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent(model_path)
    game = Game()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)

        reward, done, score = game.play(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            if agent.n_games % 10 == 0:
                print("Game:", agent.n_games, "Score:", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


def plot(scores, mean_scores):
    plt.clf()
    plt.gcf()
    plt.xlabel("Iteration")
    plt.ylabel("Score")
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))

if __name__ == "__main__":
    model_path = ''
    if len(sys.argv) > 1:
        print(sys.argv[1])
        model_path = sys.argv[1]
    train(model_path)
