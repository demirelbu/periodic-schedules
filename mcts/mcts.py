import math
import random
from copy import deepcopy
from typing import Dict, List, Callable
from models import Schedule


class MCTSNode(object):
    def __init__(self, state, parent=None, last_action=None):
        self.state: Schedule = state
        self.last_action = last_action
        self.parent = parent
        self.value_counts: float = 0.0
        self.num_rollouts: int = 0
        self.children = []
        self.unvisited_actions: List[int] = state.allocation_options_masked

    def add_random_child(self):
        index: int = random.randint(0, len(self.unvisited_actions) - 1)
        new_action: List[int] = self.unvisited_actions.pop(index)
        new_state: Schedule = self.state.allocate(new_action)
        new_node: MCTSNode = MCTSNode(new_state, self, new_action)
        self.children.append(new_node)
        return new_node

    def record_value(self, value: float):
        self.value_counts += value
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_actions) > 0

    def is_terminal(self):
        return self.state.is_maximum_cardinality_reached

    def expected_value(self):
        return float(self.value_counts) / float(self.num_rollouts)


class MCTSAgent:
    def __init__(self, num_rounds, temperature) -> None:
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_action(self, state: Schedule) -> [float, List[int]]:
        root: MCTSNode = MCTSNode(state)
        best_value: float = -1.0
        best_sequence = None

        for _ in range(self.num_rounds):
            node: MCTSNode = root

            # Select a leaf node that is unxplored or terminal.
            while (not node.can_add_child()) and (not node.is_terminal()):
                node: MCTSNode = self.select_child(node)

            # Add a new child node into the tree.
            if node.can_add_child():
                node: MCTSNode = node.add_random_child()

            # Simulate a random game from this node.
            value: float = self.simulate_random_rollout(node.state)
            sequence: Schedule = node.state
            print(sequence.schedule)

            # Propagate scores back up the tree.
            while node is not None:
                node.record_value(value)
                node = node.parent

            # Check if this is the largest we have seen so far.
            if sequence.is_maximum_cardinality_reached and (
                    value > best_value):
                best_value: float = value
                best_sequence: Schedule = deepcopy(sequence)

        if best_sequence is None:
            return -1.0, []
        else:
            return best_sequence.evaluate, best_sequence.schedule

    def select_child(self, node):
        """
        Select a child according to the upper confidence bound for trees (UCT) metric.
        """
        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1.0
        best_child = None
        # Loop over each child.
        for child in node.children:
            # Calculate the UCT score.
            value_percentage = child.expected_value()
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = value_percentage + self.temperature * exploration_factor
            # Check if this is the largest we've seen so far.
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    @staticmethod
    def simulate_random_rollout(schedule: Schedule) -> float:
        new_schedule: Schedule = deepcopy(schedule)
        while not new_schedule.is_maximum_cardinality_reached:
            new_schedule: Schedule = new_schedule.allocate(
                random.randint(0, len(schedule.allocation_options) - 1))
        value: float = new_schedule.normalize(new_schedule.evaluate)
        return value
