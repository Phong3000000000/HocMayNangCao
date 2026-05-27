"""
Base Environment Class for Reinforcement Learning.

Defines the abstract interface that all custom RL environments must implement.
Follows the Gymnasium-style API structure (reset, step, render) without
importing or using Gymnasium itself.

Author: RL Inventory Management Team
"""

from abc import ABC, abstractmethod


class BaseEnv(ABC):
    """
    Abstract base class for RL environments.
    
    Every custom environment must implement:
        - reset(seed): Initialize/reset environment state
        - step(action): Execute one action, return (next_state, reward, terminated, truncated, info)
        - render(): Display current state
        - state_encoder(state): Convert state tuple → single integer index
        - state_decoder(encoded_state): Convert integer index → state tuple
    """

    @abstractmethod
    def reset(self, seed=None):
        """
        Reset the environment to an initial state.

        Args:
            seed (int, optional): Random seed for reproducibility.
                If provided, the environment's RNG is reseeded to ensure
                deterministic behavior for the same seed.

        Returns:
            state (int): Encoded initial state.
            info (dict): Dictionary with additional information about the initial state.
        """
        pass

    @abstractmethod
    def step(self, action):
        """
        Execute one time step in the environment.

        Args:
            action (int): The action chosen by the agent.

        Returns:
            next_state (int): Encoded state after the action.
            reward (float): Scalar reward received after the transition.
            terminated (bool): True if the episode has naturally ended
                (e.g., reached max steps).
            truncated (bool): True if the episode was cut short
                (e.g., safety constraint).
            info (dict): Additional diagnostic information.
        """
        pass

    @abstractmethod
    def render(self):
        """
        Render/display the current state of the environment.

        Returns:
            str: A formatted string representation of the current state.
        """
        pass

    @abstractmethod
    def state_encoder(self, state):
        """
        Encode a structured state (e.g., tuple) into a single integer index.

        This is needed for tabular methods (Q-Learning, SARSA, etc.)
        which index the Q-table by a single integer.

        Args:
            state (tuple): The structured state representation.

        Returns:
            int: A unique integer index for this state.
        """
        pass

    @abstractmethod
    def state_decoder(self, encoded_state):
        """
        Decode a single integer index back into the structured state tuple.

        Args:
            encoded_state (int): The integer index of the state.

        Returns:
            tuple: The structured state representation.
        """
        pass
