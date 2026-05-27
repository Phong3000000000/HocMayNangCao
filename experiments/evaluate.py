"""
Evaluation Script for RL Inventory Management Agents.

Evaluates all agents (Random, Heuristic, Q-Learning, SARSA, Double Q-Learning)
on standard and unseen demand patterns. Reports mean ± std across seeds.

Usage:
    python experiments/evaluate.py

Output:
    results/evaluation_results.json — All evaluation metrics

Author: RL Inventory Management Team
"""

import os
import sys
import yaml
import numpy as np
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from envs.custom_env import InventoryEnv
from agents.q_learning import QLearningAgent
from agents.sarsa import SARSAAgent
from agents.double_q_learning import DoubleQLearningAgent
from agents.random_agent import RandomAgent
from agents.heuristic_agent import AlwaysOrder2Agent, ReorderThresholdAgent


def load_config(config_path=None):
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'configs.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def evaluate_agent(agent, env, n_episodes=100, seed_offset=0):
    """
    Evaluate an agent with epsilon=0 (greedy policy).

    Runs multiple episodes and collects comprehensive metrics.

    Args:
        agent: Agent to evaluate (must have select_action, set_eval_mode).
        env: InventoryEnv instance.
        n_episodes (int): Number of evaluation episodes.
        seed_offset (int): Seed offset to avoid overlap with training.

    Returns:
        results (dict): Metrics with mean ± std values.
        episode_histories (list): Detailed step-by-step history per episode.
    """
    agent.set_eval_mode()

    metrics = {
        'profits': [],
        'stockout_rates': [],
        'holding_costs': [],
        'order_frequencies': [],
        'avg_inventories': [],
        'total_revenues': [],
        'total_stockout_penalties': [],
        'episode_lengths': [],
        'total_stockout_units': [],
        'total_ordered': [],
    }

    episode_histories = []

    for ep in range(n_episodes):
        state, _ = env.reset(seed=ep + seed_offset)
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            state = next_state

        summary = env.get_episode_summary()
        metrics['profits'].append(summary['total_profit'])
        metrics['stockout_rates'].append(summary['stockout_rate'])
        metrics['holding_costs'].append(summary['total_holding_cost'])
        metrics['order_frequencies'].append(summary['order_frequency'])
        metrics['avg_inventories'].append(summary['avg_inventory'])
        metrics['total_revenues'].append(summary['total_revenue'])
        metrics['total_stockout_penalties'].append(
            summary['total_stockout_penalty'])
        metrics['episode_lengths'].append(summary['episode_length'])
        metrics['total_stockout_units'].append(
            summary['total_stockout_units'])
        metrics['total_ordered'].append(summary['total_ordered'])
        episode_histories.append(env.episode_history.copy())

    # Compute mean ± std for all metrics
    results = {}
    for key, values in metrics.items():
        results[f'{key}_mean'] = float(np.mean(values))
        results[f'{key}_std'] = float(np.std(values))

    # Store raw values for later analysis
    results['raw_metrics'] = {
        k: [float(v) for v in vals]
        for k, vals in metrics.items()
    }

    agent.set_train_mode()
    return results, episode_histories


def _print_results(name, results):
    """Print formatted evaluation results for a single agent."""
    print(f"  {'Metric':<22s}  {'Mean':>8s}  {'+-Std':>8s}")
    print(f"  {'-'*22}  {'-'*8}  {'-'*8}")
    print(f"  {'Profit':<22s}  "
          f"{results.get('profits_mean', 0):8.2f}  "
          f"+- {results.get('profits_std', 0):6.2f}")
    print(f"  {'Stockout Rate':<22s}  "
          f"{results.get('stockout_rates_mean', 0):8.4f}  "
          f"+- {results.get('stockout_rates_std', 0):6.4f}")
    print(f"  {'Holding Cost':<22s}  "
          f"{results.get('holding_costs_mean', 0):8.2f}  "
          f"+- {results.get('holding_costs_std', 0):6.2f}")
    print(f"  {'Order Frequency':<22s}  "
          f"{results.get('order_frequencies_mean', 0):8.4f}  "
          f"+- {results.get('order_frequencies_std', 0):6.4f}")
    print(f"  {'Avg Inventory':<22s}  "
          f"{results.get('avg_inventories_mean', 0):8.2f}  "
          f"+- {results.get('avg_inventories_std', 0):6.2f}")
    print(f"  {'Revenue':<22s}  "
          f"{results.get('total_revenues_mean', 0):8.2f}  "
          f"+- {results.get('total_revenues_std', 0):6.2f}")
    print(f"  {'Stockout Penalty':<22s}  "
          f"{results.get('total_stockout_penalties_mean', 0):8.2f}  "
          f"+- {results.get('total_stockout_penalties_std', 0):6.2f}")


def _average_seed_results(seed_results):
    """Average evaluation results across multiple seeds."""
    avg = {}
    keys = [k for k in seed_results[0].keys()
            if k.endswith('_mean') or k.endswith('_std')]

    for key in keys:
        values = [r[key] for r in seed_results if key in r]
        if values:
            avg[key] = float(np.mean(values))

    return avg


