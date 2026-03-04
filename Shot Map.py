import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

df = pd.read_csv('pao_full_stats_with_minutes.csv')
df = df[['player_name', 'X', 'Y', 'shotType', 'is_goal', 'xg']]
df = df[df['shotType'] != "Penalty"]

pitch = Pitch(pitch_type='opta', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(13, 8))

colors = ['#1d7a3a' if x == 1 else '#d9534f' for x in df['is_goal']]

pitch.scatter(df.X, df.Y, 
              s=df.xg * 500, 
              c=colors, 
              edgecolors='white', 
              alpha=0.7, 
              ax=ax)

plt.title('Panathinaikos Shot Map', color='white', size=20, pad=20)
fig.set_facecolor('#22312b')
plt.savefig('Shot Map.png') 
plt.show()

