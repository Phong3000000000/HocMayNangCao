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
    py -m streamlit run dashboard/app.py

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
# ─── Unified color palette ─────────────────────────────────
COLOR_PRIMARY = '#4F46E5'    # Indigo-600
COLOR_SUCCESS = '#059669'    # Emerald-600
COLOR_WARNING = '#D97706'    # Amber-600
COLOR_DANGER  = '#DC2626'    # Red-600
COLOR_INFO    = '#2563EB'    # Blue-600
COLOR_PURPLE  = '#7C3AED'    # Violet-600
COLOR_SLATE   = '#475569'    # Slate-600
COLOR_LIGHT   = '#F8FAFC'    # Slate-50

CHART_COLORS = {
    'inventory': COLOR_SUCCESS,
    'orders': COLOR_INFO,
    'demand': COLOR_WARNING,
    'stockout': COLOR_DANGER,
    'reward': COLOR_PRIMARY,
    'cumulative': COLOR_PURPLE,
}

AGENT_CHART_COLORS = [
    '#EF4444',  # Red-500
    '#F59E0B',  # Amber-500
    '#10B981',  # Emerald-500
    '#3B82F6',  # Blue-500
    '#6366F1',  # Indigo-500
    '#8B5CF6',  # Violet-500
]

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        padding: 0.8rem 0;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .main-subtitle {
        text-align: center;
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 0.9rem;
    }
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

@st.cache_resource
def load_trained_agent(agent_type, seed=0, results_dir=None):
    """Load a trained agent from saved Q-table."""
    if results_dir is None:
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


