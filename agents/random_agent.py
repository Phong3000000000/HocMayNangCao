"""
Random Agent for Inventory Management.

Baseline agent that selects actions uniformly at random.
Used as a lower-bound performance benchmark.

Author: RL Inventory Management Team
"""

import numpy as np


class RandomAgent:
    """
    Random Agent: selects order quantity uniformly at random from {0, ..., n_actions-1}.

    This serves as the weakest baseline. Any trained RL agent should
    significantly outperform this agent.
    """

    def __init__(self, n_actions, seed=None):
        """
        Args:
            n_actions (int): Number of possible actions (6 for order 0–5).
            seed (int, optional): Random seed for reproducibility.
        """
        self.n_actions = n_actions
        self.rng = np.random.RandomState(seed)
        self.name = "Random Agent"
        self.on_policy = False  # Off-policy (no learning)

    def select_action(self, state):
        """Select a random action regardless of state."""
        return self.rng.randint(0, self.n_actions)

    def update(self, state, action, reward, next_state, done):
        """No learning — random agent does not update."""
        pass

    def set_eval_mode(self):
        """No-op: random agent behaves the same in eval mode."""
        pass

    def set_train_mode(self):
        """No-op: random agent behaves the same in train mode."""
        pass
