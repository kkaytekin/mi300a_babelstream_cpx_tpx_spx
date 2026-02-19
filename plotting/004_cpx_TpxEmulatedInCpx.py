import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# 2 XCDs per APU — emulating 1st TPX of each APU in CPX mode
data = {
    0:  [711179.848, 711388.345, 715148.809, 715120.231, 701710.061],
    1:  [710962.058, 711099.898, 714993.247, 714964.682, 703062.149],
    6:  [711208.112, 711244.622, 715087.608, 715074.988, 703352.173],
    7:  [711143.344, 711250.511, 715079.671, 715070.147, 702549.234],
    12: [710984.420, 711129.215, 715017.926, 714978.091, 702734.303],
    13: [711022.084, 711153.942, 715001.182, 715012.371, 703495.029],
    18: [711006.783, 711163.362, 715063.877, 715001.182, 703541.123],
    19: [710947.936, 711069.171, 714971.109, 714983.646, 702165.612],
}

baseline_1xcd = np.array([710919.819, 711137.930, 714967.461, 714965.925, 704574.931])

MB_TO_TB = 1e6
TB_TO_TIB = 1e12 / (2**40)
THEORETICAL_BW_TB = 5.3

apu_map = {
    'APU 0': [0, 1], 'APU 1': [6, 7], 'APU 2': [12, 13], 'APU 3': [18, 19]
}
apu_colors = {'APU 0': '#2196F3', 'APU 1': '#FF9800', 'APU 2': '#E91E63', 'APU 3': '#4CAF50'}

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), gridspec_kw={'width_ratios': [3, 2, 2]})

# ── Left: per-device bars ──
ax = axes[0]
all_devs = [0, 1, 6, 7, 12, 13, 18, 19]
dev_colors = []
for d in all_devs:
    for apu, devs in apu_map.items():
        if d in devs:
            dev_colors.append(apu_colors[apu])

x = np.arange(len(ops))
w = 0.09
for i, d in enumerate(all_devs):
    v = np.array(data[d]) / MB_TO_TB
    apu_name = [a for a, ds in apu_map.items() if d in ds][0]
    ax.bar(x + (i - 3.5) * w, v, w, color=dev_colors[i], edgecolor='white',
           linewidth=0.5, label=f'Dev {d} ({apu_name})', zorder=3, alpha=0.85)

for j in range(len(ops)):
    ax.hlines(baseline_1xcd[j] / MB_TO_TB, x[j] - 4*w, x[j] + 4*w,
              colors='red', linewidths=1, linestyles='--', alpha=0.5, zorder=4)

ax.set_xticks(x)
ax.set_xticklabels(ops, fontsize=12, fontweight='bold')
ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(0.698, 0.718)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
# Simplified legend: just APU colors
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=a) for a, c in apu_colors.items()]
legend_elements.append(plt.Line2D([0], [0], color='red', linestyle='--', alpha=0.5, label='1-XCD isolated'))
ax.legend(handles=legend_elements, fontsize=8, ncol=5, loc='lower left')
ax.set_title('Per-XCD bandwidth (2 per APU)', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

# ── Middle: cross-APU spread ──
ax = axes[1]
for j, op in enumerate(ops):
    values = [np.array(data[d][j]) / MB_TO_TB for d in all_devs]
    mean_v = np.mean(values)
    spread = (max(values) - min(values)) / mean_v * 100
    for i, d in enumerate(all_devs):
        ax.scatter(j, values[i], c=dev_colors[i], s=50, zorder=3,
                   edgecolors='white', linewidths=0.5)
    ax.hlines(mean_v, j - 0.3, j + 0.3, colors='black', linewidths=1, alpha=0.4)
    ax.annotate(f'±{spread:.3f}%', xy=(j, max(values)), xytext=(0, 8),
                textcoords='offset points', fontsize=8, ha='center', color='#555')

ax.set_xticks(range(len(ops)))
ax.set_xticklabels(ops, fontsize=12, fontweight='bold')
ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(0.698, 0.718)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.set_title('Cross-device spread', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

# ── Right: cumulative per APU ──
ax = axes[2]
for apu, devs in apu_map.items():
    cum = np.zeros(5)
    cum_vals = []
    for d in devs:
        cum = cum + np.array(data[d])
        cum_vals.append(cum.copy())
    cum_arr = np.array(cum_vals) / MB_TO_TB
    # Triad
    ax.plot(range(1, len(devs)+1), cum_arr[:, 3], '-o', color=apu_colors[apu],
            markersize=6, linewidth=2.2, label=f'{apu} Triad')
    ax.annotate(f'{cum_arr[-1, 3]:.3f}', xy=(len(devs), cum_arr[-1, 3]),
                xytext=(6, 0), textcoords='offset points',
                fontsize=9, fontweight='bold', color=apu_colors[apu], va='center')

ideal = np.array([baseline_1xcd[3] * (i+1) / MB_TO_TB for i in range(2)])
ax.plot(range(1, 3), ideal, 'k--', alpha=0.3, linewidth=1.5, label='Ideal')

ax.set_xlabel('XCDs (cumulative per APU)', fontsize=10)
ax.set_ylabel('TB/s', fontsize=11)
ax.set_xticks([1, 2])
ax.set_xlim(0.5, 3.2)
ax.set_ylim(0, 1.6)
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=8, loc='upper left')
ax.set_title('Cumulative Triad per APU', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

fig.suptitle('MI300A CPX — Emulated TPX: 2 XCDs per APU (1st TPX of each)',
             fontsize=14, fontweight='bold')
fig.text(0.5, 0.005,
         'BabelStream · double-precision · arraysize=2²⁸ · numtimes=1500 · '
         'devices {0,1}, {6,7}, {12,13}, {18,19} · red dashes = 1-XCD isolated baseline',
         ha='center', fontsize=9, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.04, 1, 0.93])
plt.savefig('/home/claude/cpx_emulated_tpx.png', dpi=150, bbox_inches='tight')
print("Saved.")