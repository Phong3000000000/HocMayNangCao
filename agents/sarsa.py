"""
SARSA Agent for Inventory Management.

Implements tabular SARSA (State-Action-Reward-State-Action) — an ON-POLICY
temporal difference learning algorithm.

Update rule:
    Q(s, a) ← Q(s, a) + α [ r + γ · Q(s', a') − Q(s, a) ]

Key difference from Q-Learning:
    - Q-Learning uses max_a' Q(s', a') (off-policy, uses best possible action)
    - SARSA uses Q(s', a') where a' is the action actually taken (on-policy)

This makes SARSA more conservative: it learns the value of the policy
it is actually following (including exploratory actions), not the optimal policy.

Author: RL Inventory Management Team
"""

import numpy as np


class SARSAAgent:
    """
    Tabular SARSA agent with epsilon-greedy exploration.

    SARSA is on-policy: it updates Q using the action actually taken
    in the next state, not the greedy action.

    Features:
        - Q-table of shape (n_states, n_actions)
        - Epsilon-greedy action selection
        - Exponential epsilon decay
        - Evaluation mode with epsilon = 0
        - Save/load Q-tables
    """

    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.99,
                 epsilon_start=1.0, epsilon_end=0.05, epsilon_decay=0.9995,
                 seed=None):
        """
        Args:
            n_states (int): Total number of states (2646).
            n_actions (int): Number of actions (6).
            alpha (float): Learning rate.
            gamma (float): Discount factor.
            epsilon_start (float): Initial exploration rate.
            epsilon_end (float): Minimum exploration rate.
            epsilon_decay (float): Multiplicative decay per step.
            seed (int, optional): Random seed.
        """
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.name = "SARSA"
        self.on_policy = True  # SARSA is on-policy

        self.rng = np.random.RandomState(seed)

        # Initialize Q-table with zeros
        self.Q = np.zeros((n_states, n_actions))

        self.eval_mode = False
        self.td_errors = []

    def select_action(self, state):
        """
        Select action using epsilon-greedy policy.

        Args:
            state (int): Encoded state index.

        Returns:
            int: Selected action.
        """
        if self.eval_mode:
            return int(np.argmax(self.Q[state]))

        if self.rng.random() < self.epsilon:
            return self.rng.randint(0, self.n_actions)
        else:
            return int(np.argmax(self.Q[state]))

    def update(self, state, action, reward, next_state, done,
               next_action=None):
        """
        Update Q-value using the SARSA update rule.

        Q(s, a) ← Q(s, a) + α [ r + γ · Q(s', a') − Q(s, a) ]

        Unlike Q-Learning, SARSA uses the actual next action a' rather
        than max_a' Q(s', a').

        Args:
            state (int): Current state.
            action (int): Action taken.
            reward (float): Reward received.
            next_state (int): Next state.
            done (bool): Whether episode ended.
            next_action (int, optional): The action actually selected in
                next_state. Required for SARSA (on-policy update).
        """
        if self.eval_mode:
            return

        # ── TD target ──────────────────────────────────────────
        if done:
            td_target = reward
        else:
            # On-policy: use Q(s', a') where a' is the actual next action
            if next_action is None:
                # Fallback: select next action now (less ideal but works)
                next_action = self.select_action(next_state)
            td_target = reward + self.gamma * self.Q[next_state, next_action]

        # ── TD error & update ──────────────────────────────────
        td_error = td_target - self.Q[state, action]
        self.Q[state, action] += self.alpha * td_error

        self.td_errors.append(abs(td_error))

        # ── Decay epsilon ──────────────────────────────────────
        self.epsilon = max(self.epsilon_end,
                          self.epsilon * self.epsilon_decay)

    def set_eval_mode(self):
        """Switch to evaluation mode (epsilon = 0)."""
        self.eval_mode = True

    def set_train_mode(self):
        """Switch back to training mode."""
        self.eval_mode = False

    def reset_epsilon(self):
        """Reset epsilon to initial value."""
        self.epsilon = self.epsilon_start

    def get_policy(self):
        """Extract greedy policy from Q-table."""
        return np.argmax(self.Q, axis=1)

    def save(self, filepath):
        """Save Q-table and epsilon."""
        np.savez(filepath, Q=self.Q, epsilon=np.array([self.epsilon]))

    def load(self, filepath):
        """Load Q-table and epsilon."""
        data = np.load(filepath)
        self.Q = data['Q']
        self.epsilon = float(data['epsilon'][0])
