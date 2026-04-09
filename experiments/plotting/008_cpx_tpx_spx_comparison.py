import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# ── CPX full node: 24 devices, 6 per APU, 1 XCD each ──
cpx_data = {
    0:  [710977.123, 711208.936, 715038.956, 715058.083, 703535.246],
    1:  [710774.630, 711013.610, 714934.294, 714953.257, 675442.288],
    2:  [667300.873, 667864.316, 672170.274, 664503.617, 548469.394],
    3:  [680968.212, 710592.474, 714611.455, 714632.144, 611420.583],
    4:  [597211.522, 592109.389, 616826.774, 617955.654, 365684.991],
    5:  [587868.263, 580458.797, 634746.431, 647405.469, 398209.157],
    6:  [673211.571, 674153.087, 672192.015, 676825.298, 551175.006],
    7:  [710727.583, 711059.518, 714908.828, 714925.567, 702008.150],
    8:  [673435.352, 673898.164, 672726.870, 674582.980, 555529.481],
    9:  [589938.619, 571959.787, 649292.500, 664077.640, 406499.931],
    10: [591443.231, 596761.857, 645144.813, 624374.622, 388401.554],
    11: [711066.463, 711078.236, 714970.792, 714973.965, 695388.446],
    12: [710712.412, 711020.554, 714894.548, 714986.582, 681944.558],
    13: [677363.994, 674256.698, 683109.880, 648300.604, 442232.905],
    14: [658202.475, 677694.253, 658966.808, 639624.193, 437408.888],
    15: [675890.844, 674653.975, 660034.912, 689410.367, 491744.277],
    16: [709503.018, 710111.837, 714162.377, 714133.878, 600776.063],
    17: [709453.795, 710227.032, 714207.425, 714366.606, 660565.217],
    18: [617022.878, 614589.609, 643386.559, 633122.711, 392554.630],
    19: [709809.057, 710363.177, 714377.775, 714404.709, 654739.788],
    20: [676650.069, 674022.957, 684640.092, 707392.696, 588882.324],
    21: [622232.590, 597045.568, 654173.286, 676840.231, 406604.991],
    22: [709682.388, 710198.847, 714330.962, 714350.051, 659069.984],
    23: [701466.868, 706936.158, 678025.548, 683555.554, 568183.956],
}
cpx_apu_map = {0: list(range(0,6)), 1: list(range(6,12)), 2: list(range(12,18)), 3: list(range(18,24))}

# ── TPX full node: 12 devices, 3 per APU, 2 XCDs each ──
tpx_data = {
    0:  [1341471.750, 1358507.388, 1359284.728, 1366840.203, 1175886.691],
    1:  [1290910.388, 1309791.059, 1350511.059, 1360561.872, 1171195.541],
    2:  [1417377.108, 1418411.115, 1427905.451, 1427965.585, 1376952.649],
    3:  [1413137.540, 1416629.108, 1425482.160, 1426144.825, 1370646.901],
    4:  [1416007.934, 1416988.517, 1428082.702, 1428190.657, 1353494.183],
    5:  [1335735.279, 1329878.810, 1340571.387, 1335419.501, 1133566.954],
    6:  [1414631.617, 1416250.734, 1426792.306, 1426871.307, 1279896.706],
    7:  [1416138.195, 1416923.072, 1427981.410, 1428102.013, 1351960.829],
    8:  [1315890.718, 1334705.432, 1328956.927, 1315158.983, 1080797.813],
    9:  [1314251.892, 1324293.932, 1318108.077, 1334655.938, 1141287.195],
    10: [1416381.507, 1417475.342, 1427807.349, 1427930.770, 1356799.765],
    11: [1414534.243, 1416128.857, 1425264.562, 1426514.291, 1269189.372],
}
tpx_apu_map = {0: [0,1,2], 1: [3,4,5], 2: [6,7,8], 3: [9,10,11]}

# ── SPX full node: 4 devices, 1 per APU, 6 XCDs each ──
spx_data = {
    0: [3718782.807, 3623808.898, 3651245.425, 3651742.133, 2655243.138],
    1: [3729730.386, 3645397.552, 3629134.777, 3650769.540, 2762319.296],
    2: [3681459.443, 3617551.784, 3634785.967, 3644285.058, 2652160.645],
    3: [3740354.945, 3626100.436, 3650335.144, 3637515.474, 2679680.193],
}
spx_apu_map = {0: [0], 1: [1], 2: [2], 3: [3]}

