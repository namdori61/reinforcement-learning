import argparse
from tqdm import tqdm

from env import GridWorld
from agent import Agent


parser = argparse.ArgumentParser(description='GraidWorld TD')
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
    alpha = 0.01 #reduce learning rate based on low variance

    for k in tqdm(range(args.num_episode), desc='sampling episodes'):
        done = False
        while not done:
            x, y = env.get_state()
            action = agent.select_action()
            (x_prime, y_prime), reward, done = env.step(action)
            x_prime, y_prime = env.get_state()

            #table update after one step
            data[x][y] = data[x][y] + alpha * (reward + gamma * data[x_prime][y_prime] - data[x][y])
        env.reset()

    for row in data:
        print(row)


if __name__ == '__main__':
    main()