"""
Streamlit Dashboard for RL Inventory Management Demo.

Features:
    - Select demand regime (Low / Medium / High)
    - Select agent (Random, Heuristic, Q-Learning, SARSA, Double Q-Learning)
    - Inventory level chart over time
    - Daily order actions chart
    - Policy Table (inventory → recommended order)
    - Policy Heatmap
    - Learning curves
    - Real-time episode simulation with state/action/reward display

Usage:
    streamlit run dashboard/app.py

Author: RL Inventory Management Team
"""

import os
import sys
import json
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from envs.custom_env import InventoryEnv, DEMAND_REGIMES, DAY_NAMES
from agents.random_agent import RandomAgent
from agents.heuristic_agent import AlwaysOrder2Agent, ReorderThresholdAgent
from agents.q_learning import QLearningAgent
from agents.sarsa import SARSAAgent
from agents.double_q_learning import DoubleQLearningAgent


# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RL Inventory Management",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3748;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        margin-top: 0.3rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

@st.cache_resource
def load_trained_agent(agent_type, seed=0):
    """Load a trained agent from saved Q-table."""
    results_dir = os.path.join(PROJECT_ROOT, 'results')
    env = InventoryEnv()
    n_states = env.N_STATES
    n_actions = env.N_ACTIONS

    if agent_type == 'q_learning':
        agent = QLearningAgent(n_states, n_actions)
        model_path = os.path.join(results_dir, 'q_learning', f'seed_{seed}.npz')
    elif agent_type == 'sarsa':
        agent = SARSAAgent(n_states, n_actions)
        model_path = os.path.join(results_dir, 'sarsa', f'seed_{seed}.npz')
    elif agent_type == 'double_q_learning':
        agent = DoubleQLearningAgent(n_states, n_actions)
        model_path = os.path.join(results_dir, 'double_q_learning',
                                  f'seed_{seed}.npz')
    else:
        return None, False

    if os.path.exists(model_path):
        agent.load(model_path)
        return agent, True
    return agent, False


def get_agent(agent_type, env):
    """Create or load an agent based on type."""
    if agent_type == 'Random':
        return RandomAgent(env.N_ACTIONS, seed=42), True
    elif agent_type == 'Always Order 2':
        return AlwaysOrder2Agent(), True
    elif agent_type == 'Reorder Threshold':
        return ReorderThresholdAgent(threshold=5, order_amount=5, env=env), True
    elif agent_type == 'Q-Learning':
        agent, loaded = load_trained_agent('q_learning')
        return agent, loaded
    elif agent_type == 'SARSA':
        agent, loaded = load_trained_agent('sarsa')
        return agent, loaded
    elif agent_type == 'Double Q-Learning':
        agent, loaded = load_trained_agent('double_q_learning')
        return agent, loaded
    return None, False


def run_episode(agent, env, seed=42):
    """Run a single episode and collect step data."""
    state, info = env.reset(seed=seed)
    agent.set_eval_mode()

    steps = []
    done = False

    while not done:
        inv, regime, dow, pending = env.state_decoder(state)
        action = agent.select_action(state)
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

        steps.append({
            'day': info['day'],
            'inventory_before': inv + pending,  # After receiving pending
            'action': action,
            'demand': info['demand'],
            'sold': info['sold'],
            'stockout': info['stockout'],
            'inventory_after': info['inventory_after'],
            'reward': reward,
            'revenue': info['revenue'],
            'purchase_cost': info['purchase_cost'],
            'holding_cost': info['holding_cost'],
            'stockout_penalty': info['stockout_penalty'],
            'regime': DEMAND_REGIMES[info['demand_regime']],
            'day_name': DAY_NAMES[(dow + 1) % 7],  # day_of_week after step
        })

        state = next_state

    agent.set_train_mode()
    return steps, env.get_episode_summary()


