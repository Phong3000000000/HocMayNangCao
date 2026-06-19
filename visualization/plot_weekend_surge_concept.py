import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    # Set up dark slide size: 16:9 aspect ratio
    fig, ax = plt.subplots(figsize=(10, 6.2), facecolor='#0F172A')
    ax.set_facecolor('#0F172A')
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    x = np.arange(len(days))
    
    # Define simulated daily demand values for illustration
    # Mon-Fri: normal Medium regime (mostly 2, 3, 4 units)
    # Sat-Sun: surged High regime (mostly 5, 6, 7, 8 units)
    np.random.seed(42)
    normal_demands = [3, 2, 4, 3, 4]  # Mon-Fri
    surge_demands = [7, 6]           # Sat-Sun
    
    # Plot background regime blocks
    # Mon-Fri: Medium (Regime 1)
    # Sat-Sun: High (Regime 2)
    ax.fill_between([0, 4], 0, 3, color='#38BDF8', alpha=0.1, label='Seen Regime (Medium)')
    ax.fill_between([4, 6], 0, 3, color='#F97316', alpha=0.12, label='Unseen Surge (High)')
    
    # Plot the transition boundary line
    ax.axvline(x=4, color='#64748B', linestyle='--', linewidth=1.8, alpha=0.7)
    ax.text(3.9, 8.2, "THỜI ĐIỂM BẮT ĐẦU CUỐI TUẦN\n(Weekend Starts)", 
            color='#94A3B8', fontsize=9.5, fontweight='bold', ha='right', va='center')
    
    # Plot simulated demand dots
    ax.scatter(x[:5], normal_demands, color='#38BDF8', s=150, zorder=5, edgecolor='#F8FAFC', linewidth=1.5, label='Nhu cầu ngày thường (Mon-Fri)')
    ax.scatter(x[5:], surge_demands, color='#F97316', s=180, zorder=5, edgecolor='#F8FAFC', linewidth=1.5, label='Nhu cầu tăng vọt cuối tuần (Sat-Sun)')
    
    # Draw step lines to show the "Regime Shift" concept
    regime_step_x = [0, 4, 4, 6]
    regime_step_y = [3.5, 3.5, 5.5, 5.5]  # Illustrative average demand levels
    ax.plot(regime_step_x, regime_step_y, color='#60A5FA', linewidth=3, linestyle='-', alpha=0.5, label='Xu hướng trung bình (Regime Trend)')
    
    # Add arrows and annotations showing the +1 Regime Shift
    ax.annotate('', xy=(5, 5.5), xytext=(5, 3.5),
                arrowprops=dict(arrowstyle="->", color='#F97316', lw=2.5, mutation_scale=15))
    ax.text(5.2, 4.5, "+1 Regime Shift\n(Low -> Med, Med -> High)", 
            color='#F97316', fontsize=10.5, fontweight='bold', ha='left', va='center')
    
    # Add text labels on the shaded areas
    ax.text(2, 1.5, "MÔ HÌNH ĐÃ HUẤN LUYỆN\n(SEEN PATTERN)\n\nAgent học cách cân đối giữa\nchi phí lưu kho & bán hàng\nở mức nhu cầu bình thường.", 
            color='#38BDF8', fontsize=11, fontweight='bold', ha='center', va='center')
    
    ax.text(5, 1.5, "THỬ THÁCH CHƯA TỪNG HỌC\n(UNSEEN PATTERN)\n\nKiểm tra khả năng thích ứng\nvà tính tổng quát hóa (generalization)\nkhi nhu cầu đột ngột tăng vọt.", 
            color='#F97316', fontsize=11, fontweight='bold', ha='center', va='center')
    
    # Set labels and ticks
    ax.set_xticks(x)
    ax.set_xticklabels(days, fontsize=12, color='#F8FAFC', fontweight='bold')
    
    ax.set_yticks([0, 2, 4, 6, 8, 10])
    ax.set_yticklabels(['0', '2', '4', '6', '8', '10+ khách'], fontsize=11, color='#F8FAFC')
    
    ax.set_ylabel('Số khách mua / Nhu cầu (Units)', fontsize=12, color='#F8FAFC', fontweight='bold', labelpad=10)
    ax.set_title('Mô Phỏng Thử Nghiệm Weekend Surge (Unseen Pattern Stress Test)', fontsize=14, color='#F8FAFC', fontweight='bold', pad=20)
    
    # Limits and grid
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(0, 9.5)
    ax.grid(axis='y', color='#334155', linestyle='-', linewidth=0.5, alpha=0.5)
    
    # Spine styling
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_color('#334155')
        
    ax.legend(loc='upper left', facecolor='#1E293B', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=9.5)
    
    plt.tight_layout()
    
    # Save
    os.makedirs('reports/figures', exist_ok=True)
    out_path = 'reports/figures/weekend_surge_concept.png'
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generalization concept plot saved to {out_path}")

if __name__ == '__main__':
    main()
