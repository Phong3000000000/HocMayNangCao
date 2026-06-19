import os
import numpy as np
import matplotlib.pyplot as plt

# Define transition matrix matching custom_env.py
transition_matrix = np.array([
    [0.90, 0.08, 0.02],  # Low -> Low, Medium, High
    [0.05, 0.85, 0.10],  # Medium -> Low, Medium, High
    [0.02, 0.08, 0.90]   # High -> Low, Medium, High
])

regimes = ['Low', 'Medium', 'High']

def main():
    fig, ax = plt.subplots(figsize=(8, 6.5))
    
    # Plot heatmap
    im = ax.imshow(transition_matrix * 100, cmap='Blues', vmin=0, vmax=100)
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.set_ylabel("Transition Probability (%)", rotation=-90, va="bottom", fontsize=11)
    
    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(regimes)))
    ax.set_yticks(np.arange(len(regimes)))
    ax.set_xticklabels(regimes, fontsize=11, fontweight='bold')
    ax.set_yticklabels(regimes, fontsize=11, fontweight='bold')
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(regimes)):
        for j in range(len(regimes)):
            val = transition_matrix[i, j] * 100
            # Change text color depending on cell background darkness
            color = "white" if val > 50 else "#1E293B"
            ax.text(j, i, f"{val:.0f}%",
                    ha="center", va="center", 
                    color=color, fontsize=14, fontweight='bold')
            
    ax.set_title("Layer 1: Demand Regime Transition Matrix (Markov Chain)", fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel("Today's Regime (Hôm nay)", fontsize=12, fontweight='bold', labelpad=10)
    ax.set_xlabel("Tomorrow's Regime (Ngày mai)", fontsize=12, fontweight='bold', labelpad=10)
    
    plt.tight_layout()
    
    # Save directory
    os.makedirs('reports/figures', exist_ok=True)
    out_path = 'reports/figures/regime_transition_matrix.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved transition matrix plot to {out_path}")

if __name__ == '__main__':
    main()