def build_policy_table(agent, env, regime=1, dow=0):
    """
    Build the policy table: for each (inventory, pending_order),
    show the recommended order amount.

    Returns a 2D numpy array: rows=inventory (0–20), cols=pending (0–5).
    """
    if hasattr(agent, 'get_policy'):
        policy = agent.get_policy()
    elif hasattr(agent, 'Q'):
        policy = np.argmax(agent.Q, axis=1)
    else:
        # Heuristic agents: simulate
        table = np.zeros((env.N_INVENTORY, env.N_PENDING), dtype=int)
        for inv in range(env.N_INVENTORY):
            for pending in range(env.N_PENDING):
                state_idx = env.state_encoder((inv, regime, dow, pending))
                table[inv, pending] = agent.select_action(state_idx)
        return table

    table = np.zeros((env.N_INVENTORY, env.N_PENDING), dtype=int)
    for inv in range(env.N_INVENTORY):
        for pending in range(env.N_PENDING):
            state_idx = env.state_encoder((inv, regime, dow, pending))
            table[inv, pending] = policy[state_idx]

    return table


# ═══════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════

def main():
    # ─── Header ────────────────────────────────────────────────
    st.markdown('<div class="main-header">📦 RL Inventory Management</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center; color:#718096; font-size:1.1rem;">'
        'Quản lý Tồn kho bằng Reinforcement Learning — Dashboard Demo'
        '</p>',
        unsafe_allow_html=True
    )

    # ─── Sidebar Controls ─────────────────────────────────────
    with st.sidebar:
        st.header("⚙️ Controls")

        agent_type = st.selectbox(
            "🤖 Select Agent",
            ['Random', 'Always Order 2', 'Reorder Threshold',
             'Q-Learning', 'SARSA', 'Double Q-Learning'],
            index=3  # Default to Q-Learning
        )

        demand_regime = st.selectbox(
            "📊 Demand Regime",
            ['Low', 'Medium', 'High'],
            index=1
        )
        regime_id = {'Low': 0, 'Medium': 1, 'High': 2}[demand_regime]

        weekend_surge = st.checkbox("🌊 Weekend Surge (unseen pattern)")
        episode_seed = st.number_input("🎲 Episode Seed", 0, 999, 42)

        st.divider()
        st.markdown("### 📋 About")
        st.markdown("""
        **State**: (inventory, demand_regime, day, pending_order)
        - Inventory: 0–20 units
        - Demand: Low/Medium/High
        - Actions: Order 0–5 units
        - Episode: 30 days
        """)

    # ─── Load Agent ────────────────────────────────────────────
    env = InventoryEnv(
        regime_transitions=True,
        weekend_surge=weekend_surge
    )
    agent, is_loaded = get_agent(agent_type, env)

    if agent is None:
        st.error("❌ Could not create agent.")
        return

    if agent_type in ['Q-Learning', 'SARSA', 'Double Q-Learning'] and not is_loaded:
        st.warning(
            f"⚠️ No trained model found for {agent_type}. "
            f"Please run `python experiments/train.py` first.\n\n"
            f"Using untrained (random) Q-table."
        )

    # ─── Run Episode ───────────────────────────────────────────
    # Override regime in env
    env_sim = InventoryEnv(
        regime_transitions=True,
        weekend_surge=weekend_surge
    )
    steps, summary = run_episode(agent, env_sim, seed=episode_seed)

    # ─── Tabs ──────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Episode Simulation",
        "📊 Policy Table & Heatmap",
        "📉 Learning Curves",
        "🏆 Agent Comparison"
    ])

    # ═══════════════════════════════════════════════════════════
    # TAB 1: Episode Simulation
    # ═══════════════════════════════════════════════════════════
    with tab1:
        st.subheader(f"Episode Simulation — {agent_type}")

        # Metric cards
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("💰 Total Profit", f"{summary['total_profit']:.1f}")
        with col2:
            st.metric("📦 Avg Inventory", f"{summary['avg_inventory']:.1f}")
        with col3:
            st.metric("🚫 Stockout Rate",
                       f"{summary['stockout_rate']:.1%}")
        with col4:
            st.metric("🏷️ Holding Cost",
                       f"{summary['total_holding_cost']:.1f}")
        with col5:
            st.metric("🛒 Order Frequency",
                       f"{summary['order_frequency']:.1%}")

        # Charts
        days = [s['day'] for s in steps]

        # Inventory chart
        fig_inv, ax_inv = plt.subplots(figsize=(12, 4))
        inventories = [s['inventory_after'] for s in steps]
        ax_inv.fill_between(days, inventories, alpha=0.3, color='#51CF66')
        ax_inv.plot(days, inventories, 'o-', color='#2B8A3E',
                    linewidth=2, markersize=5)
        ax_inv.axhline(y=5, color='red', linestyle='--', alpha=0.5,
                       label='Reorder point')
        ax_inv.set_xlabel('Day')
        ax_inv.set_ylabel('Inventory')
        ax_inv.set_title('📦 Inventory Level Over Time')
        ax_inv.legend()
        ax_inv.grid(True, alpha=0.3)
        st.pyplot(fig_inv)
        plt.close(fig_inv)

        # Action chart
        col_a, col_b = st.columns(2)

        with col_a:
            fig_act, ax_act = plt.subplots(figsize=(10, 4))
            actions = [s['action'] for s in steps]
            ax_act.bar(days, actions, color='#339AF0', alpha=0.8,
                       edgecolor='white')
            ax_act.set_xlabel('Day')
            ax_act.set_ylabel('Order Amount')
            ax_act.set_title('🛒 Daily Orders')
            ax_act.set_yticks(range(6))
            ax_act.grid(True, alpha=0.3)
            st.pyplot(fig_act)
            plt.close(fig_act)

        with col_b:
            fig_dem, ax_dem = plt.subplots(figsize=(10, 4))
            demands = [s['demand'] for s in steps]
            stockouts = [s['stockout'] for s in steps]
            ax_dem.bar(days, demands, color='#FFA94D', alpha=0.7,
                       label='Demand')
            ax_dem.bar(days, stockouts, color='#FF6B6B', alpha=0.9,
                       label='Stockout')
            ax_dem.set_xlabel('Day')
            ax_dem.set_ylabel('Units')
            ax_dem.set_title('📊 Demand & Stockouts')
            ax_dem.legend()
            ax_dem.grid(True, alpha=0.3)
            st.pyplot(fig_dem)
            plt.close(fig_dem)

        # Cumulative reward
        fig_rew, ax_rew = plt.subplots(figsize=(12, 4))
        cum_rewards = np.cumsum([s['reward'] for s in steps])
        ax_rew.plot(days, cum_rewards, 'o-', color='#845EF7',
                    linewidth=2, markersize=5)
        ax_rew.fill_between(days, cum_rewards, alpha=0.2, color='#845EF7')
        ax_rew.set_xlabel('Day')
        ax_rew.set_ylabel('Cumulative Reward')
        ax_rew.set_title('💰 Cumulative Reward Over Episode')
        ax_rew.grid(True, alpha=0.3)
        st.pyplot(fig_rew)
        plt.close(fig_rew)

        # Step-by-step table
        with st.expander("📋 Step-by-Step Details", expanded=False):
            import pandas as pd
            df = pd.DataFrame(steps)
            st.dataframe(df, use_container_width=True, height=400)

    # ═══════════════════════════════════════════════════════════
    # TAB 2: Policy Table & Heatmap
    # ═══════════════════════════════════════════════════════════
    with tab2:
        st.subheader(f"Policy — {agent_type}")

        pol_col1, pol_col2 = st.columns([1, 2])

        with pol_col1:
            st.markdown("#### Settings")
            pol_regime = st.selectbox(
                "Demand Regime for Policy",
                ['Low', 'Medium', 'High'],
                index=1,
                key='pol_regime'
            )
            pol_regime_id = {'Low': 0, 'Medium': 1, 'High': 2}[pol_regime]

            pol_dow = st.selectbox(
                "Day of Week",
                list(range(7)),
                format_func=lambda x: DAY_NAMES[x],
                key='pol_dow'
            )

        # Build policy table
        policy_table = build_policy_table(
            agent, env, regime=pol_regime_id, dow=pol_dow
        )

        with pol_col2:
            st.markdown("#### Policy Table")
            st.markdown(
                "*Rows = Inventory level (0–20), "
                "Columns = Pending order (0–5), "
                "Values = Recommended order amount*"
            )

            import pandas as pd
            df_policy = pd.DataFrame(
                policy_table,
                index=[f"Inv={i}" for i in range(21)],
                columns=[f"Pend={p}" for p in range(6)]
            )
            st.dataframe(df_policy, use_container_width=True, height=500)

        # Policy Heatmap
        st.markdown("#### Policy Heatmap")
        fig_heat, ax_heat = plt.subplots(figsize=(10, 12))
        im = ax_heat.imshow(policy_table, cmap='YlOrRd', aspect='auto',
                            origin='lower', vmin=0, vmax=5)

        for inv in range(21):
            for pending in range(6):
                color = 'white' if policy_table[inv, pending] >= 3 else 'black'
                ax_heat.text(pending, inv,
                             str(policy_table[inv, pending]),
                             ha='center', va='center',
                             fontsize=9, color=color)

        ax_heat.set_xlabel('Pending Order', fontsize=12)
        ax_heat.set_ylabel('Inventory Level', fontsize=12)
        ax_heat.set_title(
            f'Policy: {agent_type} | '
            f'Regime: {pol_regime} | Day: {DAY_NAMES[pol_dow]}',
            fontsize=14, fontweight='bold'
        )
        ax_heat.set_xticks(range(6))
        ax_heat.set_yticks(range(21))

        cbar = plt.colorbar(im, ax=ax_heat, label='Order Amount')
        cbar.set_ticks(range(6))

        plt.tight_layout()
        st.pyplot(fig_heat)
        plt.close(fig_heat)

    # ═══════════════════════════════════════════════════════════
    # TAB 3: Learning Curves
    # ═══════════════════════════════════════════════════════════
    with tab3:
        st.subheader("📉 Learning Curves")

        results_dir = os.path.join(PROJECT_ROOT, 'results')
        agent_names = ['q_learning', 'sarsa', 'double_q_learning']
        colors = {
            'q_learning': '#51CF66',
            'sarsa': '#339AF0',
            'double_q_learning': '#845EF7'
        }
        display_names = {
            'q_learning': 'Q-Learning',
            'sarsa': 'SARSA',
            'double_q_learning': 'Double Q-Learning'
        }

        has_any = False
        fig_lc, ax_lc = plt.subplots(figsize=(14, 6))

        for aname in agent_names:
            history_path = os.path.join(
                results_dir, f'{aname}_history.json'
            )
            if not os.path.exists(history_path):
                continue
            has_any = True

            with open(history_path, 'r') as f:
                histories = json.load(f)

            # Collect rewards across seeds
            all_rewards = []
            for seed_key, seed_data in histories.items():
                rewards = seed_data.get('episode_rewards', [])
                if rewards:
                    all_rewards.append(rewards)

            if not all_rewards:
                continue

            min_len = min(len(r) for r in all_rewards)
            all_rewards = np.array([r[:min_len] for r in all_rewards])

            # Smoothing
            window = 50
            if min_len > window:
                smoothed = np.array([
                    np.convolve(r, np.ones(window)/window, mode='valid')
                    for r in all_rewards
                ])
                mean_c = np.mean(smoothed, axis=0)
                std_c = np.std(smoothed, axis=0)
                x = np.arange(len(mean_c)) + window // 2

                color = colors.get(aname, '#999')
                label = display_names.get(aname, aname)
                ax_lc.plot(x, mean_c, color=color, linewidth=2, label=label)
                ax_lc.fill_between(x, mean_c - std_c, mean_c + std_c,
                                   alpha=0.15, color=color)

        if has_any:
            ax_lc.set_xlabel('Episode', fontsize=12)
            ax_lc.set_ylabel('Total Reward', fontsize=12)
            ax_lc.set_title('Learning Curves (Mean ± Std across Seeds)',
                            fontsize=14, fontweight='bold')
            ax_lc.legend(fontsize=12)
            ax_lc.grid(True, alpha=0.3)
            st.pyplot(fig_lc)
            plt.close(fig_lc)
        else:
            st.info(
                "📭 No training history found. "
                "Run `python experiments/train.py` first."
            )
            plt.close(fig_lc)

        # Epsilon schedule
        st.markdown("#### Epsilon Decay Schedule")
        for aname in agent_names:
            history_path = os.path.join(
                results_dir, f'{aname}_history.json'
            )
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    histories = json.load(f)
                first_seed = list(histories.keys())[0]
                epsilons = histories[first_seed].get('epsilons', [])
                if epsilons:
                    fig_eps, ax_eps = plt.subplots(figsize=(10, 3))
                    ax_eps.plot(epsilons, color='#FF6B6B', linewidth=1.5)
                    ax_eps.axhline(y=0.05, color='gray', linestyle='--',
                                   alpha=0.5, label='ε_min')
                    ax_eps.set_xlabel('Episode')
                    ax_eps.set_ylabel('Epsilon (ε)')
                    ax_eps.set_title(f'Epsilon Schedule — '
                                     f'{display_names.get(aname, aname)}')
                    ax_eps.legend()
                    ax_eps.grid(True, alpha=0.3)
                    st.pyplot(fig_eps)
                    plt.close(fig_eps)
                    break

    # ═══════════════════════════════════════════════════════════
    # TAB 4: Agent Comparison
    # ═══════════════════════════════════════════════════════════
    with tab4:
        st.subheader("🏆 Agent Comparison")

        eval_path = os.path.join(results_dir, 'evaluation_results.json')

        if os.path.exists(eval_path):
            with open(eval_path, 'r') as f:
                eval_results = json.load(f)

            # Filter out weekend surge for main comparison
            main_agents = {k: v for k, v in eval_results.items()
                           if 'weekend_surge' not in k}

            if main_agents:
                import pandas as pd

                # Build comparison dataframe
                comp_data = []
                for aname, metrics in main_agents.items():
                    comp_data.append({
                        'Agent': aname.replace('_', ' ').title(),
                        'Profit': f"{metrics.get('profits_mean', 0):.1f} "
                                  f"± {metrics.get('profits_std', 0):.1f}",
                        'Stockout Rate': f"{metrics.get('stockout_rates_mean', 0):.3f}",
                        'Holding Cost': f"{metrics.get('holding_costs_mean', 0):.1f}",
                        'Avg Inventory': f"{metrics.get('avg_inventories_mean', 0):.1f}",
                        'Order Freq': f"{metrics.get('order_frequencies_mean', 0):.3f}",
                    })

                df_comp = pd.DataFrame(comp_data)
                st.dataframe(df_comp, use_container_width=True)

                # Bar charts
                agent_labels = list(main_agents.keys())
                display_labels = [a.replace('_', ' ').title()
                                  for a in agent_labels]
                bar_colors = ['#FF6B6B', '#FFA94D', '#FFD93D',
                              '#51CF66', '#339AF0', '#845EF7']

                fig_comp, axes = plt.subplots(2, 2, figsize=(14, 10))
                fig_comp.suptitle('Agent Comparison — Key Metrics',
                                  fontsize=16, fontweight='bold')

                metric_configs = [
                    ('profits_mean', 'profits_std', 'Profit ↑'),
                    ('stockout_rates_mean', 'stockout_rates_std',
                     'Stockout Rate ↓'),
                    ('holding_costs_mean', 'holding_costs_std',
                     'Holding Cost ↓'),
                    ('avg_inventories_mean', 'avg_inventories_std',
                     'Avg Inventory'),
                ]

                for idx, (mean_key, std_key, title) in enumerate(
                        metric_configs):
                    ax = axes[idx // 2][idx % 2]
                    vals = [main_agents[a].get(mean_key, 0)
                            for a in agent_labels]
                    errs = [main_agents[a].get(std_key, 0)
                            for a in agent_labels]
                    colors_list = bar_colors[:len(agent_labels)]

                    ax.bar(display_labels, vals, yerr=errs, capsize=5,
                           color=colors_list, alpha=0.8, edgecolor='white')
                    ax.set_title(title, fontsize=13)
                    ax.tick_params(axis='x', rotation=30)
                    ax.grid(axis='y', alpha=0.3)

                plt.tight_layout()
                st.pyplot(fig_comp)
                plt.close(fig_comp)
        else:
            st.info(
                "📭 No evaluation results found. Run:\n\n"
                "```bash\n"
                "python experiments/train.py\n"
                "python experiments/evaluate.py\n"
                "```"
            )


if __name__ == '__main__':
    main()
