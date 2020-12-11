import argparse
from tqdm import tqdm

import gym
import torch
import torch.nn.functional as F
import torch.optim as optim

from replay_buffer import ReplayBuffer
from q_net import Qnet


parser = argparse.ArgumentParser(description='CartPole DQN')
parser.add_argument('--num_episode', type=int,
                    default=10000,
                    help='The number of episodes in DQN')
parser.add_argument('--lr', type=float,
                    default=0.0005,
                    help='The learning rate of DQN')
parser.add_argument('--gamma', type=float,
                    default=0.98,
                    help='The gamma of DQN')
parser.add_argument('--buffer_limit', type=int,
                    default=50000,
                    help='The buffer limit of Replay Buffer')
parser.add_argument('--batch_size', type=int,
                    default=32,
                    help='The batch size of DQN')
args = parser.parse_args()


def train(q,
          q_target,
          memory,
          optimizer):
    for i in range(10):
        s, a, r, s_prime, done_mask = memory.sample(args.batch_size)

        q_out = q(s)
        q_a = q_out.gather(1, a)
        max_q_prime = q_target(s_prime).max(1)[0].unsqueeze(1)
        target = r + args.gamma * max_q_prime * done_mask
        loss = F.smooth_l1_loss(q_a, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


def main():
    env = gym.make('CartPole-v1')
    q = Qnet()
    q_target = Qnet()
    q_target.load_state_dict(q.state_dict())
    memory = ReplayBuffer()

    print_interval = 20
    score = 0.0
    optimizer = optim.Adam(q.parameters(), lr=args.lr)

    for n_epi in tqdm(range(args.num_episode), desc='sampling episodes'):
        eps = max(0.01, 0.08 - 0.01 * (n_epi / 200)) # Linear annealing from 0.08 to 0.01
        s = env.reset()
        done = False

        while not done:
            a = q.sample_action(torch.from_numpy(s).float(), eps)
            s_prime, r, done, info = env.step(a)
            done_mask = 0.0 if done else 1.0
            memory.put((s, a, r/100.0, s_prime, done_mask))
            s = s_prime
            score += r
            if done:
                break

        if memory.size() > 2000:
            train(q, q_target, memory, optimizer)

        if n_epi % print_interval == 0 and n_epi != 0:
            q_target.load_state_dict(q.state_dict())
            print(f'n_episoe: {n_epi}, score: {score / print_interval:.1f}, n_buffer: {memory.size()}, eps: {eps*100:.1f}')
            score = 0.0

    env.close()


if __name__ == '__main__':
    main()