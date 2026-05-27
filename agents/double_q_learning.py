"""
Double Q-Learning Agent for Inventory Management.

Addresses the maximization bias in standard Q-Learning by maintaining
TWO Q-tables (Q1, Q2) and alternating which one is updated.

Update rule (randomly choose one table to update per step):
    With 50% probability:
        a* = argmax_a Q1(s', a)
        Q1(s, a) ← Q1(s, a) + α [ r + γ · Q2(s', a*) − Q1(s, a) ]
    Otherwise:
        a* = argmax_a Q2(s', a)
        Q2(s, a) ← Q2(s, a) + α [ r + γ · Q1(s', a*) − Q2(s, a) ]

Why Double Q-Learning for inventory management:
    Demand is stochastic → Q-Learning can overestimate the value of
    certain (state, action) pairs, leading to over-ordering.
    Double Q reduces this overestimation bias.

Author: RL Inventory Management Team
"""

import numpy as np


class DoubleQLearningAgent:
    """
    Double Q-Learning agent with epsilon-greedy exploration.

    Maintains two independent Q-tables (Q1, Q2). Each update step:
        1. Randomly select which table to update (50/50)
        2. Use one table to find the best action, the other to evaluate it
        3. This decorrelates action selection from value estimation

    Action selection uses the sum Q1 + Q2 for tie-breaking.
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
        self.name = "Double Q-Learning"
        self.on_policy = False  # Off-policy

        self.rng = np.random.RandomState(seed)

        # Two independent Q-tables
        self.Q1 = np.zeros((n_states, n_actions))
        self.Q2 = np.zeros((n_states, n_actions))

        self.eval_mode = False
        self.td_errors = []

    def select_action(self, state):
        """
        Select action using epsilon-greedy on the COMBINED Q-value (Q1 + Q2).

        Args:
            state (int): Encoded state index.

        Returns:
            int: Selected action.
        """
        # Combined Q for action selection
        combined_Q = self.Q1[state] + self.Q2[state]

        if self.eval_mode:
            return int(np.argmax(combined_Q))

        if self.rng.random() < self.epsilon:
            return self.rng.randint(0, self.n_actions)
        else:
            return int(np.argmax(combined_Q))

    def update(self, state, action, reward, next_state, done):
        """
        Double Q-Learning update.

        Randomly choose which Q-table to update:
            - Update Q1: use Q1 to find best action, Q2 to evaluate
            - Update Q2: use Q2 to find best action, Q1 to evaluate

        This prevents the same Q-table from both selecting AND evaluating
        the action, which would cause overestimation.

        Args:
            state (int): Current state.
            action (int): Action taken.
            reward (float): Reward received.
            next_state (int): Next state.
            done (bool): Whether episode ended.
        """
        if self.eval_mode:
            return

        if self.rng.random() < 0.5:
            # ── Update Q1 ─────────────────────────────────────
            if done:
                td_target = reward
            else:
                # Q1 selects the action, Q2 evaluates it
                best_action = int(np.argmax(self.Q1[next_state]))
                td_target = reward + self.gamma * self.Q2[next_state, best_action]

            td_error = td_target - self.Q1[state, action]
            self.Q1[state, action] += self.alpha * td_error
        else:
            # ── Update Q2 ─────────────────────────────────────
            if done:
                td_target = reward
            else:
                # Q2 selects the action, Q1 evaluates it
                best_action = int(np.argmax(self.Q2[next_state]))
                td_target = reward + self.gamma * self.Q1[next_state, best_action]

            td_error = td_target - self.Q2[state, action]
            self.Q2[state, action] += self.alpha * td_error

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
        """
        Extract greedy policy from the combined Q-table (Q1 + Q2).

        Returns:
            np.ndarray: Best action for each state, shape (n_states,).
        """
        combined_Q = self.Q1 + self.Q2
        return np.argmax(combined_Q, axis=1)

    def get_Q(self):
        """
        Return the averaged Q-table: (Q1 + Q2) / 2.

        Returns:
            np.ndarray: Averaged Q-values, shape (n_states, n_actions).
        """
        return (self.Q1 + self.Q2) / 2.0

    def save(self, filepath):
        """Save both Q-tables and epsilon to file."""
        np.savez(filepath,
                 Q1=self.Q1,
                 Q2=self.Q2,
                 epsilon=np.array([self.epsilon]))

    def load(self, filepath):
        """Load both Q-tables and epsilon from file."""
        data = np.load(filepath)
        self.Q1 = data['Q1']
        self.Q2 = data['Q2']
        self.epsilon = float(data['epsilon'][0])
