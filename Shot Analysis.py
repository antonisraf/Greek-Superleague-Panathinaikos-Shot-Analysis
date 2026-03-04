import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Panathinaikos_shots.csv')

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

x = np.arange(len(players))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 7))
ax.bar(x - width/2, actual, width, label='Actual Goals', color='#1d7a3a') 
ax.bar(x + width/2, expected, width, label='Expected Goals (xG)', color='#a2d5ab')

ax.set_ylabel('Goals')
ax.set_title('Actual VS Expected Goals Per Player')

ax.set_xticks(x)
ax.set_xticklabels(players, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
plt.savefig('actual_vs_expected.png') 

plt.figure(figsize=(12, 6))
colors = ['#1d7a3a' if val >= 0 else '#d9534f' for val in analysis['Efficiency Diff']]
plt.bar(players, analysis['Efficiency Diff'], color=colors)
plt.axhline(0, color='black', linewidth=0.8)
plt.ylabel('Efficiency Difference')
plt.title('Player Efficiency (Actual - xG)')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig('player_efficiency.png') 