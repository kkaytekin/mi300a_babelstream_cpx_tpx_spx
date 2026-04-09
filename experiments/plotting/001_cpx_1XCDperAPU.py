import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# 1 XCD per APU: devices 0, 6, 12, 18
dev_to_apu = {0: 'APU 0', 6: 'APU 1', 12: 'APU 2', 18: 'APU 3'}
data = {
    0:  [711013.374, 711170.074, 715014.276, 715002.373, 704411.948],
    6:  [710887.452, 711161.714, 714963.492, 714940.483, 704714.881],
    12: [710965.118, 711126.507, 714975.394, 714969.046, 704654.644],
    18: [710813.332, 711093.423, 714916.682, 714950.797, 704518.251],
}

apu_labels = ['APU 0\n(dev 0)', 'APU 1\n(dev 6)', 'APU 2\n(dev 12)', 'APU 3\n(dev 18)']
apu_colors = ['#2196F3', '#FF9800', '#E91E63', '#4CAF50']
devs = [0, 6, 12, 18]

THEORETICAL_BW_TB = 5.3
TB_TO_TIB = 1e12 / (2**40)
MB_TO_TB = 1e6

# Convert to TB/s
vals_tb = {d: np.array(data[d]) / MB_TO_TB for d in devs}

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), gridspec_kw={'width_ratios': [3, 2]})

# ── Left: grouped bars per operation ──
ax = axes[0]
x = np.arange(len(ops))
w = 0.18
for i, (d, color, label) in enumerate(zip(devs, apu_colors, apu_labels)):
    v = vals_tb[d]
    bars = ax.bar(x + (i - 1.5) * w, v, w, color=color, edgecolor='white',
                  linewidth=0.5, label=label.replace('\n', ' '), zorder=3)

ax.set_xticks(x)
ax.set_xticklabels(ops, fontsize=12, fontweight='bold')
ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(0.69, 0.72)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=9, ncol=4, loc='lower center')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

ax.set_title('Per-operation bandwidth (1 XCD each)', fontsize=13, fontweight='bold')

# ── Right: spread across APUs for each op ──
ax = axes[1]
for j, op in enumerate(ops):
    values = [vals_tb[d][j] for d in devs]
    mean_v = np.mean(values)
    spread = (max(values) - min(values)) / mean_v * 100
    ax.scatter([j]*4, values, c=apu_colors, s=60, zorder=3, edgecolors='white', linewidths=0.5)
    ax.hlines(mean_v, j - 0.25, j + 0.25, colors='black', linewidths=1, alpha=0.5)
    ax.annotate(f'±{spread:.2f}%', xy=(j, max(values)), xytext=(0, 8),
                textcoords='offset points', fontsize=8, ha='center', color='#555')

ax.set_xticks(range(len(ops)))
ax.set_xticklabels(ops, fontsize=12, fontweight='bold')
ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(0.69, 0.72)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.set_title('Cross-APU spread', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

fig.suptitle('MI300A CPX — BabelStream HBM Bandwidth: 1 XCD per APU',
             fontsize=14, fontweight='bold')

fig.text(0.5, 0.005,
         'BabelStream · double-precision · arraysize=2²⁸ · numtimes=1500 · 1 XCD per APU (devices 0, 6, 12, 18)',
         ha='center', fontsize=9, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.04, 1, 0.93])
plt.savefig('/home/claude/cpx_1xcd_per_apu.png', dpi=150, bbox_inches='tight')
print("Saved.")