MB_TO_TB = 1e6
TB_TO_TIB = 1e12 / (2**40)
THEO_APU = 5.3       # TB/s per APU
THEO_NODE = THEO_APU * 4  # 21.2 TB/s

triad_idx = 3
dot_idx = 4

def apu_totals(data_dict, apu_map):
    out = {}
    for a in range(4):
        s = np.zeros(5)
        for d in apu_map[a]:
            s += np.array(data_dict[d])
        out[a] = s
    return out

def node_total(data_dict):
    s = np.zeros(5)
    for d in data_dict:
        s += np.array(data_dict[d])
    return s

cpx_apu = apu_totals(cpx_data, cpx_apu_map)
tpx_apu = apu_totals(tpx_data, tpx_apu_map)
spx_apu = apu_totals(spx_data, spx_apu_map)

cpx_node = node_total(cpx_data) / MB_TO_TB
tpx_node = node_total(tpx_data) / MB_TO_TB
spx_node = node_total(spx_data) / MB_TO_TB

mode_colors = {'CPX': '#2196F3', 'TPX': '#FF9800', 'SPX': '#E91E63'}

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.38, wspace=0.3)

# ═══ Row 1: Whole-node ═══

# Row 1, col 1: whole-node per-op
ax = fig.add_subplot(gs[0, 0])
x = np.arange(len(ops))
w = 0.25
for i, (mode, vals) in enumerate([('CPX', cpx_node), ('TPX', tpx_node), ('SPX', spx_node)]):
    ax.bar(x + (i-1)*w, vals, w, color=mode_colors[mode], edgecolor='white',
           linewidth=0.5, label=mode, zorder=3)
ax.axhline(THEO_NODE, color='red', linestyle=':', alpha=0.5, linewidth=1.2,
           label=f'Node peak: {THEO_NODE:.1f} TB/s')
