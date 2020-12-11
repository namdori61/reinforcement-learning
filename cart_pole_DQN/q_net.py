import random

import torch
import torch.nn as nn
import torch.nn.functional as F


class Qnet(nn.Module):
    def __init__(self):
        super(Qnet, self).__init__()
        self.fc1 = nn.Linear(4, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 2)

    def forward(self,
                x: torch.Tensor = None) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def sample_action(self,
                      obs: torch.Tensor = None,
                      eps: float = None) -> int:
        out = self.forward(obs)
        coin = random.random()
        if coin < eps:
            return random.randint(0, 1)
        else:
            return out.argmax().item()