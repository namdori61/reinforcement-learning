from typing import Tuple
import random
import argparse
from tqdm import tqdm


parser = argparse.ArgumentParser(description='GraidWorld MC')
parser.add_argument('--num_episode', type=int,
                    default=50000,
                    help='The number of episodes in MC')
args = parser.parse_args()


class GridWorld:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def step(self, a: int = None) -> Tuple[Tuple[int, int], int, bool]:
        if a == 0:
            self.move_right()
        elif a == 1:
            self.move_left()
        elif a == 2:
            self.move_up()
        elif a == 3:
            self.move_down()

        reward = -1
        done = self.is_done()
        return (self.x, self.y), reward, done

    def move_right(self) -> None:
        self.y += 1
        if self.y > 3:
            self.y = 3

    def move_left(self) -> None:
        self.y -= 1
        if self.y < 0:
            self.y = 0

    def move_up(self) -> None:
        self.x -= 1
        if self.x < 0:
            self.x = 0

    def move_down(self) -> None:
        self.x += 1
        if self.x > 3:
            self.x = 3

    def is_done(self) -> bool:
        if self.x == 3 and self.y == 3:
            return True
        else:
            return False

    def get_state(self) -> Tuple[int, int]:
        return self.x, self.y

    def reset(self) -> Tuple[int, int]:
        self.x = 0
        self.y = 0
        return self.x, self.y


class Agent:
    def __init__(self) -> None:
        pass

    def select_action(self) -> int:
        coin = random.random()
        if coin < 0.25:
            action = 0
        elif coin < 0.5:
            action = 1
        elif coin < 0.75:
            action = 2
        else:
            action = 3
        return action


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