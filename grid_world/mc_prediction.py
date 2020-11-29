import argparse
from tqdm import tqdm

from env import GridWorld
from agent import Agent


parser = argparse.ArgumentParser(description='GraidWorld MC')
parser.add_argument('--num_episode', type=int,
                    default=50000,
                    help='The number of episodes in MC')
args = parser.parse_args()


def main():
    env = GridWorld()
    agent = Agent()
    # table initialization
    data = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    gamma = 1.0
    alpha = 0.0001

    for k in tqdm(range(args.num_episode), desc='sampling episodes'):
        done = False
        history = []
        while not done:
            action = agent.select_action()
            (x, y), reward, done = env.step(action)
            history.append((x, y, reward))
        env.reset()

        #table update
        cum_reward = 0
        for transition in history[::-1]:
            x, y, reward = transition
            data[x][y] = data[x][y] + alpha * (cum_reward - data[x][y])
            cum_reward += gamma * reward

    for row in data:
        print(row)


if __name__ == '__main__':
    main()