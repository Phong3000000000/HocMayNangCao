"""
Training Script for RL Inventory Management Agents.

Trains Q-Learning, SARSA, and Double Q-Learning agents over multiple seeds
and logs comprehensive metrics for analysis.

Usage:
    python experiments/train.py

Output:
    results/<agent_name>/seed_<i>.npz  — Saved Q-tables
    results/<agent_name>_history.json  — Training history per seed

Author: RL Inventory Management Team
"""

import os
import sys
import yaml
import numpy as np
import json
import argparse

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from envs.custom_env import InventoryEnv
from agents.q_learning import QLearningAgent
from agents.sarsa import SARSAAgent
from agents.double_q_learning import DoubleQLearningAgent


def load_config(config_path=None):
    """Load training configuration from YAML file."""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'configs.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def train_agent(agent, env, n_episodes, eval_interval=250,
                eval_episodes=30, verbose=True):
    """
    Train a single RL agent and return training history.

    Handles both on-policy (SARSA) and off-policy (Q-Learning, Double Q)
    training loops automatically.

    Args:
        agent: Agent instance with select_action(), update() methods.
        env: InventoryEnv instance.
        n_episodes (int): Number of training episodes.
        eval_interval (int): Evaluate every N episodes.
        eval_episodes (int): Number of evaluation episodes.
        verbose (bool): Whether to print progress.

    Returns:
        dict: Training history with metrics per episode.
    """
    history = {
        'episode_rewards': [],
        'episode_profits': [],
        'episode_stockout_rates': [],
        'episode_holding_costs': [],
        'episode_order_frequencies': [],
        'episode_avg_inventories': [],
        'eval_rewards': [],
        'eval_episodes': [],
        'epsilons': [],
    }

    is_sarsa = getattr(agent, 'on_policy', False)

    for episode in range(n_episodes):
        # Reset environment (use episode number as part of randomization)
        state, info = env.reset(seed=None)
        total_reward = 0.0
        done = False

        if is_sarsa:
            # ── SARSA training loop (on-policy) ────────────────
            action = agent.select_action(state)

            while not done:
                next_state, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated

                # Select next action BEFORE updating (on-policy)
                next_action = agent.select_action(next_state) if not done else 0
                agent.update(state, action, reward, next_state, done,
                             next_action=next_action)

                state = next_state
                action = next_action
                total_reward += reward
        else:
            # ── Q-Learning / Double Q training loop (off-policy) ─
            while not done:
                action = agent.select_action(state)
                next_state, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated

                agent.update(state, action, reward, next_state, done)

                state = next_state
                total_reward += reward

        # ── Record episode metrics ─────────────────────────────
        summary = env.get_episode_summary()
        history['episode_rewards'].append(total_reward)
        history['episode_profits'].append(summary.get('total_profit', 0))
        history['episode_stockout_rates'].append(
            summary.get('stockout_rate', 0))
        history['episode_holding_costs'].append(
            summary.get('total_holding_cost', 0))
        history['episode_order_frequencies'].append(
            summary.get('order_frequency', 0))
        history['episode_avg_inventories'].append(
            summary.get('avg_inventory', 0))

        if hasattr(agent, 'epsilon'):
            history['epsilons'].append(agent.epsilon)

        # ── Periodic evaluation ────────────────────────────────
        if (episode + 1) % eval_interval == 0:
            eval_reward = evaluate_agent_quick(agent, env, eval_episodes)
            history['eval_rewards'].append(eval_reward)
            history['eval_episodes'].append(episode + 1)

            if verbose:
                eps_str = (f" | eps: {agent.epsilon:.4f}"
                           if hasattr(agent, 'epsilon') else "")
                print(f"  Episode {episode+1:5d}/{n_episodes} | "
                      f"Train: {total_reward:7.1f} | "
                      f"Eval: {eval_reward:7.1f}{eps_str}")

    return history


def evaluate_agent_quick(agent, env, n_episodes=30):
    """
    Quick evaluation with epsilon=0 during training.

    Uses fixed seeds offset from training to avoid overlap.

    Args:
        agent: Agent to evaluate.
        env: InventoryEnv instance.
        n_episodes (int): Number of evaluation episodes.

    Returns:
        float: Mean total reward across evaluation episodes.
    """
    agent.set_eval_mode()
    total_rewards = []

    for ep in range(n_episodes):
        state, _ = env.reset(seed=ep + 50000)  # Offset from training
        total_reward = 0.0
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            state = next_state
            total_reward += reward

        total_rewards.append(total_reward)

    agent.set_train_mode()
    return float(np.mean(total_rewards))


