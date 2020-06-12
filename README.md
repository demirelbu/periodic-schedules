## Performance Analysis of Networked Control Systems under Periodic Communication Schedules

We here consider a networked control system that consists of `N` independent linear feedback control loops, sharing a communication network with `M` channels (i.e., `M<N`). A centralized scheduler, using a scheduling protocol that produces periodic communication sequences, dictates which feedback loops should utilize all these channels. When periodically allocating multiple communication channels to multiple feedback control systems, we compute the infinite-horizon control loss by using `costfunction`, in which the analytic expressions for quantifying the overall control performance are implemented.

The **optimal** communication sequence (for a given collection of linear feedback control subsystems) can be obtained, via **exhaustive search**, by running:

```python
python3 example_exhaustive_search.py
```

The **offline** optimization of communication sequences (for a given collection of linear feedback control subsystems) can be done, via **MCTS**, by running:

```python
python3 example_mcts.py
```

The entire paper can be downloaded from https://arxiv.org/.