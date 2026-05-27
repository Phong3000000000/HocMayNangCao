"""
Test Suite for State Encoder/Decoder.

Tests cover:
    - Encoder/decoder roundtrip for all 2646 states
    - Correct encoding formula
    - Boundary values
    - Decoder inverse correctness

Run with:
    python -m pytest tests/test_encoder.py -v

Author: RL Inventory Management Team
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from envs.custom_env import InventoryEnv


class TestEncoderDecoder:
    """Test state_encoder() and state_decoder() correctness."""

    def setup_method(self):
        self.env = InventoryEnv()

    def test_roundtrip_all_states(self):
        """
        Encoding then decoding every possible state should return
        the original state tuple.

        Total states: 21 × 3 × 7 × 6 = 2646
        """
        count = 0
        for inv in range(self.env.N_INVENTORY):       # 0..20
            for regime in range(self.env.N_REGIME):    # 0..2
                for dow in range(self.env.N_DOW):      # 0..6
                    for pending in range(self.env.N_PENDING):  # 0..5
                        state = (inv, regime, dow, pending)
                        encoded = self.env.state_encoder(state)
                        decoded = self.env.state_decoder(encoded)

                        assert decoded == state, (
                            f"Roundtrip failed: {state} → {encoded} → {decoded}"
                        )
                        count += 1

        assert count == self.env.N_STATES, \
            f"Expected {self.env.N_STATES} states, tested {count}"

    def test_encoder_range(self):
        """All encoded states should be in [0, N_STATES-1]."""
        for inv in range(self.env.N_INVENTORY):
            for regime in range(self.env.N_REGIME):
                for dow in range(self.env.N_DOW):
                    for pending in range(self.env.N_PENDING):
                        encoded = self.env.state_encoder(
                            (inv, regime, dow, pending)
                        )
                        assert 0 <= encoded < self.env.N_STATES, \
                            f"Encoded {encoded} out of range [0, {self.env.N_STATES})"

    def test_encoder_unique(self):
        """Each state tuple should map to a unique integer."""
        seen = set()
        for inv in range(self.env.N_INVENTORY):
            for regime in range(self.env.N_REGIME):
                for dow in range(self.env.N_DOW):
                    for pending in range(self.env.N_PENDING):
                        encoded = self.env.state_encoder(
                            (inv, regime, dow, pending)
                        )
                        assert encoded not in seen, \
                            f"Duplicate encoding: {encoded} for " \
                            f"state ({inv}, {regime}, {dow}, {pending})"
                        seen.add(encoded)

        assert len(seen) == self.env.N_STATES

    def test_specific_encoding_values(self):
        """Test specific state → index mappings."""
        # State (0, 0, 0, 0) → should be 0
        assert self.env.state_encoder((0, 0, 0, 0)) == 0

        # State (0, 0, 0, 1) → should be 1
        assert self.env.state_encoder((0, 0, 0, 1)) == 1

        # State (0, 0, 0, 5) → should be 5
        assert self.env.state_encoder((0, 0, 0, 5)) == 5

        # State (0, 0, 1, 0) → should be 6 (N_PENDING = 6)
        assert self.env.state_encoder((0, 0, 1, 0)) == 6

        # State (0, 1, 0, 0) → should be 42 (N_DOW * N_PENDING = 42)
        assert self.env.state_encoder((0, 1, 0, 0)) == 42

        # State (1, 0, 0, 0) → should be 126 (N_REGIME * N_DOW * N_PENDING)
        assert self.env.state_encoder((1, 0, 0, 0)) == 126

        # Last state (20, 2, 6, 5) → should be 2645
        assert self.env.state_encoder((20, 2, 6, 5)) == 2645

    def test_decoder_boundary_values(self):
        """Test decoding of boundary encoded values."""
        # Decode 0 → (0, 0, 0, 0)
        assert self.env.state_decoder(0) == (0, 0, 0, 0)

        # Decode 2645 → (20, 2, 6, 5)
        assert self.env.state_decoder(2645) == (20, 2, 6, 5)

    def test_encoder_formula_consistency(self):
        """
        Verify the encoding formula:
        index = inv * (3 * 7 * 6) + regime * (7 * 6) + dow * 6 + pending
              = inv * 126 + regime * 42 + dow * 6 + pending
        """
        for inv in [0, 5, 10, 15, 20]:
            for regime in [0, 1, 2]:
                for dow in [0, 3, 6]:
                    for pending in [0, 2, 5]:
                        expected = (inv * 126 + regime * 42
                                    + dow * 6 + pending)
                        actual = self.env.state_encoder(
                            (inv, regime, dow, pending)
                        )
                        assert actual == expected, \
                            f"Formula mismatch: expected {expected}, got {actual}"

    def test_state_space_size(self):
        """N_STATES should be 2646."""
        assert self.env.N_STATES == 2646
        assert self.env.N_STATES == 21 * 3 * 7 * 6

    def test_action_space_size(self):
        """N_ACTIONS should be 6."""
        assert self.env.N_ACTIONS == 6


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