ax.set_xticks(x)
ax.set_xticklabels(ops, fontsize=11, fontweight='bold')
ax.set_ylabel('TB/s', fontsize=11)
ax.set_title('Whole-node bandwidth', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.set_ylim(0, THEO_NODE * 1.15)
ax2 = ax.twinx(); ymin, ymax = ax.get_ylim(); ax2.set_ylim(ymin*TB_TO_TIB, ymax*TB_TO_TIB); ax2.set_ylabel('TiB/s')

# Row 1, col 2: whole-node % of theoretical peak
ax = fig.add_subplot(gs[0, 1])
for mode, vals in [('CPX', cpx_node), ('TPX', tpx_node), ('SPX', spx_node)]:
    pcts = vals / THEO_NODE * 100
    ax.plot(ops, pcts, '-o', color=mode_colors[mode], markersize=8, linewidth=2.5, label=mode)
ax.axhline(100, color='red', linestyle=':', alpha=0.4, linewidth=1.2)
ax.set_ylabel('% of theoretical peak', fontsize=10)
ax.set_ylim(45, 105)
ax.set_title('Whole-node % of peak', fontsize=13, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(alpha=0.2)
ax.set_axisbelow(True)

# Row 1, col 3: Triad summary bars
ax = fig.add_subplot(gs[0, 2])
modes = ['CPX', 'TPX', 'SPX']
triad_vals = [cpx_node[triad_idx], tpx_node[triad_idx], spx_node[triad_idx]]
bars = ax.bar(modes, triad_vals, color=[mode_colors[m] for m in modes],
              edgecolor='white', linewidth=0.8, width=0.55, zorder=3)
ax.axhline(THEO_NODE, color='red', linestyle=':', alpha=0.5, linewidth=1.2,
           label=f'Peak: {THEO_NODE:.1f} TB/s')

for bar, val in zip(bars, triad_vals):
    pct = val / THEO_NODE * 100
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.2,
            f'{val:.1f} TB/s\n({pct:.0f}% peak)',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylabel('TB/s', fontsize=11)
ax.set_ylim(0, THEO_NODE * 1.15)
ax.set_title('Triad: whole-node', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax2 = ax.twinx(); ymin, ymax = ax.get_ylim(); ax2.set_ylim(ymin*TB_TO_TIB, ymax*TB_TO_TIB); ax2.set_ylabel('TiB/s')

# ═══ Row 2: Per-APU ═══

# Row 2, col 1: per-APU Triad bars
ax = fig.add_subplot(gs[1, 0])
x = np.arange(4)
w = 0.25
for i, (mode, apu_dict) in enumerate([('CPX', cpx_apu), ('TPX', tpx_apu), ('SPX', spx_apu)]):
    vals = [apu_dict[a][triad_idx] / MB_TO_TB for a in range(4)]
    ax.bar(x + (i-1)*w, vals, w, color=mode_colors[mode], edgecolor='white',
           linewidth=0.5, label=mode, zorder=3)

ax.axhline(THEO_APU, color='red', linestyle=':', alpha=0.5, linewidth=1.2,
           label=f'APU peak: {THEO_APU} TB/s')
ax.set_xticks(x)
ax.set_xticklabels([f'APU {a}' for a in range(4)], fontsize=11)
ax.set_ylabel('TB/s', fontsize=11)
ax.set_title('Triad per APU', fontsize=13, fontweight='bold')
ax.legend(fontsize=8)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)
ax.set_ylim(0, THEO_APU * 1.15)
ax2 = ax.twinx(); ymin, ymax = ax.get_ylim(); ax2.set_ylim(ymin*TB_TO_TIB, ymax*TB_TO_TIB); ax2.set_ylabel('TiB/s')

# Row 2, col 2: per-APU Triad % of peak
ax = fig.add_subplot(gs[1, 1])
for i, (mode, apu_dict) in enumerate([('CPX', cpx_apu), ('TPX', tpx_apu), ('SPX', spx_apu)]):
    pcts = [apu_dict[a][triad_idx] / MB_TO_TB / THEO_APU * 100 for a in range(4)]
    ax.bar(np.arange(4) + (i-1)*w, pcts, w, color=mode_colors[mode],
           edgecolor='white', linewidth=0.5, label=mode, zorder=3)

ax.axhline(100, color='red', linestyle=':', alpha=0.4, linewidth=1.2)
ax.set_xticks(range(4))
ax.set_xticklabels([f'APU {a}' for a in range(4)], fontsize=11)
ax.set_ylabel('% of APU peak (5.3 TB/s)', fontsize=10)
ax.set_ylim(60, 105)
ax.set_title('Triad % of peak per APU', fontsize=13, fontweight='bold')
ax.legend(fontsize=8)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)

# Row 2, col 3: Dot % of peak per APU
ax = fig.add_subplot(gs[1, 2])
for i, (mode, apu_dict) in enumerate([('CPX', cpx_apu), ('TPX', tpx_apu), ('SPX', spx_apu)]):
    pcts = [apu_dict[a][dot_idx] / MB_TO_TB / THEO_APU * 100 for a in range(4)]
    ax.bar(np.arange(4) + (i-1)*w, pcts, w, color=mode_colors[mode],
           edgecolor='white', linewidth=0.5, label=mode, zorder=3)

ax.axhline(100, color='red', linestyle=':', alpha=0.4, linewidth=1.2)
ax.set_xticks(range(4))
ax.set_xticklabels([f'APU {a}' for a in range(4)], fontsize=11)
ax.set_ylabel('% of APU peak (5.3 TB/s)', fontsize=10)
ax.set_ylim(40, 105)
ax.set_title('Dot % of peak per APU', fontsize=13, fontweight='bold')
ax.legend(fontsize=8)
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)

# ═══ Row 3: Device distributions + summary ═══

# Row 3, col 1: Triad device distribution
ax = fig.add_subplot(gs[2, 0])
cpx_triad_devs = [cpx_data[d][triad_idx] / MB_TO_TB for d in cpx_data]
tpx_triad_devs = [tpx_data[d][triad_idx] / MB_TO_TB for d in tpx_data]
spx_triad_devs = [spx_data[d][triad_idx] / MB_TO_TB for d in spx_data]

bp = ax.boxplot([cpx_triad_devs, tpx_triad_devs, spx_triad_devs],
                tick_labels=['CPX\n(24 dev)', 'TPX\n(12 dev)', 'SPX\n(4 dev)'],
                patch_artist=True, widths=0.5)
for patch, color in zip(bp['boxes'], [mode_colors[m] for m in modes]):
    patch.set_facecolor(color); patch.set_alpha(0.6)

