import math
import random
import numpy as np
from copy import deepcopy
from typing import Dict, List, Callable
from models import Schedule


# tag::mcts-node[]
class MCTSNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state: Schedule = game_state
        self.move = move
        self.parent = parent        # Optional[UCTNode]
        self.win_counts: float = 0.0
        self.num_rollouts: int = 0
        self.children = []
        self.unvisited_moves: List[int] = game_state.legal_choices()
# end::mcts-node[]

# tag::mcts-add-child[]
    def add_random_child(self):
        index: int = random.randint(0, len(self.unvisited_moves) - 1)
        # index: int = 0
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


class MCTSAgent:
    def __init__(self, num_rounds, temperature):
        self.num_rounds = num_rounds
        self.temperature = temperature
        self.k = 0

# tag::mcts-signature[]
    def select_move(self, game_state: Schedule):
        print('Start!')
        root: MCTSNode = MCTSNode(game_state)
        print(root.game_state.sequence)
# end::mcts-signature[]

# tag::mcts-rounds[]
        for _ in range(self.num_rounds):
            node: MCTSNode = root
            self.k += 1

            print("============= {} =============".format(self.k))

            while (not node.can_add_child()) and (not node.is_terminal()):
                node: MCTSNode = self.select_child(node)
                print("State: {}, Reward: {:3.2f}, Number of Times: {}".format(
                    node.game_state.sequence, node.win_counts, node.num_rollouts))

            # Add a new child node into the tree.
            if node.can_add_child():
                node: MCTSNode = node.add_random_child()
                print("populate:")
                print("State: {}, Reward: {:3.2f}, Number of Times: {}".format(
                    node.game_state.sequence, node.win_counts, node.num_rollouts))

            print("==============================")

            # Simulate a random game from this node.
            reward: float = self.simulate_random_game(node.game_state)

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


# tag::mcts-selection[]
        # Having performed as many MCTS rounds as we have time for, we
        # now pick a move.
        best_move = None
        best_pct = -100000.0
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

        best_score = -100000.0
        best_child = None
        # Loop over each child.
        for child in node.children:
            # Calculate the UCT score.
            win_percentage = child.winning_frac()
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            # I changed the sign infornt of temp.
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
        reward: float = -1 * new_schedule.evaluate()
        return reward

