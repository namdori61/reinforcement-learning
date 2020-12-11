from typing import Tuple, List, Union
import random
import numpy as np


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

class QAgent:
    def __init__(self,
                 alpha: float = 0.01) -> None:
        self.q_table = np.zeros((5, 7, 4)) # q values
        self.eps = 0.9
        self.alpha = alpha

    def select_action(self, s: Tuple = None) -> int:
        #action by eps-greedy
        x, y = s
        coin = random.random()
        if coin < self.eps:
            action = random.randint(0, 3)
        else:
            action_val = self.q_table[x, y, :]
            action = np.argmax(action_val)
        return action

    def mc_update_table(self,
                        history: List[Tuple] = None) -> None:
        #update q table value by episode(history)
        cum_reward = 0
        for transition in history[::-1]:
            s, a, r, s_prime = transition
            x, y = s
            #update by MC
            self.q_table[x, y, a] = self.q_table[x, y, a] + self.alpha * (cum_reward - self.q_table[x, y, a])
            cum_reward = cum_reward + r

    def sarsa_update_table(self,
                           transition: Tuple[Union[int, Tuple[int]]] = None) -> None:
        # update q table value by transition
        s, a, r, s_prime = transition
        x, y = s
        next_x, next_y = s_prime
        a_prime = self.select_action(s_prime) # select action in state s'
        # SARSA update
        self.q_table[x, y, a] = self.q_table[x, y, a]\
                                + self.alpha * (r + self.q_table[next_x, next_y, a_prime] - self.q_table[x, y, a])

    def q_learning_update_table(self,
                                transition: Tuple[Union[int, Tuple[int]]] = None) -> None:
        # update q table value by transition
        s, a, r, s_prime = transition
        x, y = s
        next_x, next_y = s_prime
        # Q-Learning update
        self.q_table[x, y, a] = self.q_table[x, y, a]\
                                + self.alpha * (r + np.argmax(self.q_table[next_x, next_y, :]) - self.q_table[x, y, a])


    def anneal_eps(self,
                   step: float = 0.03) -> None:
        self.eps -= step
        self.eps = max(self.eps, 0.1)

    def show_table(self):
        #Show actions that has max q value
        q_lst = self.q_table.tolist()
        data = np.zeros((5, 7))
        for row_idx in range(len(q_lst)):
            row = q_lst[row_idx]
            for col_idx in range(len(row)):
                col = row[col_idx]
                action = np.argmax(col)
                data[row_idx, col_idx] = action
        print(data)