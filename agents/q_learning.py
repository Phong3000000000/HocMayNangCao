"""
Q-Learning Agent for Inventory Management.

Implements tabular Q-Learning with epsilon-greedy exploration.

Update rule (TD learning):
    Q(s, a) ← Q(s, a) + α [ r + γ · max_a' Q(s', a') − Q(s, a) ]

Where:
    α  = learning rate (step size)
    γ  = discount factor (importance of future rewards)
    r + γ · max Q(s', a') = TD target
    TD target − Q(s, a) = TD error

If s' is terminal: TD target = r  (no future rewards).

Author: RL Inventory Management Team
"""

import numpy as np


class QLearningAgent:
    """
    Tabular Q-Learning agent with epsilon-greedy exploration.

    Features:
        - Q-table of shape (n_states, n_actions)
        - Epsilon-greedy action selection
        - Exponential epsilon decay schedule
        - Evaluation mode with epsilon = 0 (greedy policy)
        - Save/load trained Q-tables

    Hyperparameters:
        α (alpha): Learning rate — controls how much new info overrides old
        γ (gamma): Discount factor — how much agent values future rewards
        ε (epsilon): Exploration rate — probability of random action
        ε_decay: Multiplicative decay applied to ε after each update
    """

    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.99,
                 epsilon_start=1.0, epsilon_end=0.05, epsilon_decay=0.9995,
                 seed=None):
        """
        Args:
            n_states (int): Total number of states (2646 for inventory env).
            n_actions (int): Number of possible actions (6).
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
        self.name = "Q-Learning"
        self.on_policy = False  # Q-Learning is off-policy

        # Random number generator
        self.rng = np.random.RandomState(seed)

        # Initialize Q-table with zeros
        # Shape: (n_states, n_actions) = (2646, 6)
        self.Q = np.zeros((n_states, n_actions))

        # Mode flag
        self.eval_mode = False

        # Training statistics
        self.td_errors = []

    def select_action(self, state):
        """
        Select action using epsilon-greedy policy.

        In eval mode: always select greedy action (epsilon = 0).
        In train mode: with probability ε select random, else greedy.

        Args:
            state (int): Encoded state index.

        Returns:
            int: Selected action.
        """
        # Evaluation mode: pure greedy
        if self.eval_mode:
            return int(np.argmax(self.Q[state]))

        # Epsilon-greedy exploration
        if self.rng.random() < self.epsilon:
            return self.rng.randint(0, self.n_actions)
        else:
            return int(np.argmax(self.Q[state]))

    def update(self, state, action, reward, next_state, done):
        """
        Update Q-value using the Q-Learning update rule.

        Q(s, a) ← Q(s, a) + α [ r + γ · max_a' Q(s', a') − Q(s, a) ]

        If done (terminal state): target = r (no future discounted rewards).

        Args:
            state (int): Current state index.
            action (int): Action taken.
            reward (float): Reward received.
            next_state (int): Next state index.
            done (bool): Whether next_state is terminal.
        """
        if self.eval_mode:
            return  # No updates during evaluation

        # ── Compute TD target ──────────────────────────────────
        if done:
            # Terminal state: no future rewards
            td_target = reward
        else:
            # Non-terminal: r + γ · max_a' Q(s', a')
            td_target = reward + self.gamma * np.max(self.Q[next_state])

        # ── Compute TD error ───────────────────────────────────
        td_error = td_target - self.Q[state, action]

        # ── Update Q-value ─────────────────────────────────────
        self.Q[state, action] += self.alpha * td_error

        # Record TD error magnitude for monitoring
        self.td_errors.append(abs(td_error))

        # ── Decay epsilon ──────────────────────────────────────
        self.epsilon = max(self.epsilon_end,
                          self.epsilon * self.epsilon_decay)

    def set_eval_mode(self):
        """Switch to evaluation mode (epsilon = 0, no updates)."""
        self.eval_mode = True

    def set_train_mode(self):
        """Switch back to training mode."""
        self.eval_mode = False

    def reset_epsilon(self):
        """Reset epsilon to its initial value."""
        self.epsilon = self.epsilon_start

    def get_policy(self):
        """
        Extract the greedy policy from the Q-table.

        Returns:
            np.ndarray: Array of shape (n_states,) where policy[s] = best action.
        """
        return np.argmax(self.Q, axis=1)

    def save(self, filepath):
        """Save Q-table and current epsilon to file."""
        np.savez(filepath, Q=self.Q, epsilon=np.array([self.epsilon]))

    def load(self, filepath):
        """Load Q-table and epsilon from file."""
        data = np.load(filepath)
        self.Q = data['Q']
        self.epsilon = float(data['epsilon'][0])
