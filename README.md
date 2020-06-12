## Performance Analysis of Networked Control Systems under Periodic Communication Schedules

We consider a networked control system that consists of `N` independent linear feedback control loops, sharing a communication network with `M` channels (`M<N`). A centralized scheduler, employing a scheduling protocol that produces periodic communication sequences, dictates which feedback loops should utilize all these channels. Under the periodic scheduling protocol, we derive analytic expressions for quantifying the overall control performance of the networked control system in terms of a quadratic function.


We also study the offline optimization of communication sequences for a given collection of linear feedback control subsystems and determine the period of these communication sequences that attains the near-optimal control performance.

To compute the **optimal** sequence of allocation for a given set of periods via **exhaustive search**, one can run

```python
python3 example_exhaustive_search.py
```

To compute the **near-optimal** sequence of allocation for a given set of periods via **MCTS**, one can run

```python
python3 example_mcts.py
```