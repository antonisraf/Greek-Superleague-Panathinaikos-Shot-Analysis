import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/pao_full_stats_with_minutes.csv')



analysis = df.groupby('player_name').agg({
    'is_goal': 'sum',
    'xg': 'sum'
}).reset_index()

analysis['efficiency'] = analysis['is_goal'] - analysis['xg']

analysis.columns = ['Player', 'Actual Goals', 'Expected Goals (xG)', 'Efficiency Diff']

analysis = analysis.sort_values(by='Actual Goals', ascending=False)

print(analysis.to_string(index=False))

players = analysis['Player']
actual = analysis['Actual Goals']
expected = analysis['Expected Goals (xG)']

plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
bg_color = '#1b2721' 

fig, ax = plt.subplots(figsize=(14, 7), facecolor=bg_color)
ax.set_facecolor(bg_color)

x = np.arange(len(players))
width = 0.35

ax.bar(x - width/2, actual, width, label='Actual Goals', color='#28a745', edgecolor=bg_color) 
ax.bar(x + width/2, expected, width, label='Expected Goals (xG)', color='#a2d5ab', alpha=0.7, edgecolor=bg_color)

ax.set_ylabel('Goals', fontweight='bold')
ax.set_title('Actual VS Expected Goals Per Player', fontsize=15, pad=20, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(players, rotation=45, ha='right')

for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
ax.legend(facecolor=bg_color, edgecolor='white')
ax.grid(axis='y', linestyle='--', alpha=0.1)

plt.tight_layout()
plt.savefig('actual_vs_expected_dark.png', facecolor=fig.get_facecolor())


fig2, ax2 = plt.subplots(figsize=(14, 7), facecolor=bg_color)
ax2.set_facecolor(bg_color)

colors = ['#28a745' if val >= 0 else '#d9534f' for val in analysis['Efficiency Diff']]
ax2.bar(players, analysis['Efficiency Diff'], color=colors, edgecolor=bg_color)

ax2.axhline(0, color='white', linewidth=1, alpha=0.5)
ax2.set_ylabel('Efficiency Difference', fontweight='bold')
ax2.set_title('Player Efficiency (Actual - xG)', fontsize=15, pad=20, fontweight='bold')
ax2.set_xticks(range(len(players)))
ax2.set_xticklabels(players, rotation=45, ha='right')

for spine in ['top', 'right']: ax2.spines[spine].set_visible(False)
ax2.grid(axis='y', linestyle='--', alpha=0.1)

plt.tight_layout()
plt.savefig('player_efficiency_dark.png', facecolor=fig2.get_facecolor())
plt.show()