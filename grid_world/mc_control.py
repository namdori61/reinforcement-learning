import argparse
from tqdm import tqdm

from env import UpgradedGridWorld
from agent import QAgent


parser = argparse.ArgumentParser(description='Upgraded GraidWorld MC control')
parser.add_argument('--num_episode', type=int,
                    default=1000,
                    help='The number of episodes in MC')
args = parser.parse_args()


def main():
    env = UpgradedGridWorld()
    agent = QAgent()

    for n_epi in tqdm(range(args.num_episode), desc='sampling episodes'):
        done = False
        history = []

        s = env.reset()
        while not done:
            a = agent.select_action(s)
            s_prime, r, done = env.step(a)
            history.append((s, a, r, s_prime))
            s = s_prime

        agent.update_table(history)
        agent.anneal_eps()

    agent.show_table()


if __name__ == '__main__':
    main()