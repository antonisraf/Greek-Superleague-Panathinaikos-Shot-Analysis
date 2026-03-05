import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

df = pd.read_csv('data/pao_full_stats_with_minutes.csv')


goals_only = df[df['is_goal'] == 1]

pitch = Pitch(pitch_type='opta', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(13, 8))
fig.set_facecolor('#22312b')

pitch.kdeplot(
    goals_only.X, 
    goals_only.Y, 
    fill=True, 
    levels=100, 
    thresh=0.05, 
    cut=4, 
    cmap='plasma',
    ax=ax
)

plt.title('Panathinaikos Goal Density (Scoring Zones)', color='white', size=20, pad=20)
plt.savefig('plots/goal_density_heatmap.png', bbox_inches='tight', dpi=300)
plt.show()