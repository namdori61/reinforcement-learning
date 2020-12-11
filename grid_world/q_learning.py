import argparse
from tqdm import tqdm

from env import UpgradedGridWorld
from agent import QAgent


parser = argparse.ArgumentParser(description='Upgraded GraidWorld TD control')
parser.add_argument('--num_episode', type=int,
                    default=1000,
                    help='The number of episodes in MC')
args = parser.parse_args()


def main():
    env = UpgradedGridWorld()
    agent = QAgent(alpha=0.1)

    for n_epi in tqdm(range(args.num_episode), desc='sampling episodes'):
        done = False

        s = env.reset()
        while not done:
            a = agent.select_action(s)
            s_prime, r, done = env.step(a)
            agent.q_learning_update_table((s, a, r, s_prime))
            s = s_prime

        agent.anneal_eps(step=0.01)

    agent.show_table()


if __name__ == '__main__':
    main()