for i, (devs, color) in enumerate([(cpx_triad_devs, mode_colors['CPX']),
                                     (tpx_triad_devs, mode_colors['TPX']),
                                     (spx_triad_devs, mode_colors['SPX'])]):
    jitter = np.random.default_rng(42).uniform(-0.12, 0.12, len(devs))
    ax.scatter(np.full(len(devs), i+1) + jitter, devs, c=color, s=25, alpha=0.7,
               edgecolors='white', linewidths=0.5, zorder=4)

ax.set_ylabel('TB/s (per device)', fontsize=11)
ax.set_title('Triad: device distribution', fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)

# Row 3, col 2: Dot device distribution
ax = fig.add_subplot(gs[2, 1])
cpx_dot_devs = [cpx_data[d][dot_idx] / MB_TO_TB for d in cpx_data]
tpx_dot_devs = [tpx_data[d][dot_idx] / MB_TO_TB for d in tpx_data]
spx_dot_devs = [spx_data[d][dot_idx] / MB_TO_TB for d in spx_data]

bp = ax.boxplot([cpx_dot_devs, tpx_dot_devs, spx_dot_devs],
                tick_labels=['CPX\n(24 dev)', 'TPX\n(12 dev)', 'SPX\n(4 dev)'],
                patch_artist=True, widths=0.5)
for patch, color in zip(bp['boxes'], [mode_colors[m] for m in modes]):
    patch.set_facecolor(color); patch.set_alpha(0.6)

for i, (devs, color) in enumerate([(cpx_dot_devs, mode_colors['CPX']),
                                     (tpx_dot_devs, mode_colors['TPX']),
                                     (spx_dot_devs, mode_colors['SPX'])]):
    jitter = np.random.default_rng(42).uniform(-0.12, 0.12, len(devs))
    ax.scatter(np.full(len(devs), i+1) + jitter, devs, c=color, s=25, alpha=0.7,
               edgecolors='white', linewidths=0.5, zorder=4)

ax.set_ylabel('TB/s (per device)', fontsize=11)
ax.set_title('Dot: device distribution', fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.2)
ax.set_axisbelow(True)

# Row 3, col 3: summary table
ax = fig.add_subplot(gs[2, 2])
ax.axis('off')

table_data = []
for mode, nv in [('CPX', cpx_node), ('TPX', tpx_node), ('SPX', spx_node)]:
    n_devs = {'CPX': 24, 'TPX': 12, 'SPX': 4}[mode]
    xcds_per = {'CPX': 1, 'TPX': 2, 'SPX': 6}[mode]
    triad = nv[triad_idx]
    dot = nv[dot_idx]
    table_data.append([
        mode,
        f'{n_devs} × {xcds_per} XCD',
        f'{triad:.1f}',
        f'{triad/THEO_NODE*100:.0f}%',
        f'{dot:.1f}',
        f'{dot/THEO_NODE*100:.0f}%',
    ])

table = ax.table(
    cellText=table_data,
    colLabels=['Mode', 'Layout', 'Triad\n(TB/s)', '% of\npeak', 'Dot\n(TB/s)', '% of\npeak'],
    cellLoc='center',
    loc='center',
    colWidths=[0.11, 0.25, 0.13, 0.11, 0.13, 0.11],
)
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.15, 2)

for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor('#cccccc')
    if row == 0:
        cell.set_facecolor('#f0f0f0')
        cell.set_text_props(fontweight='bold')
    elif col == 0:
        m = ['CPX', 'TPX', 'SPX'][row-1]
        cell.set_facecolor(mode_colors[m])
        cell.set_alpha(0.3)

ax.set_title('Summary', fontsize=13, fontweight='bold', pad=20)

fig.suptitle('MI300A Full-Node BabelStream — CPX vs TPX vs SPX',
             fontsize=16, fontweight='bold')
fig.text(0.5, 0.005,
         'BabelStream · double-precision · arraysize=2²⁸ · numtimes=1500 · '
         'CPX=24×1-XCD · TPX=12×2-XCD · SPX=4×6-XCD · '
         'theoretical peak: 5.3 TB/s per APU, 21.2 TB/s per node',
         ha='center', fontsize=9, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('/home/claude/cpx_tpx_spx_v2.png', dpi=150, bbox_inches='tight')
print("Saved.")