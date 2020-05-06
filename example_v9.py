import math
import random
import copy
import enum
import numpy as np
from copy import deepcopy
from collections import namedtuple
from collections import defaultdict
from typing import Dict, List, Iterable, Callable, NewType
from abc import ABC, abstractmethod
from functions import costfunction

# create a python dictionary
variables: Dict = {}
# number of systems
variables['no_plants']: int = 3
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

# tag::agent[]
class Agent:
    def __init__(self):
        pass

    def select_move(self, game_state):
        raise NotImplementedError()
# end::agent[]

    def diagnostics(self):
        return {}


class Schedule:
    def __init__(self, sequence: List[int], func: Callable[[
                 List[int]], float], period: int, no_users: int) -> None:
        self.period: int = period
        self.no_users: int = no_users
        self.func: Callable[[List[int]], float] = func
        self.sequence: List[int] = sequence

    def legal_choices(self) -> List[int]:
        if self.is_over():
            return []
        return [i for i in range(1, self.no_users + 1)]

    def allocate(self, user: int) -> object:
        #if not self.is_over():
        self.sequence.append(user)
        return Schedule(self.sequence, self.func, self.period, self.no_users)

    def evaluate(self) -> float:
        return self.func(self.sequence)

    def is_over(self) -> bool:  # is_completed
        return len(self.sequence) >= self.period

    def __str__(self) -> str:  # needed to be updated
        return f"The schedule is {self.sequence} that is {self.is_over()}."


# tag::mcts-node[]
class MCTSNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state: Schedule = game_state
        self.move = move
        self.parent = parent        # Optional[UCTNode]
        self.win_counts: float = 0
        self.num_rollouts: int = 0
        self.children = []
        print('Visit MCTSNode')
        self.unvisited_moves: List[int] = game_state.legal_choices()
# end::mcts-node[]

# tag::mcts-add-child[]
    def add_random_child(self):
        index: int = random.randint(0, len(self.unvisited_moves) - 1)
        new_move: List[int] = self.unvisited_moves.pop(index)
        new_game_state: Schedule = self.game_state.allocate(new_move)
        new_node: MCTSNode = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node
# end::mcts-add-child[]

# tag::mcts-record-win[]
    def record_win(self, reward: float):
        self.win_counts += reward
        self.num_rollouts += 1
# end::mcts-record-win[]

# tag::mcts-readers[]
    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.is_over()

    def winning_frac(self):
        return float(self.win_counts) / float(self.num_rollouts)
# end::mcts-readers[]


class MCTSAgent(Agent):
    def __init__(self, num_rounds, temperature):
        Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature
        self.k = 0

# tag::mcts-signature[]
    def select_move(self, game_state: Schedule):
        print('Start!')
        root: MCTSNode = MCTSNode(game_state)
        print(root.game_state.sequence)
        print('Stop!')
# end::mcts-signature[]

# tag::mcts-rounds[]
        for _ in range(self.num_rounds):
            node: MCTSNode = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

            # Add a new child node into the tree.
            if node.can_add_child():
                node: MCTSNode = node.add_random_child()

            # Simulate a random game from this node.
            reward = self.simulate_random_game(node.game_state)
            self.k += 1
            print(self.k)
            print("Sequence: {}, Reward: {}".format(node.game_state.sequence,reward))
            #print()
            # Propagate scores back up the tree.
            while node is not None:
                node.record_win(reward)
                node = node.parent
# end::mcts-rounds[]


        scored_moves = [
            (child.winning_frac(),
             child.move, child.num_rollouts)
            for child in root.children
        ]
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        for s, m, n in scored_moves[:10]:
            print('%s - %.3f (%d)' % (m, s, n))

#        print(node)

# tag::mcts-selection[]
        # Having performed as many MCTS rounds as we have time for, we
        # now pick a move.
        best_move = None
        best_pct = -1.0    # I should change this
        for child in root.children:
            child_pct = child.winning_frac()
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        print('Select move %s with win pct %.3f' % (best_move, best_pct))
        return best_move
# end::mcts-selection[]

# tag::mcts-uct[]
    def select_child(self, node):
        """
        Select a child according to the upper confidence bound for trees (UCT) metric.
        """
        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None
        # Loop over each child.
        for child in node.children:
            # Calculate the UCT score.
            win_percentage = child.winning_frac()
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor
            # Check if this is the largest we've seen so far.
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child
# end::mcts-uct[]

    @staticmethod
    def simulate_random_game(schedule: Schedule) -> float:
        new_schedule = deepcopy(schedule)
        while not new_schedule.is_over():
            new_schedule = new_schedule.allocate(random.randint(1, 3))
        reward: float = 1 * new_schedule.evaluate()
        return reward


if __name__ == "__main__":
    # construct the cost function
    costfunc = costfunction(variables)
    # create an instant for schedule
    schedule = Schedule([], costfunc, 10, 3)
    print(schedule)
    # ...
    bot = MCTSAgent(10, temperature=1.4)
    #
#    while not schedule.is_over():
    move = bot.select_move(schedule)
#    schedule.allocate(move)

    print(schedule)
    print(costfunc(schedule.sequence))




#    bot = MCTSAgent(500, temperature=1.4)
#    bot.select_move(schedule.game_state)


#    while not game.is_over():
    """
    reward = MCTSAgent.simulate_random_game(node.game_state)
    print(reward)
    """


"""
    while not game.is_over():
        print_board(game.board)
        if game.next_player == gotypes.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)
"""


"""
if __name__ == "__main__":
    schedule = Schedule([], 5, 3)

    while not schedule.is_over():
        schedule.allocate(random.randint(1, 3))
        print(schedule)
"""
