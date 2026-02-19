import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# Emulated TPX in CPX mode: 2 separate XCDs per APU (each device = 1 XCD)
emu_data = {
    'APU 0': {0: [711179.848, 711388.345, 715148.809, 715120.231, 701710.061],
              1: [710962.058, 711099.898, 714993.247, 714964.682, 703062.149]},
    'APU 1': {6: [711208.112, 711244.622, 715087.608, 715074.988, 703352.173],
              7: [711143.344, 711250.511, 715079.671, 715070.147, 702549.234]},
    'APU 2': {12: [710984.420, 711129.215, 715017.926, 714978.091, 702734.303],
              13: [711022.084, 711153.942, 715001.182, 715012.371, 703495.029]},
    'APU 3': {18: [711006.783, 711163.362, 715063.877, 715001.182, 703541.123],
              19: [710947.936, 711069.171, 714971.109, 714983.646, 702165.612]},
}

# Real TPX mode: 1 device per APU, each device = 2 XCDs
tpx_data = {
    'APU 0': [1417492.651, 1417909.604, 1428278.046, 1428261.898, 1364172.429],
    'APU 1': [1417675.126, 1417792.121, 1428572.271, 1428578.607, 1365239.156],
    'APU 2': [1417240.072, 1418007.444, 1428233.401, 1428221.052, 1365000.081],
    'APU 3': [1416380.106, 1417296.193, 1427676.672, 1427701.983, 1362510.622],
}

MB_TO_TB = 1e6
TB_TO_TIB = 1e12 / (2**40)

apu_names = ['APU 0', 'APU 1', 'APU 2', 'APU 3']
apu_colors = ['#2196F3', '#FF9800', '#E91E63', '#4CAF50']

# Compute emulated sums (sum of 2 XCDs per APU)
emu_sums = {}
for apu in apu_names:
    devs = list(emu_data[apu].values())
    emu_sums[apu] = np.array(devs[0]) + np.array(devs[1])

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), gridspec_kw={'width_ratios': [3, 2, 2]})

# ── Left: side-by-side bars per op (emu vs real) ──
ax = axes[0]
x = np.arange(len(ops))
w = 0.09

for i, apu in enumerate(apu_names):
    emu_tb = emu_sums[apu] / MB_TO_TB
    tpx_tb = np.array(tpx_data[apu]) / MB_TO_TB
    # Emulated: lighter, hatched
    ax.bar(x + (2*i - 3.5) * w, emu_tb, w, color=apu_colors[i], alpha=0.4,
           edgecolor=apu_colors[i], linewidth=1, hatch='///',
           label=f'{apu} CPX emu' if i == 0 else None, zorder=3)
    # Real TPX: solid
    ax.bar(x + (2*i - 2.5) * w, tpx_tb, w, color=apu_colors[i], alpha=0.9,
           edgecolor='white', linewidth=0.5,
           label=f'{apu} TPX real' if i == 0 else None, zorder=3)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='grey', alpha=0.4, hatch='///', edgecolor='grey', label='CPX emulated (2×1 XCD)'),
    Patch(facecolor='grey', alpha=0.9, edgecolor='white', label='TPX real (1×2 XCD)'),
]
ax.legend(handles=legend_elements, fontsize=9, loc='lower left')

ax.set_xticks(x)
ax.set_xticklabels(ops, fontsize=12, fontweight='bold')
ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(1.35, 1.44)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.set_title('Aggregate 2-XCD bandwidth per APU', fontsize=13, fontweight='bold')

ax2 = ax.twinx()
ymin, ymax = ax.get_ylim()
ax2.set_ylim(ymin * TB_TO_TIB, ymax * TB_TO_TIB)
ax2.set_ylabel('TiB/s', fontsize=11)

# ── Middle: ratio TPX/emulated ──
ax = axes[1]
for i, apu in enumerate(apu_names):
    ratio = np.array(tpx_data[apu]) / emu_sums[apu] * 100
    ax.plot(ops, ratio, '-o', color=apu_colors[i], markersize=7, linewidth=2, label=apu)

ax.axhline(100, color='black', linestyle='--', alpha=0.4, linewidth=1.2)
ax.set_ylabel('TPX real / CPX emulated (%)', fontsize=10)
ax.set_ylim(96, 101)
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=9)
ax.set_title('TPX vs emulated ratio', fontsize=13, fontweight='bold')

# ── Right: per-op comparison as grouped bars ──
ax = axes[2]
x = np.arange(len(apu_names))
w = 0.15

for j, op in enumerate(ops):
    emu_vals = [emu_sums[apu][j] / MB_TO_TB for apu in apu_names]
    tpx_vals = [tpx_data[apu][j] / MB_TO_TB for apu in apu_names]
    diff_pct = [(t - e) / e * 100 for t, e in zip(tpx_vals, emu_vals)]
    ax.bar(x + (j - 2) * w, diff_pct, w, label=op, zorder=3, alpha=0.85)

ax.axhline(0, color='black', linewidth=0.8, alpha=0.5)
ax.set_xticks(x)
ax.set_xticklabels(apu_names, fontsize=11)
ax.set_ylabel('Δ bandwidth (%)', fontsize=10)
ax.set_title('TPX gain over emulated', fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.legend(fontsize=8, ncol=3, loc='lower left')

fig.suptitle('MI300A — Real TPX (1×2-XCD device) vs Emulated TPX in CPX (2×1-XCD devices)',
             fontsize=14, fontweight='bold')
fig.text(0.5, 0.005,
         'BabelStream · double-precision · arraysize=2²⁸ · numtimes=1500 · '
         '1st TPX per APU · both configs use 2 XCDs per APU',
         ha='center', fontsize=9, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.04, 1, 0.93])
plt.savefig('/home/claude/cpx_vs_tpx.png', dpi=150, bbox_inches='tight')
print("Saved.")