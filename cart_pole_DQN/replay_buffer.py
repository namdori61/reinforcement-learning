from typing import Tuple, Union
import collections
import random

import torch


class ReplayBuffer:
    def __init__(self,
                 buffer_limit: int = 50000) -> None:
        self.buffer = collections.deque(maxlen=buffer_limit)  # FIFO

    def put(self,
            transition: Tuple[Union[Tuple[int], int]] = None) -> None:
        self.buffer.append(transition)

    def sample(self,
               n: int = None) -> Tuple[torch.Tensor]:
        mini_batch = random.sample(self.buffer, n)
        s_lst, a_lst, r_lst, s_prime_lst, done_mask_lst = [], [], [], [], []

        for transition in mini_batch:
            s, a, r, s_prime, done_mask = transition
            s_lst.append(s)
            a_lst.append([a])
            r_lst.append([r])
            s_prime_lst.append(s_prime)
            done_mask_lst.append([done_mask])

        return torch.tensor(s_lst, dtype=torch.float), torch.tensor(a_lst), torch.tensor(r_lst), \
               torch.tensor(s_prime_lst, dtype=torch.float), torch.tensor(done_mask_lst)

    def size(self) -> int:
        return len(self.buffer)