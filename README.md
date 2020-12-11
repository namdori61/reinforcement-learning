# reinforcement-learning
reinforcement learning tutorial

## References
1. 바닥부터 배우는 강화학습, 노승은, 영진닷컴, 2020
2. Fundamental of Reinforcement Learning, 이웅원, https://dnddnjs.gitbooks.io/rl/content/

## Requirements

- tqdm
- numpy

## Model Free & Small world (Grid World)

### MC (Monte Carlo)
- MC prediction : `python grid_world/mc_prediction.py --num_episode [int]`
- MC control : `python grid_world/mc_control.py --num_episode [int]`

### TD (Temporal Difference)
- TD prediction : `python grid_world/td_prediction.py --num_episode [int]`
- TD control (SARSA) : `python grid_world/sarsa.py --num_episode [int]`
- TD control (Q-Learing) : `python grid_world/q_learning.py --num_episode [int]`