def run_evaluation(config=None):
    """
    Run the full evaluation pipeline.

    Steps:
        1. Evaluate baselines (Random, AlwaysOrder2, ReorderThreshold)
        2. Evaluate trained RL agents (Q-Learning, SARSA, Double Q)
        3. Evaluate RL agents on unseen demand patterns (weekend surge)
        4. Save all results to JSON
    """
    if config is None:
        config = load_config()

    eval_cfg = config['evaluation']
    n_eval_episodes = eval_cfg['n_episodes']
    n_seeds = config['training']['n_seeds']

    results_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'results'
    )
    os.makedirs(results_dir, exist_ok=True)

    env = InventoryEnv(regime_transitions=True)
    n_states = env.N_STATES
    n_actions = env.N_ACTIONS

    all_results = {}

    # ═══════════════════════════════════════════════════════════
    # 1. Evaluate Baseline Agents
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("  EVALUATING BASELINE AGENTS")
    print(f"{'='*60}")

    baseline_agents = {
        'random': RandomAgent(n_actions, seed=42),
        'always_order_2': AlwaysOrder2Agent(),
        'reorder_threshold': ReorderThresholdAgent(
            threshold=5, order_amount=5, env=env
        ),
    }

    for name, agent in baseline_agents.items():
        print(f"\n  > {agent.name}")
        env_eval = InventoryEnv(regime_transitions=True)
        results, _ = evaluate_agent(
            agent, env_eval, n_eval_episodes,
            seed_offset=eval_cfg.get('seed_offset', 10000)
        )
        all_results[name] = results
        _print_results(name, results)

    # ═══════════════════════════════════════════════════════════
    # 2. Evaluate Trained RL Agents
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("  EVALUATING TRAINED RL AGENTS")
    print(f"{'='*60}")

    rl_agents = {
        'q_learning': (QLearningAgent, config['agents']['q_learning']),
        'sarsa': (SARSAAgent, config['agents']['sarsa']),
        'double_q_learning': (DoubleQLearningAgent,
                              config['agents']['double_q_learning']),
    }

    for agent_name, (AgentClass, agent_cfg) in rl_agents.items():
        print(f"\n  > {agent_name}")
        seed_results = []

        for seed in range(n_seeds):
            model_path = os.path.join(
                results_dir, agent_name, f'seed_{seed}.npz'
            )

            if not os.path.exists(model_path):
                print(f"    Seed {seed}: Model not found, skipping.")
                continue

            agent = AgentClass(
                n_states=n_states,
                n_actions=n_actions,
                alpha=agent_cfg['alpha'],
                gamma=agent_cfg['gamma'],
                seed=seed
            )
            agent.load(model_path)

            env_eval = InventoryEnv(regime_transitions=True)
            results, _ = evaluate_agent(
                agent, env_eval, n_eval_episodes,
                seed_offset=seed * 1000 + eval_cfg.get('seed_offset', 10000)
            )
            seed_results.append(results)

        if seed_results:
            avg_results = _average_seed_results(seed_results)
            all_results[agent_name] = avg_results
            _print_results(agent_name, avg_results)
        else:
            print(f"    No trained models found for {agent_name}.")

    # ═══════════════════════════════════════════════════════════
    # 3. Evaluate on Unseen Demand Patterns (Weekend Surge)
    # ═══════════════════════════════════════════════════════════
    if eval_cfg.get('test_weekend_surge', True):
        print(f"\n{'='*60}")
        print("  EVALUATING ON UNSEEN PATTERN: WEEKEND SURGE")
        print(f"{'='*60}")

        for agent_name, (AgentClass, agent_cfg) in rl_agents.items():
            print(f"\n  > {agent_name} (Weekend Surge)")

            model_path = os.path.join(
                results_dir, agent_name, 'seed_0.npz'
            )
            if not os.path.exists(model_path):
                print(f"    Model not found, skipping.")
                continue

            agent = AgentClass(
                n_states=n_states,
                n_actions=n_actions,
                alpha=agent_cfg['alpha'],
                gamma=agent_cfg['gamma'],
                seed=0
            )
            agent.load(model_path)

            # Test with weekend_surge=True (unseen during training)
            env_surge = InventoryEnv(
                regime_transitions=True, weekend_surge=True
            )
            results, _ = evaluate_agent(
                agent, env_surge, n_eval_episodes,
                seed_offset=eval_cfg.get('seed_offset', 10000)
            )
            all_results[f'{agent_name}_weekend_surge'] = results
            _print_results(f'{agent_name} (Weekend Surge)', results)

    # ═══════════════════════════════════════════════════════════
    # 4. Save All Results
    # ═══════════════════════════════════════════════════════════
    eval_path = os.path.join(results_dir, 'evaluation_results.json')

    # Remove raw_metrics for JSON (too large)
    serializable = {}
    for name, res in all_results.items():
        serializable[name] = {
            k: v for k, v in res.items()
            if k != 'raw_metrics'
        }

    with open(eval_path, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, indent=2)

    print(f"\n{'='*60}")
    print(f"  EVALUATION COMPLETE")
    print(f"  Results saved -> {eval_path}")
    print(f"{'='*60}")

    return all_results


if __name__ == '__main__':
    run_evaluation()