def get_agent(agent_type, env, results_dir=None):
    """Create or load an agent based on type."""
    if agent_type == 'Random':
        return RandomAgent(env.N_ACTIONS, seed=42), True
    elif agent_type == 'Always Order 2':
        return AlwaysOrder2Agent(), True
    elif agent_type == 'Reorder Threshold':
        return ReorderThresholdAgent(threshold=5, order_amount=5, env=env), True
    elif agent_type == 'Q-Learning':
        agent, loaded = load_trained_agent('q_learning', results_dir=results_dir)
        return agent, loaded
    elif agent_type == 'SARSA':
        agent, loaded = load_trained_agent('sarsa', results_dir=results_dir)
        return agent, loaded
    elif agent_type == 'Double Q-Learning':
        agent, loaded = load_trained_agent('double_q_learning', results_dir=results_dir)
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
    st.markdown('<div class="main-header">RL Inventory Management</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">'
        'Quan ly Ton kho bang Reinforcement Learning'
        '</div>',
        unsafe_allow_html=True
    )

    # ─── Sidebar Controls ─────────────────────────────────────
    with st.sidebar:
        st.header("Controls")

        agent_type = st.selectbox(
            "Select Agent",
            ['Random', 'Always Order 2', 'Reorder Threshold',
             'Q-Learning', 'SARSA', 'Double Q-Learning'],
            index=3  # Default to Q-Learning
        )

        # Training Budget selector
        results_100k_dir = os.path.join(PROJECT_ROOT, 'results_100k')
        budget_options = ['20,000 episodes']
        if os.path.isdir(results_100k_dir):
            budget_options.append('100,000 episodes')

        training_budget = st.selectbox(
            "Training Budget",
            budget_options,
            index=0,
            help="Select which trained model to use (20K or 100K episodes)"
        )

        # Determine results directory based on selection
        if training_budget == '100,000 episodes':
            selected_results_dir = results_100k_dir
        else:
            selected_results_dir = os.path.join(PROJECT_ROOT, 'results')

        weekend_surge = st.checkbox("Weekend Surge (unseen pattern)")
        surge_days = None
        if weekend_surge:
            selected_days = st.multiselect(
                "Select Surge Days",
                options=list(range(7)),
                default=[5, 6],
                format_func=lambda x: DAY_NAMES[x],
                help="Select days of the week when demand surge occurs"
            )
            surge_days = selected_days

        episode_seed = st.number_input("Episode Seed", 0, 999, 42)

        # Khởi tạo môi trường tạm thời để lấy xu hướng nhu cầu ban đầu dựa trên seed
        temp_env = InventoryEnv(
            regime_transitions=True,
            weekend_surge=weekend_surge,
            surge_days=surge_days
        )
        _, temp_info = temp_env.reset(seed=episode_seed)
        initial_regime_name = temp_info['demand_regime_name'].title()

        st.text_input(
            "Initial Demand Regime (from Seed)",
            value=initial_regime_name,
            disabled=True,
            help="The demand regime for Day 1, determined deterministically by the Episode Seed."
        )

        st.divider()
        st.markdown("### About")
        st.markdown("""
        **State**: (inventory, demand_regime, day, pending_order)
        - Inventory: 0-20 units
        - Demand: Low/Medium/High
        - Actions: Order 0-5 units
        - Episode: 30 days
        """)

    # ─── Load Agent ────────────────────────────────────────────
    env = InventoryEnv(
        regime_transitions=True,
        weekend_surge=weekend_surge,
        surge_days=surge_days
    )
    agent, is_loaded = get_agent(agent_type, env,
                                  results_dir=selected_results_dir)

    if agent is None:
        st.error("❌ Could not create agent.")
        return

    if agent_type in ['Q-Learning', 'SARSA', 'Double Q-Learning'] and not is_loaded:
        st.warning(
            f"No trained model found for {agent_type}. "
            f"Please run `py experiments/train.py` first. "
            f"Using untrained (random) Q-table."
        )

    # ─── Run Episode ───────────────────────────────────────────
    env_sim = InventoryEnv(
        regime_transitions=True,
        weekend_surge=weekend_surge,
        surge_days=surge_days
    )
    steps, summary = run_episode(agent, env_sim, seed=episode_seed)

    # ─── Tabs ──────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Episode Simulation",
        "Policy & Heatmap",
        "Learning Curves",
        "Agent Comparison",
        "Weekend Surge Test",
        "Budget Comparison (20K vs 100K)"
    ])

    # ═══════════════════════════════════════════════════════════
    # TAB 1: Episode Simulation
    # ═══════════════════════════════════════════════════════════
    with tab1:
        st.subheader(f"Episode Simulation -- {agent_type}")

        # Metric cards
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Profit", f"{summary['total_profit']:.1f}")
        with col2:
            st.metric("Avg Inventory", f"{summary['avg_inventory']:.1f}")
        with col3:
            st.metric("Stockout Rate",
                       f"{summary['stockout_rate']:.1%}")
        with col4:
            st.metric("Holding Cost",
                       f"{summary['total_holding_cost']:.1f}")
        with col5:
            st.metric("Order Frequency",
                       f"{summary['order_frequency']:.1%}")

        # Charts
        days = [s['day'] for s in steps]

        # Inventory chart
        fig_inv, ax_inv = plt.subplots(figsize=(12, 4))
        inventories = [s['inventory_after'] for s in steps]
        ax_inv.fill_between(days, inventories, alpha=0.2,
                            color=CHART_COLORS['inventory'])
        ax_inv.plot(days, inventories, 'o-',
                    color=CHART_COLORS['inventory'],
                    linewidth=2, markersize=4)
        ax_inv.axhline(y=5, color=COLOR_DANGER, linestyle='--',
                       alpha=0.5, label='Reorder point')
        ax_inv.set_xlabel('Day')
        ax_inv.set_ylabel('Inventory')
        ax_inv.set_title('Inventory Level Over Time')
        
        # Detail X and Y axes
        ax_inv.set_xticks(range(1, 31))
        ax_inv.set_yticks(range(0, max(inventories) + 2))
        ax_inv.tick_params(axis='both', labelsize=9)
        
        ax_inv.legend()
        ax_inv.grid(True, alpha=0.3)
        st.pyplot(fig_inv)
        plt.close(fig_inv)

        # Action + Demand charts
        col_a, col_b = st.columns(2)

        with col_a:
            fig_act, ax_act = plt.subplots(figsize=(10, 4))
            actions = [s['action'] for s in steps]
            ax_act.bar(days, actions, color=CHART_COLORS['orders'],
                       alpha=0.8, edgecolor='white')
            ax_act.set_xlabel('Day')
            ax_act.set_ylabel('Order Amount')
            ax_act.set_title('Daily Orders')
            
            # Detail X and Y axes
            ax_act.set_xticks(range(1, 31))
            ax_act.set_yticks(range(6))
            ax_act.tick_params(axis='both', labelsize=9)
            
            ax_act.grid(True, alpha=0.3)
            st.pyplot(fig_act)
            plt.close(fig_act)

        with col_b:
            fig_dem, ax_dem = plt.subplots(figsize=(10, 4))
            demands = [s['demand'] for s in steps]
            stockouts = [s['stockout'] for s in steps]
            ax_dem.bar(days, demands, color=CHART_COLORS['demand'],
                       alpha=0.7, label='Demand')
            ax_dem.bar(days, stockouts, color=CHART_COLORS['stockout'],
                       alpha=0.9, label='Stockout')
            ax_dem.set_xlabel('Day')
            ax_dem.set_ylabel('Units')
            ax_dem.set_title('Demand & Stockouts')
            
            # Detail X and Y axes
            ax_dem.set_xticks(range(1, 31))
            ax_dem.set_yticks(range(0, max(demands) + 2))
            ax_dem.tick_params(axis='both', labelsize=9)
            
            ax_dem.legend()
            ax_dem.grid(True, alpha=0.3)
            st.pyplot(fig_dem)
            plt.close(fig_dem)

        # Reward per day (instant reward) + Cumulative reward
        col_r1, col_r2 = st.columns(2)

        with col_r1:
            fig_rd, ax_rd = plt.subplots(figsize=(10, 4))
            rewards_daily = [s['reward'] for s in steps]
            bar_colors = [COLOR_SUCCESS if r >= 0 else COLOR_DANGER
                          for r in rewards_daily]
            ax_rd.bar(days, rewards_daily, color=bar_colors, alpha=0.8,
                      edgecolor='white')
            ax_rd.axhline(y=0, color=COLOR_SLATE, linestyle='-',
                          linewidth=0.8)
            ax_rd.set_xlabel('Day')
            ax_rd.set_ylabel('Reward')
            ax_rd.set_title('Daily Reward (Instant)')
            
            # Detail X and Y axes
            ax_rd.set_xticks(range(1, 31))
            min_r = int(np.floor(min(rewards_daily) / 10) * 10)
            max_r = int(np.ceil(max(rewards_daily) / 10) * 10)
            ax_rd.set_yticks(range(min_r, max_r + 1, 10))
            ax_rd.tick_params(axis='both', labelsize=9)
            
            ax_rd.grid(True, alpha=0.3)
            st.pyplot(fig_rd)
            plt.close(fig_rd)

        with col_r2:
            fig_rew, ax_rew = plt.subplots(figsize=(10, 4))
            cum_rewards = np.cumsum(rewards_daily)
            ax_rew.plot(days, cum_rewards, 'o-',
                        color=CHART_COLORS['cumulative'],
                        linewidth=2, markersize=4)
            ax_rew.fill_between(days, cum_rewards, alpha=0.15,
                                color=CHART_COLORS['cumulative'])
            ax_rew.set_xlabel('Day')
            ax_rew.set_ylabel('Cumulative Reward')
            ax_rew.set_title('Cumulative Reward')
            
            # Detail X and Y axes
            ax_rew.set_xticks(range(1, 31))
            min_cr = int(np.floor(min(cum_rewards) / 25) * 25)
            max_cr = int(np.ceil(max(cum_rewards) / 25) * 25)
            ax_rew.set_yticks(range(min_cr, max_cr + 1, 25))
            ax_rew.tick_params(axis='both', labelsize=9)
            
            ax_rew.grid(True, alpha=0.3)
            st.pyplot(fig_rew)
            plt.close(fig_rew)

        # Step-by-step table
        with st.expander("Step-by-Step Details", expanded=False):
            import pandas as pd
            df = pd.DataFrame(steps)
            st.dataframe(df, use_container_width=True, height=400)

    # ═══════════════════════════════════════════════════════════
    # TAB 2: Policy Table & Heatmap
    # ═══════════════════════════════════════════════════════════
    with tab2:
        st.subheader(f"Policy -- {agent_type}")

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
        im = ax_heat.imshow(policy_table, cmap='Blues', aspect='auto',
                            origin='lower', vmin=0, vmax=5)

        for inv in range(21):
            for pending in range(6):
                val = policy_table[inv, pending]
                color = 'white' if val >= 3 else '#1E293B'
                ax_heat.text(pending, inv, str(val),
                             ha='center', va='center',
                             fontsize=9, fontweight='bold', color=color)

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
        st.subheader("Learning Curves")
        st.caption(f"Showing results for: **{training_budget}**")

        results_dir = selected_results_dir
        agent_names = ['q_learning', 'sarsa', 'double_q_learning']
        colors = {
            'q_learning': '#3B82F6',
            'sarsa': '#6366F1',
            'double_q_learning': '#8B5CF6'
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

            # Smoothing (Adjusted window size for downsampled data)
            window = 20 if training_budget == '100,000 episodes' else 10
            if min_len > window:
                smoothed = np.array([
                    np.convolve(r, np.ones(window)/window, mode='valid')
                    for r in all_rewards
                ])
                mean_c = np.mean(smoothed, axis=0)
                std_c = np.std(smoothed, axis=0)
                
                # Scale X-axis to display correct episode numbers (factor of 50)
                budget_eps = 100000 if training_budget == '100,000 episodes' else 20000
                scale_factor = budget_eps / len(all_rewards[0])
                x = (np.arange(len(mean_c)) + window // 2) * scale_factor

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
                "No training history found. "
                "Run `py experiments/train.py` first."
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
                    budget_eps = 100000 if training_budget == '100,000 episodes' else 20000
                    scale_factor = budget_eps / len(epsilons)
                    eps_x = np.arange(len(epsilons)) * scale_factor

                    fig_eps, ax_eps = plt.subplots(figsize=(10, 3))
                    ax_eps.plot(eps_x, epsilons, color='#FF6B6B', linewidth=1.5)
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
        st.subheader("Agent Comparison")
        st.caption(f"Showing results for: **{training_budget}**")

        eval_path = os.path.join(selected_results_dir,
                                 'evaluation_results.json')

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
                bar_colors = AGENT_CHART_COLORS

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
                "No evaluation results found. Run:\n\n"
                "```bash\n"
                "py experiments/train.py\n"
                "py experiments/evaluate.py\n"
                "```"
            )

    # ═══════════════════════════════════════════════════════════
    # TAB 5: Weekend Surge Test (Dynamic Evaluation)
    # ═══════════════════════════════════════════════════════════
    with tab5:
        st.subheader("Weekend Surge Stress Test (Dynamic)")
        st.markdown(
            "Run real-time evaluation of all agents under a custom demand surge pattern. "
            "Select the surge days in the sidebar and configure test parameters below."
        )

        col_cfg1, col_cfg2 = st.columns(2)
        with col_cfg1:
            eval_episodes = st.slider("Number of Test Episodes", 10, 100, 30, help="Fewer episodes will evaluate faster.")
        with col_cfg2:
            eval_seeds = st.slider("Number of Seeds", 1, 10, 3, help="Fewer seeds will evaluate faster.")

        # Show warning if weekend_surge checkbox is off
        if not weekend_surge:
            st.warning("Please check 'Weekend Surge (unseen pattern)' in the sidebar to enable surge simulation.")
        elif surge_days is None or len(surge_days) == 0:
            st.warning("Please select at least one surge day in the sidebar to run the stress test.")
            
        run_btn = st.button("Run Live Stress Test", disabled=not weekend_surge or not surge_days)

        if run_btn:
            agents_list = ['Q-Learning', 'SARSA', 'Double Q-Learning']
            results_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            # Define evaluation environments
            env_normal = InventoryEnv(regime_transitions=True, weekend_surge=False)
            env_surge = InventoryEnv(regime_transitions=True, weekend_surge=True, surge_days=surge_days)
            
            surge_results = []
            
            # Helper fast evaluation function
            def eval_fast(agent_obj, env_obj, n_eps, n_sds):
                profits = []
                agent_obj.set_eval_mode()
                for sd in range(n_sds):
                    for ep in range(n_eps):
                        state, _ = env_obj.reset(seed=sd * 1000 + ep + 15000)
                        done = False
                        while not done:
                            action = agent_obj.select_action(state)
                            next_state, reward, terminated, truncated, info = env_obj.step(action)
                            done = terminated or truncated
                            state = next_state
                        profits.append(env_obj.get_episode_summary()['total_profit'])
                agent_obj.set_train_mode()
                return float(np.mean(profits))

            # Run loop
            total_steps = len(agents_list)
            for idx, name in enumerate(agents_list):
                results_placeholder.text(f"Evaluating agent: {name}...")
                
                # Load agent
                agent_obj, loaded = get_agent(name, env_normal, results_dir=selected_results_dir)
                
                # Normal evaluate
                normal_mean = eval_fast(agent_obj, env_normal, eval_episodes, eval_seeds)
                # Surge evaluate
                surge_mean = eval_fast(agent_obj, env_surge, eval_episodes, eval_seeds)
                
                diff_pct = ((surge_mean - normal_mean) / normal_mean * 100) if normal_mean > 0 else 0
                diff_sign = "+" if diff_pct >= 0 else ""
                
                surge_results.append({
                    'Agent': name,
                    'Normal Profit': normal_mean,
                    'Surge Profit': surge_mean,
                    'Profit Change (%)': f"{diff_sign}{diff_pct:.1f}%",
                    'diff_pct_val': diff_pct
                })
                
                progress_bar.progress((idx + 1) / total_steps)
            
            results_placeholder.empty()
            progress_bar.empty()
            
            # Render results
            st.success("Evaluation completed successfully!")
            
            import pandas as pd
            df_dyn = pd.DataFrame(surge_results)
            
            # Format columns for display
            df_disp = df_dyn.copy()
            df_disp['Normal Profit'] = df_disp['Normal Profit'].map(lambda x: f"{x:.1f}")
            df_disp['Surge Profit'] = df_disp['Surge Profit'].map(lambda x: f"{x:.1f}")
            
            st.dataframe(df_disp.drop(columns=['diff_pct_val']), use_container_width=True)
            
            # Create a bar chart comparing Normal Profit vs Surge Profit
            fig_dyn, ax_dyn = plt.subplots(figsize=(10, 5))
            
            x_indices = np.arange(len(surge_results))
            bar_width = 0.35

            normal_profits_vals = [row['Normal Profit'] for row in surge_results]
            surge_profits_vals = [row['Surge Profit'] for row in surge_results]
            agent_labels_list = [row['Agent'] for row in surge_results]

            rects1 = ax_dyn.bar(x_indices - bar_width/2, normal_profits_vals, bar_width, 
                                  label='Normal Demand', color='#3B82F6', alpha=0.8)
            rects2 = ax_dyn.bar(x_indices + bar_width/2, surge_profits_vals, bar_width, 
                                  label='Weekend Surge (Custom)', color='#FFA94D', alpha=0.9)

            ax_dyn.set_ylabel('Profit ($)')
            ax_dyn.set_title(f"Profit Comparison (Live Test: Surge on {[DAY_NAMES[d] for d in surge_days]})")
            ax_dyn.set_xticks(x_indices)
            ax_dyn.set_xticklabels(agent_labels_list)
            ax_dyn.legend()
            ax_dyn.grid(axis='y', alpha=0.3)

            # Add change percentage text labels
            for idx, rect in enumerate(rects2):
                height = rect.get_height()
                chg_text = surge_results[idx]['Profit Change (%)']
                ax_dyn.annotate(chg_text,
                                  xy=(rect.get_x() + rect.get_width() / 2, height),
                                  xytext=(0, 3),
                                  textcoords="offset points",
                                  ha='center', va='bottom', fontsize=9, fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig_dyn)
            plt.close(fig_dyn)

    # ═══════════════════════════════════════════════════════════
    # TAB 6: Budget Comparison (20K vs 100K Episodes)
    # ═══════════════════════════════════════════════════════════
    with tab6:
        st.subheader("Training Budget Comparison: 20,000 vs 100,000 Episodes")
        st.markdown(
            "Comparing the performance of RL agents trained with different training budgets. "
            "This highlights how algorithms benefit from more training data."
        )

        eval_20k_path = os.path.join(PROJECT_ROOT, 'results', 'evaluation_results.json')
        eval_100k_path = os.path.join(PROJECT_ROOT, 'results_100k', 'evaluation_results.json')

        if os.path.exists(eval_20k_path) and os.path.exists(eval_100k_path):
            with open(eval_20k_path, 'r') as f:
                eval_20k = json.load(f)
            with open(eval_100k_path, 'r') as f:
                eval_100k = json.load(f)

            all_keys = ['random', 'always_order_2', 'reorder_threshold', 'q_learning', 'sarsa', 'double_q_learning']
            display_names_local = {
                'random': 'Random',
                'always_order_2': 'Always Order 2',
                'reorder_threshold': 'Reorder Threshold',
                'q_learning': 'Q-Learning',
                'sarsa': 'SARSA',
                'double_q_learning': 'Double Q-Learning'
            }

            budget_data = []
            for k in all_keys:
                if k in eval_20k and k in eval_100k:
                    # Profit
                    p_20k = eval_20k[k].get('profits_mean', 0)
                    p_100k = eval_100k[k].get('profits_mean', 0)
                    p_diff = ((p_100k - p_20k) / p_20k * 100) if p_20k > 0 else 0
                    
                    # Stockout Rate
                    st_20k = eval_20k[k].get('stockout_rates_mean', 0)
                    st_100k = eval_100k[k].get('stockout_rates_mean', 0)
                    st_diff = ((st_100k - st_20k) / st_20k * 100) if st_20k > 0 else 0
                    
                    # Avg Inventory
                    inv_20k = eval_20k[k].get('avg_inventories_mean', 0)
                    inv_100k = eval_100k[k].get('avg_inventories_mean', 0)
                    inv_diff = ((inv_100k - inv_20k) / inv_20k * 100) if inv_20k > 0 else 0
                    
                    # Stockout Penalty
                    pen_20k = eval_20k[k].get('total_stockout_penalties_mean', 0)
                    pen_100k = eval_100k[k].get('total_stockout_penalties_mean', 0)
                    pen_diff = ((pen_100k - pen_20k) / pen_20k * 100) if pen_20k > 0 else 0

                    budget_data.append({
                        'Agent': display_names_local[k],
                        'Profit (20K)': p_20k,
                        'Profit (100K)': p_100k,
                        'Profit Change': p_diff,
                        'Stockout (20K)': st_20k,
                        'Stockout (100K)': st_100k,
                        'Stockout Change': st_diff,
                        'Avg Inv (20K)': inv_20k,
                        'Avg Inv (100K)': inv_100k,
                        'Inv Change': inv_diff,
                        'Penalty (20K)': pen_20k,
                        'Penalty (100K)': pen_100k,
                        'Penalty Change': pen_diff
                    })

            import pandas as pd
            df_budget = pd.DataFrame(budget_data)
            
            # Format display dataframe
            df_budget_disp = pd.DataFrame()
            df_budget_disp['Agent'] = df_budget['Agent']
            df_budget_disp['Profit (20K)'] = df_budget['Profit (20K)'].map(lambda x: f"{x:.1f}")
            df_budget_disp['Profit (100K)'] = df_budget['Profit (100K)'].map(lambda x: f"{x:.1f}")
            df_budget_disp['Profit Change'] = df_budget['Profit Change'].map(lambda x: "0.0%" if abs(x) < 1e-5 else (f"+{x:.1f}%" if x > 0 else f"{x:.1f}%"))
            
            df_budget_disp['Stockout Rate (20K)'] = df_budget['Stockout (20K)'].map(lambda x: f"{x:.3f}")
            df_budget_disp['Stockout Rate (100K)'] = df_budget['Stockout (100K)'].map(lambda x: f"{x:.3f}")
            df_budget_disp['Stockout Change'] = df_budget['Stockout Change'].map(lambda x: "0.0%" if abs(x) < 1e-5 else (f"+{x:.1f}%" if x > 0 else f"{x:.1f}%"))
            
            df_budget_disp['Avg Inv (20K)'] = df_budget['Avg Inv (20K)'].map(lambda x: f"{x:.2f}")
            df_budget_disp['Avg Inv (100K)'] = df_budget['Avg Inv (100K)'].map(lambda x: f"{x:.2f}")
            
            df_budget_disp['Penalty (20K)'] = df_budget['Penalty (20K)'].map(lambda x: f"{x:.1f}")
            df_budget_disp['Penalty (100K)'] = df_budget['Penalty (100K)'].map(lambda x: f"{x:.1f}")
            df_budget_disp['Penalty Change'] = df_budget['Penalty Change'].map(lambda x: "0.0%" if abs(x) < 1e-5 else (f"+{x:.1f}%" if x > 0 else f"{x:.1f}%"))

            st.dataframe(df_budget_disp, use_container_width=True)

            # Create 2x2 comparison charts
            fig_bud, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig_bud.suptitle('Performance Comparison: 20K vs. 100K Episodes', fontsize=16, fontweight='bold')

            # Biểu đồ configs
            chart_configs = [
                ('Profit ($)', 'Profit (20K)', 'Profit (100K)', 'Profit Change', axes[0][0], '#A5B4FC', '#4F46E5', 'higher'),
                ('Stockout Rate', 'Stockout (20K)', 'Stockout (100K)', 'Stockout Change', axes[0][1], '#FCA5A5', '#DC2626', 'lower'),
                ('Avg Inventory', 'Avg Inv (20K)', 'Avg Inv (100K)', 'Inv Change', axes[1][0], '#FDE047', '#CA8A04', 'lower'),
                ('Stockout Penalty ($)', 'Penalty (20K)', 'Penalty (100K)', 'Penalty Change', axes[1][1], '#FDBA74', '#EA580C', 'lower')
            ]

            x_indices = np.arange(len(budget_data))
            bar_width = 0.35
            labels = df_budget['Agent'].tolist()

            for title, key_20k, key_100k, key_chg, ax, color_20k, color_100k, direction in chart_configs:
                vals_20k = df_budget[key_20k].tolist()
                vals_100k = df_budget[key_100k].tolist()

                rects1 = ax.bar(x_indices - bar_width/2, vals_20k, bar_width, 
                                 label='20,000 Episodes', color=color_20k, alpha=0.8, edgecolor='white')
                rects2 = ax.bar(x_indices + bar_width/2, vals_100k, bar_width, 
                                 label='100,000 Episodes', color=color_100k, alpha=0.9, edgecolor='white')

                ax.set_ylabel(title, fontsize=11)
                ax.set_title(f'Comparison: {title}', fontsize=12, fontweight='bold')
                ax.set_xticks(x_indices)
                ax.set_xticklabels(labels, fontsize=9, rotation=15)
                ax.legend(fontsize=9)
                ax.grid(axis='y', alpha=0.3)

                # Add percentage change text labels on top of 100K bars
                for idx, rect in enumerate(rects2):
                    height = rect.get_height()
                    chg_val = df_budget.iloc[idx][key_chg]
                    
                    if abs(chg_val) < 1e-5:
                        chg_text = "0.0%"
                        text_color = '#475569'
                    else:
                        chg_text = f"+{chg_val:.1f}%" if chg_val > 0 else f"{chg_val:.1f}%"
                        # Highlight colors based on improvement direction (green for good, red for bad)
                        is_good = (chg_val > 0 and direction == 'higher') or (chg_val < 0 and direction == 'lower')
                        text_color = '#059669' if is_good else '#DC2626'
                    
                    ax.annotate(chg_text,
                               xy=(rect.get_x() + rect.get_width() / 2, height),
                               xytext=(0, 3),
                               textcoords="offset points",
                               ha='center', va='bottom', fontsize=9, fontweight='bold', color=text_color)

            plt.tight_layout()
            st.pyplot(fig_bud)
            plt.close(fig_bud)
        else:
            st.info("Ensure both standard results (results/) and 100k results (results_100k/) contain evaluation_results.json.")

if __name__ == '__main__':
    main()
