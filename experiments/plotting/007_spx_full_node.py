import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# SPX full node: 4 devices, 1 per APU, 6 XCDs each
data = {
    0: [3718782.807, 3623808.898, 3651245.425, 3651742.133, 2655243.138],
    1: [3729730.386, 3645397.552, 3629134.777, 3650769.540, 2762319.296],
    2: [3681459.443, 3617551.784, 3634785.967, 3644285.058, 2652160.645],
    3: [3740354.945, 3626100.436, 3650335.144, 3637515.474, 2679680.193],
}

dev_to_apu = {0: 'APU 0', 1: 'APU 1', 2: 'APU 2', 3: 'APU 3'}
apu_colors = ['#2196F3', '#FF9800', '#E91E63', '#4CAF50']

MB_TO_TB = 1e6
TB_TO_TIB = 1e12 / (2**40)
THEORETICAL_BW_TB = 5.3

# Ideal: 6× isolated 1-XCD baseline
baseline_1xcd = np.array([710919.819, 711137.930, 714967.461, 714965.925, 704574.931])
baseline_spx = baseline_1xcd * 6

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), gridspec_kw={'width_ratios': [3, 2, 2]})

# ── Left: per-device grouped bars ──
ax = axes[0]
x = np.arange(len(ops))
w = 0.18
for i, d in enumerate(range(4)):
    v = np.array(data[d]) / MB_TO_TB
    ax.bar(x + (i - 1.5) * w, v, w, color=apu_colors[i], edgecolor='white',
           linewidth=0.5, label=f'Dev {d} ({dev_to_apu[d]})', zorder=3)

ax.axhline(baseline_spx[3] / MB_TO_TB, color='red', linestyle='--', alpha=0.5,
           linewidth=1.2, label='Ideal (6×1-XCD)')
ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', alpha=0.4, linewidth=1.2,
           label='5.3 TB/s peak')

ax.set_xticks(x)
ax.set_xticklabels(ops, fontsize=12, fontweight='bold')
ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(2.4, 5.6)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=8, loc='upper left')
ax.set_title('Per-device bandwidth (6 XCDs each)', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

# ── Middle: efficiency vs ideal ──
ax = axes[1]
for i, d in enumerate(range(4)):
    pcts = np.array(data[d]) / baseline_spx * 100
    ax.plot(ops, pcts, '-o', color=apu_colors[i], markersize=7, linewidth=2,
            label=f'{dev_to_apu[d]}')

ax.axhline(100, color='red', linestyle='--', alpha=0.5, linewidth=1.2)
ax.set_ylabel('% of ideal (6× isolated 1-XCD)', fontsize=10)
ax.set_ylim(55, 105)
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=9)
ax.set_title('Efficiency vs. ideal', fontsize=13, fontweight='bold')

# ── Right: summary bar (Triad) with annotations ──
ax = axes[2]
triad_vals = [data[d][3] / MB_TO_TB for d in range(4)]
ideal_triad = baseline_spx[3] / MB_TO_TB
labels = [dev_to_apu[d] for d in range(4)]

bars = ax.bar(labels, triad_vals, color=apu_colors, edgecolor='white', linewidth=0.8,
              width=0.55, zorder=3)
ax.axhline(ideal_triad, color='black', linestyle='--', alpha=0.4, linewidth=1.2,
           label=f'Ideal: {ideal_triad:.2f} TB/s')
ax.axhline(THEORETICAL_BW_TB, color='red', linestyle=':', linewidth=1.5, alpha=0.6,
           label=f'Peak: {THEORETICAL_BW_TB} TB/s')

for bar, val in zip(bars, triad_vals):
    eff_ideal = val / ideal_triad * 100
    eff_peak = val / THEORETICAL_BW_TB * 100
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.06,
            f'{val:.2f} TB/s\n({eff_ideal:.0f}% ideal · {eff_peak:.0f}% peak)',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(0, THEORETICAL_BW_TB * 1.3)
ax.legend(fontsize=8.5, loc='upper right')
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.set_title('Triad per APU', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

fig.suptitle('MI300A SPX Mode — Full Node BabelStream (4 devices, 1 per APU, 6 XCDs each)',
             fontsize=14, fontweight='bold')
fig.text(0.5, 0.005,
         'BabelStream · double-precision · arraysize=2²⁸ · numtimes=1500 · '
         'SPX mode (6 XCDs/device) · "ideal" = 6× isolated 1-XCD baseline',
         ha='center', fontsize=9, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.04, 1, 0.93])
plt.savefig('/home/claude/spx_full_node.png', dpi=150, bbox_inches='tight')
print("Saved.")