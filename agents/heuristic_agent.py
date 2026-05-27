"""
Heuristic Agents for Inventory Management.

Two rule-based baselines:
1. AlwaysOrder2Agent: Always orders exactly 2 units per day.
2. ReorderThresholdAgent: Orders 5 units when inventory drops below 5.

These represent simple, interpretable policies that RL agents should
be able to outperform.

Author: RL Inventory Management Team
"""


class AlwaysOrder2Agent:
    """
    Always Order 2 Agent: orders exactly 2 units every day regardless of state.

    This is the simplest non-random baseline. It provides a steady but
    inflexible restocking policy.
    """

    def __init__(self):
        self.name = "Always Order 2"
        self.on_policy = False

    def select_action(self, state):
        """Always return action = 2 (order 2 units)."""
        return 2

    def update(self, state, action, reward, next_state, done):
        """No learning — fixed heuristic."""
        pass

    def set_eval_mode(self):
        pass

    def set_train_mode(self):
        pass


class ReorderThresholdAgent:
    """
    Reorder Threshold Agent: if inventory < threshold, order a fixed amount.

    Default policy:
        - If inventory < 5 → order 5 units
        - Otherwise → order 0 units

    This mimics a common real-world reorder-point policy.

    Args:
        threshold (int): Inventory level below which an order is placed.
        order_amount (int): Number of units to order when triggered.
        env: Environment instance (needed to decode state → inventory).
    """

    def __init__(self, threshold=5, order_amount=5, env=None):
        self.threshold = threshold
        self.order_amount = order_amount
        self.env = env  # Used to decode state to extract inventory
        self.name = f"Reorder (inv<{threshold} -> order {order_amount})"
        self.on_policy = False

    def select_action(self, state):
        """
        Order if inventory is below the threshold.

        Args:
            state (int): Encoded state index. Decoded to extract inventory level.

        Returns:
            int: 0 if inventory >= threshold, else order_amount (capped at 5).
        """
        if self.env is not None:
            inventory, _, _, _ = self.env.state_decoder(state)
        else:
            # Fallback: assume state IS the inventory level
            inventory = state

        if inventory < self.threshold:
            return min(self.order_amount, 5)  # Cap at max order
        return 0

    def update(self, state, action, reward, next_state, done):
        """No learning — fixed heuristic."""
        pass

    def set_eval_mode(self):
        pass

    def set_train_mode(self):
        pass
