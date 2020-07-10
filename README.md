## Performance Analysis of Networked Control Systems under Periodic Communication Schedules

[![arxiv](https://img.shields.io/badge/eess.SY-arXiv%3A2006.08015-B31B1B.svg)](https://arxiv.org/abs/2006.08015)

### Abstract

We here consider a networked control system that consists of `N` independent linear feedback control loops, sharing a communication network with `M` channels (i.e., `M<N`). A centralized scheduler, using a scheduling protocol that produces periodic communication sequences, dictates which feedback loops should utilize all these channels. When periodically allocating multiple communication channels to multiple feedback control systems, we compute the infinite-horizon control loss by using `costfunction`, in which the analytic expressions for quantifying the overall control performance are implemented.

### Requirements

This code was tested on **Python 3.7.6**. To install the required python pakages, please run:

```python
pip3 install -r requirements.txt
```

### Numerical results

For a collection of three unstable subsystems that communicates over a single channels (by using `systems(n=2,m=1,p=1,N=3,M=1,seed=20)`), the optimal communication sequence  can be obtained, via **exhaustive search**, by running:

```python
python3 example_exhaustive_search.py
```

For a collection of three unstable subsystems that communicates over a single channels (by using `systems(n=2,m=1,p=1,N=3,M=1,seed=20)`), the **offline** optimization of communication sequences can be done, via **MCTS**, by running:

```python
python3 example_mcts.py
```

Optimal periodic schedules for three feedback loops while sharing a single channel can be obtained as shown in the figure below.

| Period | Periodic sequence       | Total loss  |
| ------ | ----------------------- | ----------- |
| 3      | 2,3,1                   | 576.2013    |
| 4      | 2,1,3,1                 | 385.9708    |
| 5      | 2,1,3,1,1               | 399.8308    |
| 6      | 2,1,2,1,3,1             | 385.3658    |
| 7      | 2,1,3,1,2,1,1           | 380.4990    |
| 9      | 2,1,2,1,3,1,2,1,1       | 390.7592    |
| 10     | 2,1,2,1,3,1,2,1,3,1     | 385.6078    |
| 11     | 2,1,1,2,1,3,1,2,1,3,1   | 382.4858    |
| 12     | 2,1,2,1,3,1,2,1,2,1,3,1 | 385.3658    |

For a group of five unstable subsystems that communicates over a network with two channels (by using `systems(n=4,m=3,p=2,N=5,M=2,seed=65)`), the **offline** optimization of communication sequences can be done, via **MCTS**, by running:

```python
python3 example_mcts_v2.py
```
