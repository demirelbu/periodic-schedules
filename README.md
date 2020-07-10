## Performance Analysis of Networked Control Systems under Periodic Communication Schedules

[![arxiv](https://img.shields.io/badge/eess.SY-arXiv%3A2006.08015-B31B1B.svg)](https://arxiv.org/abs/2006.08015)

### Abstract

We here consider a networked control system that consists of `N` independent linear feedback control loops, sharing a communication network with `M` channels (i.e., `M<N`). A centralized scheduler, using a scheduling protocol that produces periodic communication sequences, dictates which feedback loops should utilize all these channels. When periodically allocating multiple communication channels to multiple feedback control systems, we compute the infinite-horizon control loss by using `costfunction`, in which the analytic expressions for quantifying the overall control performance are implemented.

### Requirements

This code was tested on Python 3.7.6. To install the required python pakages, please run:

```python
pip3 install -r requirements.txt
```

### Results

The **optimal** communication sequence (for a given collection of linear feedback control systems) can be obtained, via **exhaustive search**, by running:

```python
python3 example_exhaustive_search.py
```

The **offline** optimization of communication sequences (for a given collection of linear feedback control systems) can be done, via **MCTS**, by running:

```python
python3 example_mcts.py
```
