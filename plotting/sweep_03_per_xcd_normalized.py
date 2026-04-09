"""Sweep plot 3: Per-XCD normalised Triad — the key insight.
All three modes nearly overlap when you normalise by XCDs per device,
showing that individual silicon delivers similar bandwidth regardless of grouping.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _common import *

fig, ax = plt.subplots(figsize=(8, 5))

configs = [
    ('CPX', 'cpx', 1),
    ('TPX', 'tpx', 2),
    ('SPX', 'spx', 6),
]

for mode, key, n_xcds in configs:
    df = load_sweep(key)
    exps = sorted(df['exp'].unique())
    # Per-XCD buffer: for TPX/SPX the per-device array is n_xcds × the base,
    # so per-XCD = per-device / n_xcds  →  same as CPX buffer
    xcd_buf = np.array([df[df.exp == e]['arraysize_elements'].iloc[0] * 8 / 1e6 / n_xcds
                        for e in exps])

    t_mean = np.array([df[df.exp == e]['Triad_MBs'].mean() / MB_TO_TB / n_xcds for e in exps])
    t_min  = np.array([df[df.exp == e]['Triad_MBs'].min()  / MB_TO_TB / n_xcds for e in exps])
    t_max  = np.array([df[df.exp == e]['Triad_MBs'].max()  / MB_TO_TB / n_xcds for e in exps])

    ax.plot(xcd_buf, t_mean, '-o', color=MODE_COLORS[mode],
            markersize=5, linewidth=2.5, label=mode, zorder=3)
    ax.fill_between(xcd_buf, t_min, t_max, alpha=0.13, color=MODE_COLORS[mode])

ax.axhline(THEO_XCD, color='red', ls='--', lw=1.2, alpha=0.7,
           label=f'XCD peak ({THEO_XCD:.3f} TB/s)')

ax.set_xscale('log')
style_ax(ax, ylabel='TB/s (per XCD)', xlabel='Per-XCD buffer size per array (MB)',
         title='Triad Bandwidth per XCD — Normalised\nOverlap means partition mode is transparent to individual XCDs')
ax.legend(fontsize=10)

fig.tight_layout()
savefig(fig, 'sweep_03_per_xcd_normalized.png')
