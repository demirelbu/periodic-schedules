import time
import math
import random
import numpy as np
from typing import Dict, List
from functions import costfunction

# create a python dictionary
variables: Dict = {}
# number of systems
variables['no_plants'] = 3
# System 1
variables['A1'] = np.matrix([[0.8114, 0.3277], [0.4478, 0.8819]])
variables['B1'] = np.matrix([[0.6651], [0.8834]])
variables['C1'] = np.matrix([[0.7117, 0.6653]])
variables['Q1'] = np.matrix(
    [[1.2146, 0.2539], [0.2539, 1.4417]])                   # state cost
variables['R1'] = np.matrix(
    [[0.6676]])                                             # control cost
# covariance of process noise
variables['W1'] = np.matrix([[1.0324, 0.1464], [0.1464, 0.7221]])
# covariance of measurement noise
variables['V1'] = np.matrix([[0.7158]])
# System 2
variables['A2'] = np.matrix([[0.6538, 0.6301], [0.5739, 0.7875]])
variables['B2'] = np.matrix([[0.1314], [0.1582]])
variables['C2'] = np.matrix([[0.9958, 0.9315]])
variables['Q2'] = np.matrix(
    [[0.9600, 0.4860], [0.4860, 1.2684]])                   # state cost
variables['R2'] = np.matrix(
    [[1.0161]])                                             # control cost
# covariance of process noise
variables['W2'] = np.matrix(
    [[0.8992, -0.4091], [-0.4091, 1.2267]])
# covariance of measurement noise
variables['V2'] = np.matrix([[0.9359]])
# System 3
variables['A3'] = np.matrix([[0.3502, 0.6309], [0.2857, 0.8476]])
variables['B3'] = np.matrix([[0.7238], [0.3317]])
variables['C3'] = np.matrix([[1.2116, 0.9824]])
variables['Q3'] = np.matrix(
    [[0.3773, 0.1158], [0.1158, 0.4689]])                   # state cost
variables['R3'] = np.matrix(
    [[1.4400]])                                             # control cost
# covariance of process noise
variables['W3'] = np.matrix(
    [[0.6642, -0.1361], [-0.1361, 0.2247]])
# covariance of measurement noise
variables['V3'] = np.matrix([[1.2732]])


QuadraticCost = costfunction(variables)


class UCTNode:
    def __init__(self, state, parent=None, prior: float = 0.0):
        self.state = state
        #
        self.is_expanded: bool = False
        #
        self.parent = parent  # Optional[UCTNode]
        self.children = {}  # Dict[move, UCTNode]
        self.prior = prior
        self.total_value: float = 0.0
        self.number_visits: int = 0

    def Q(self) -> float:
        return self.total_value / (1 + self.number_visits)

    def U(self) -> float:
        return (math.sqrt(self.parent.number_visits) *
                self.prior / (1 + self.number_visits))

    def best_child(self):
        return max(self.children.values(),
                   key=lambda node: node.Q() + node.U())

    def select_leaf(self):
        current = self
        while current.is_expanded:
            current = current.best_child()
        return current

    def expand(self, child_priors):
        self.is_expanded = True
        for move, prior in enumerate(child_priors):
            self.add_child(move, prior)

    def add_child(self, move, prior):
        self.children[move] = UCTNode(
            self.state.play(move), parent=self, prior=prior)

    def backup(self, value_estimate: float):
        current = self
        while current.parent is not None:
            current.number_visits += 1
            current.total_value += value_estimate
            current = current.parent

    def __str__(self):
        return f'This is {self.children}.'


def UCT_search(state, num_reads):
    root = UCTNode(state)
    for _ in range(num_reads):
        leaf = root.select_leaf()
        # something here
        print(leaf.state)
        child_priors, value_estimate = NeuralNet.evaluate(leaf.state)
        leaf.expand(child_priors)
        leaf.backup(value_estimate)
    return max(root.children.items(), key=lambda item: item[1].number_visits)

"""
class rollout:
    @classmethod
    def evaluate(self):
        return None, None
"""

class NeuralNet():
    @classmethod
    def evaluate(self, state):
        return np.random.random([10]), np.random.random()


class GameState():
    def __init__(self, to_play=1):
        self.to_play = to_play

    def play(self, move):
        return GameState(-self.to_play)




num_reads = 5
tick = time.time()
UCT_search(GameState(), num_reads)
tock = time.time()
print("Took %s sec to run %s times" % (tock - tick, num_reads))