def create_agent(agent_name, agent_cfg, n_states, n_actions, seed):
    """
    Factory function to create an agent by name.

    Args:
        agent_name (str): One of 'q_learning', 'sarsa', 'double_q_learning'.
        agent_cfg (dict): Hyperparameter dictionary from configs.yaml.
        n_states (int): Total state space size.
        n_actions (int): Number of actions.
        seed (int): Random seed.

    Returns:
        Agent instance.
    """
    common_args = dict(
        n_states=n_states,
        n_actions=n_actions,
        alpha=agent_cfg['alpha'],
        gamma=agent_cfg['gamma'],
        epsilon_start=agent_cfg['epsilon_start'],
        epsilon_end=agent_cfg['epsilon_end'],
        epsilon_decay=agent_cfg['epsilon_decay'],
        seed=seed,
    )

    if agent_name == 'q_learning':
        return QLearningAgent(**common_args)
    elif agent_name == 'sarsa':
        return SARSAAgent(**common_args)
    elif agent_name == 'double_q_learning':
        return DoubleQLearningAgent(**common_args)
    else:
        raise ValueError(f"Unknown agent: {agent_name}")


def run_training(config=None, output_dir=None, n_episodes_override=None):
    """
    Run the full training pipeline for all RL agents.

    For each agent type, trains over multiple seeds and saves:
        - Q-tables (results/<agent>/seed_<i>.npz)
        - Training history (results/<agent>_history.json)

    Args:
        config: Configuration dict. If None, loads from configs.yaml.
        output_dir (str, optional): Custom output directory for results.
            Defaults to 'results/' in project root.
        n_episodes_override (int, optional): Override n_episodes from config.
    """
    if config is None:
        config = load_config()

    training_cfg = config['training']
    n_episodes = n_episodes_override or training_cfg['n_episodes']
    n_seeds = training_cfg['n_seeds']
    eval_interval = training_cfg['eval_interval']
    eval_episodes = training_cfg.get('eval_episodes', 30)

    # Output directory for saved models and histories
    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'results'
        )
    os.makedirs(output_dir, exist_ok=True)

    # Get state/action space sizes from environment
    env = InventoryEnv(regime_transitions=True)
    n_states = env.N_STATES
    n_actions = env.N_ACTIONS

    print(f"State space: {n_states} states, Action space: {n_actions} actions")
    print(f"Training: {n_episodes} episodes x {n_seeds} seeds")
    print(f"Evaluation every {eval_interval} episodes "
          f"({eval_episodes} eval episodes)")
    print(f"Output directory: {output_dir}")

    # ═══════════════════════════════════════════════════════════
    # Train each agent type
    # ═══════════════════════════════════════════════════════════
    agent_names = ['q_learning', 'sarsa', 'double_q_learning']

    all_results = {}

    for agent_name in agent_names:
        agent_cfg = config['agents'][agent_name]

        print(f"\n{'='*60}")
        print(f"  Training: {agent_name.upper()}")
        print(f"  alpha={agent_cfg['alpha']}, gamma={agent_cfg['gamma']}, "
              f"eps: {agent_cfg['epsilon_start']}->{agent_cfg['epsilon_end']}")
        print(f"{'='*60}")

        seed_histories = []

        for seed in range(n_seeds):
            print(f"\n  -- Seed {seed+1}/{n_seeds} --")

            # Fresh environment per seed
            env = InventoryEnv(regime_transitions=True)

            # Create agent
            agent = create_agent(agent_name, agent_cfg,
                                 n_states, n_actions, seed)

            # Train
            history = train_agent(
                agent, env, n_episodes,
                eval_interval=eval_interval,
                eval_episodes=eval_episodes,
                verbose=True
            )
            seed_histories.append(history)

            # Save trained model
            if training_cfg.get('save_models', True):
                agent_dir = os.path.join(output_dir, agent_name)
                os.makedirs(agent_dir, exist_ok=True)
                agent.save(os.path.join(agent_dir, f'seed_{seed}.npz'))

        all_results[agent_name] = seed_histories

        # Save training history (JSON serializable)
        history_path = os.path.join(output_dir, f'{agent_name}_history.json')
        serializable = {}
        for i, h in enumerate(seed_histories):
            serializable[f'seed_{i}'] = {
                k: [float(v) for v in vals]
                for k, vals in h.items()
            }

        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2)

        print(f"\n  [OK] Saved {agent_name} results -> {output_dir}")

    # ═══════════════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("  TRAINING COMPLETE")
    print(f"{'='*60}")
    print(f"  Results directory: {output_dir}")
    for agent_name in agent_names:
        print(f"  * {agent_name}: {n_seeds} seeds trained")
    print(f"\n  Next step: python experiments/evaluate.py")

    return all_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Train RL agents for Inventory Management'
    )
    parser.add_argument(
        '--output-dir', type=str, default=None,
        help='Custom output directory for results (default: results/)'
    )
    parser.add_argument(
        '--episodes', type=int, default=None,
        help='Override number of training episodes (default: from configs.yaml)'
    )
    args = parser.parse_args()

    # Resolve output_dir to absolute path relative to project root
    out_dir = None
    if args.output_dir:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        out_dir = os.path.join(project_root, args.output_dir)

    run_training(output_dir=out_dir, n_episodes_override=args.episodes)

