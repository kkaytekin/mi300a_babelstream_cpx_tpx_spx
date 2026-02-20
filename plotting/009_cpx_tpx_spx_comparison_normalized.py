import matplotlib.pyplot as plt
import numpy as np

ops = ['Copy', 'Mul', 'Add', 'Triad', 'Dot']

# ── CPX full node: 24 devices, 6 per APU, 1 XCD each ──
# arraysize = 2^28 (2147.5 MB per stream), numtimes=1500
cpx_data = {
    0:  [631190.033,  596760.531,  682621.241,  682774.612,  428210.983],
    1:  [673020.313,  673670.482,  681761.690,  682430.348,  568836.765],
    2:  [709450.045,  709995.389,  713965.306,  713967.759,  621375.224],
    3:  [642826.858,  617712.845,  645396.158,  644391.049,  414570.172],
    4:  [709853.402,  710729.582,  714175.914,  714170.293,  650286.287],
    5:  [710848.390,  711033.149,  714968.491,  714962.064,  702839.525],
    6:  [709943.751,  710357.068,  713977.966,  714159.289,  623109.681],
    7:  [710908.514,  711116.852,  714953.336,  714967.618,  703010.824],
    8:  [603779.831,  578542.769,  638858.495,  645672.288,  410037.263],
    9:  [611121.659,  674988.598,  657756.397,  626313.793,  459314.853],
    10: [710420.517,  710722.526,  714427.684,  714756.701,  675566.272],
    11: [673788.955,  674384.483,  672434.068,  668931.823,  552430.816],
    12: [619336.674,  654629.515,  644049.497,  643278.440,  397855.593],
    13: [709835.804,  710261.915,  714435.606,  714445.906,  645344.148],
    14: [709771.286,  710322.998,  714430.932,  714414.216,  660625.671],
    15: [709068.100,  709673.945,  713898.058,  714124.458,  603456.617],
    16: [676226.801,  656764.805,  660793.817,  655448.279,  449641.006],
    17: [658580.549,  675352.754,  684245.977,  650996.317,  401471.565],
    18: [710225.388,  710424.042,  713985.878,  714167.998,  616724.828],
    19: [710656.789,  710995.601,  714901.846,  714886.695,  704289.392],
    20: [710829.684,  710614.342,  714518.805,  714738.383,  668040.496],
    21: [670810.568,  672100.677,  670991.975,  671334.516,  600202.225],
    22: [671624.680,  672588.091,  671593.454,  671971.793,  600765.474],
    23: [606906.735,  657799.749,  662179.974,  655827.400,  443427.309],
}
cpx_apu_map = {0: list(range(0, 6)), 1: list(range(6, 12)), 2: list(range(12, 18)), 3: list(range(18, 24))}

# ── TPX full node: 12 devices, 3 per APU, 2 XCDs each ──
# arraysize = 2^29 (4295.0 MB per stream, 2× CPX), numtimes=600
tpx_data = {
    0:  [1419336.633, 1420244.574, 1429876.998, 1429980.146, 1355886.778],
    1:  [1329703.415, 1369294.008, 1318553.337, 1334462.696, 1161424.904],
    2:  [1329561.198, 1377550.407, 1321158.745, 1337435.375, 1154424.401],
    3:  [1194311.944, 1094370.433, 1096086.087, 1101087.892,  835763.415],
    4:  [1211527.140, 1116293.248, 1104708.270, 1131079.744,  905932.733],
    5:  [1256503.566, 1232044.089, 1161329.069, 1087218.440,  785016.488],
    6:  [1210932.789, 1119504.072, 1117463.128, 1161319.648,  842164.569],
    7:  [1224438.000, 1166394.043, 1120241.752, 1155773.628,  812725.024],
    8:  [1246448.117, 1254858.720, 1232760.773, 1137590.714,  869338.764],
    9:  [1334095.786, 1314957.858, 1341456.527, 1301882.919, 1135532.837],
    10: [1198638.285, 1361161.657, 1330883.074, 1350478.786, 1067991.624],
    11: [1246272.882, 1257680.783, 1263054.915, 1247335.598,  835331.037],
}
tpx_apu_map = {0: [0, 1, 2], 1: [3, 4, 5], 2: [6, 7, 8], 3: [9, 10, 11]}

# ── SPX full node: 4 devices, 1 per APU, 6 XCDs each ──
# arraysize = 2^31 (12884.9 MB per stream, 6× CPX), numtimes=250
spx_data = {
    0: [3579338.265, 3604062.507, 3492627.042, 3402137.538, 2529591.019],
    1: [3504102.942, 3512144.764, 3307762.040, 3266523.441, 2489446.221],
    2: [3522880.962, 3541155.601, 3474715.525, 3357602.908, 2521795.918],
    3: [3507947.089, 3399359.562, 3265232.093, 3261776.971, 2508449.292],
}
spx_apu_map = {0: [0], 1: [1], 2: [2], 3: [3]}

MB_TO_TB = 1e6
TB_TO_TIB = 1e12 / (2**40)
THEO_APU = 5.3        # TB/s per APU
THEO_NODE = THEO_APU * 4  # 21.2 TB/s

triad_idx = 3
dot_idx   = 4


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
ax.set_ylim(40, 110)
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
ax.set_ylim(30, 110)
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
    n_devs  = {'CPX': 24, 'TPX': 12, 'SPX': 4}[mode]
    xcds    = {'CPX':  1, 'TPX':  2, 'SPX': 6}[mode]
    arr_mb  = {'CPX': '2148', 'TPX': '4295', 'SPX': '12885'}[mode]
    triad   = nv[triad_idx]
    dot     = nv[dot_idx]
    table_data.append([
        mode,
        f'{n_devs} × {xcds} XCD',
        arr_mb,
        f'{triad:.1f}',
        f'{triad/THEO_NODE*100:.0f}%',
        f'{dot:.1f}',
        f'{dot/THEO_NODE*100:.0f}%',
    ])

table = ax.table(
    cellText=table_data,
    colLabels=['Mode', 'Layout', 'Array\n(MB)', 'Triad\n(TB/s)', '% of\npeak', 'Dot\n(TB/s)', '% of\npeak'],
    cellLoc='center',
    loc='center',
    colWidths=[0.10, 0.20, 0.12, 0.13, 0.11, 0.13, 0.11],
)
table.auto_set_font_size(False)
table.set_fontsize(10)
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

fig.suptitle('MI300A Full-Node BabelStream — CPX vs TPX vs SPX (Normalized Array Size)',
             fontsize=15, fontweight='bold')
fig.text(0.5, 0.005,
         'BabelStream · double-precision · array size normalized per XCD: '
         'CPX=2²⁸ elems (2148 MB) · TPX=2²⁹ elems (4295 MB) · SPX=6×2²⁸ elems (12885 MB) · '
         'CPX numtimes=1500 · TPX numtimes=600 · SPX numtimes=250 · '
         'theoretical peak: 5.3 TB/s per APU, 21.2 TB/s per node',
         ha='center', fontsize=8.5, style='italic', color='#555555',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#cccccc', alpha=0.9))

plt.tight_layout(rect=[0, 0.04, 1, 0.95])
plt.savefig('009_cpx_tpx_spx_comparison_normalized.png', dpi=150, bbox_inches='tight')
print("Saved.")
