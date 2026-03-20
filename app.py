import streamlit as st
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import re

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="PAO Analytics", layout="wide", page_icon="🍀")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=Barlow:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif !important;
    background-color: #0d1a13 !important;
    color: #e8f0eb !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #132019 !important;
    border-right: 1px solid #1e3528 !important;
}
[data-testid="stSidebar"] * { color: #e8f0eb !important; }

/* Selectbox label */
[data-testid="stSidebar"] label {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: #7a9c85 !important;
}

/* Selectbox widget */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #0d1a13 !important;
    border: 1px solid #1b5e35 !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
    border-color: #00a651 !important;
    box-shadow: 0 0 0 2px rgba(0,166,81,0.2) !important;
}

/* Main title */
h1 {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 900 !important;
    font-size: 2.1rem !important;
    letter-spacing: 1px !important;
    color: #e8f0eb !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #132019 !important;
    border: 1px solid #1e3528 !important;
    border-left: 3px solid #00a651 !important;
    border-radius: 10px !important;
    padding: 16px 20px !important;
}
[data-testid="metric-container"] label {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #7a9c85 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    color: #e8f0eb !important;
}

/* Tabs */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1e3528 !important;
}
[data-baseweb="tab"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 13px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #7a9c85 !important;
    background: transparent !important;
    border: none !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: #00a651 !important;
    border-bottom: 2px solid #00a651 !important;
}

/* Section headers */
h3 {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: #7a9c85 !important;
    border-bottom: 1px solid #1e3528 !important;
    padding-bottom: 6px !important;
}

hr { border-color: #1e3528 !important; }

/* pyplot containers — force same bg */
[data-testid="stImage"] img { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA LOAD
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/pao_full_stats_with_minutes.csv')

        ordered_matches = [
            ("14151977", "levadiakos"),
            ("14151961", "kifisia"),
            ("14151978", "olympiacos"),
            ("14151962", "panetolikos"),
            ("14151988", "atromitos"),
            ("14151991", "aris"),
            ("14152000", "asteras"),
            ("14152006", "volos"),
            ("14152018", "paok"),
            ("14152020", "panserraikos"),
            ("14152030", "aek"),
            ("14152032", "larisa"),
            ("14152045", "volos"),
            ("14152052", "paok"),
            ("14159112", "panserraikos"),
            ("14159111", "aek"),
            ("14159125", "atromitos"),
            ("14159131", "kifisia"),
            ("14159139", "olympiacos"),
            ("14159147", "larisa"),
            ("14159157", "ofi"),
            ("14159161", "aris"),
            ("15477451", "ofi"),
            ("14159167", "levadiakos"),
            ("14159174", "panetolikos"),
        ]

        team_names = {
            "levadiakos":   "Levadiakos",
            "kifisia":      "Kifisia",
            "olympiacos":   "Olympiacos",
            "panetolikos":  "Panetolikos",
            "atromitos":    "Atromitos",
            "aris":         "Aris",
            "asteras":      "Asteras Tripolis",
            "volos":        "Volos",
            "paok":         "PAOK",
            "panserraikos": "Panserraikos",
            "aek":          "AEK Athens",
            "larisa":       "Larisa",
            "ofi":          "OFI Crete",
        }

        ordinal = {1: "1ος", 2: "2ος", 3: "3ος", 4: "4ος", 5: "5ος"}
        counts      = {}
        id_to_label = {}
        label_order = []

        for match_id, opp_key in ordered_matches:
            opp_name        = team_names[opp_key]
            counts[opp_key] = counts.get(opp_key, 0) + 1
            n               = counts[opp_key]
            label           = f"vs {opp_name} ({ordinal.get(n, str(n)+'ος')} αγώνας)"
            id_to_label[match_id] = label
            label_order.append(label)

        def clean_id(val):
            found = re.search(r'(\d+)', str(val))
            return found.group(1) if found else str(val)

        df['clean_match_id'] = df['match_id'].apply(clean_id)
        df['match_label']    = df['clean_match_id'].map(id_to_label).fillna("Other")

        return df, label_order
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame(), []


df, match_order = load_data()


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
import base64

def get_logo_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    logo_b64  = get_logo_b64("Panathinaikos_F.C._logo.svg.png")
    logo_html = (
        f'<img src="data:image/png;base64,{logo_b64}" '
        f'style="width:90px;height:90px;object-fit:contain;'
        f'filter:drop-shadow(0 0 12px rgba(0,166,81,0.5));margin-bottom:10px;">'
    )
except Exception:
    logo_html = '<div style="font-size:52px;margin-bottom:10px;">🍀</div>'

with st.sidebar:
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:center;
                padding:28px 0 22px;border-bottom:1px solid #1e3528;margin-bottom:20px;">
        {logo_html}
        <div style="font-family:'Barlow Condensed',sans-serif;font-weight:900;
                    font-size:14px;letter-spacing:3px;text-transform:uppercase;color:#00a651;">
            Panathinaikos
        </div>
        <div style="font-size:11px;letter-spacing:2px;color:#7a9c85;margin-top:3px;">
            Season 2025 – 26
        </div>
    </div>
    """, unsafe_allow_html=True)

    existing_labels = set(df['match_label'].unique()) if not df.empty else set()
    seen, ordered_unique = set(), []
    for m in match_order:
        if m in existing_labels and m not in seen:
            ordered_unique.append(m)
            seen.add(m)

    match_options   = ["Όλοι οι Αγώνες"] + ordered_unique
    selected_match  = st.selectbox("Αντίπαλος", match_options)
    player_options  = ["Όλη η Ομάδα"] + (sorted(df['player_name'].unique().tolist()) if not df.empty else [])
    selected_player = st.selectbox("Παίκτης", player_options)


# ─────────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────────
if not df.empty:

    # Filter
    filtered_df = df.copy()
    if selected_match != "Όλοι οι Αγώνες":
        filtered_df = filtered_df[filtered_df['match_label'] == selected_match]
    if selected_player != "Όλη η Ομάδα":
        filtered_df = filtered_df[filtered_df['player_name'] == selected_player]

    # Minutes
    total_mins   = 0
    show_minutes = selected_player != "Όλη η Ομάδα"
    if show_minutes:
        if selected_match != "Όλοι οι Αγώνες":
            total_mins = int(filtered_df['minute'].max()) if not filtered_df.empty else 0
            min_text   = f" &nbsp;·&nbsp; {total_mins}'"
        else:
            total_mins = int(df[df['player_name'] == selected_player].groupby('match_id')['minute'].max().sum())
            min_text   = f" &nbsp;·&nbsp; {total_mins}' total"
    else:
        min_text = ""

    match_text = selected_match if selected_match != "Όλοι οι Αγώνες" else "All Matches"

    st.markdown(f"""
    <h1>
        <span style="color:#00a651;">{selected_player}</span>{min_text}
        <span style="font-weight:300;font-size:1.3rem;color:#7a9c85;margin-left:14px;">— {match_text}</span>
    </h1>
    """, unsafe_allow_html=True)

    # Metrics (3 only — no conversion)
    actual_g   = int(filtered_df['is_goal'].sum())
    expected_g = filtered_df['xg'].sum()

    if show_minutes:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Σύνολο Σουτ", len(filtered_df))
        c2.metric("Γκολ",        actual_g)
        c3.metric("xG",          f"{expected_g:.2f}")
        c4.metric("Λεπτά",       f"{total_mins}'")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Σύνολο Σουτ", len(filtered_df))
        c2.metric("Γκολ",        actual_g)
        c3.metric("xG",          f"{expected_g:.2f}")

    st.divider()

    # ── TABS ──
    tab1, tab2 = st.tabs(["📍  Shot Analysis", "📊  Player Efficiency"])

    # Shared matplotlib colors
    PITCH_BG = '#132019'
    FIG_BG   = '#0d1a13'

    with tab1:
        col1, col2 = st.columns(2, gap="medium")

        pitch = Pitch(
            pitch_type='opta',
            pitch_color=PITCH_BG,
            line_color='#3a6649',
            linewidth=1.2,
        )

        # ── Shot Locations ──
        with col1:
            st.markdown("### Shot Locations")

            fig, ax = pitch.draw(figsize=(9, 6))
            fig.set_facecolor(FIG_BG)
            ax.set_facecolor(PITCH_BG)

            goals  = filtered_df[filtered_df['is_goal'] == 1]
            misses = filtered_df[filtered_df['is_goal'] == 0]

            if not misses.empty:
                pitch.scatter(
                    misses.X, misses.Y,
                    s=misses.xg * 900,
                    c='#c0392b', edgecolors='#e0e0e0',
                    linewidth=0.5, alpha=0.45,
                    ax=ax, zorder=2,
                )
            if not goals.empty:
                pitch.scatter(
                    goals.X, goals.Y,
                    s=goals.xg * 900,
                    c='#00a651', edgecolors='white',
                    linewidth=0.8,
                    ax=ax, zorder=3,
                )

            legend_els = [
                Line2D([0],[0], marker='o', color='w', label='Γκολ',
                       markerfacecolor='#00a651', markersize=10),
                Line2D([0],[0], marker='o', color='w', label='Αστοχία',
                       markerfacecolor='#c0392b', markersize=10, alpha=0.6),
            ]
            ax.legend(
                handles=legend_els,
                facecolor=PITCH_BG, labelcolor='#e8f0eb',
                fontsize=9, loc='lower right',
                frameon=True, edgecolor='#1e3528', framealpha=0.95,
            )
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        # ── Shot Density ──
        with col2:
            st.markdown("### Shot Density")

            fig2, ax2 = pitch.draw(figsize=(9, 6))
            fig2.set_facecolor(FIG_BG)
            ax2.set_facecolor(PITCH_BG)

            if len(filtered_df) >= 2:
                pitch.kdeplot(
                    filtered_df.X, filtered_df.Y,
                    fill=True, levels=60,
                    cmap='Greens',
                    ax=ax2, alpha=0.75, thresh=0.05,
                )

            plt.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

    with tab2:
        st.markdown("### Efficiency: Actual Goals vs xG")

        eff_df = (
            filtered_df
            .groupby('player_name')
            .agg({'is_goal': 'sum', 'xg': 'sum'})
            .reset_index()
        )
        eff_df = (
            eff_df[eff_df['is_goal'] + eff_df['xg'] > 0]
            .sort_values('xg', ascending=True)
        )

        if not eff_df.empty:
            num_players = len(eff_df)
            eff_df = eff_df.sort_values('xg', ascending=False).reset_index(drop=True)

            COL_W     = 0.45   # inches per player column
            fig_width = max(7, num_players * COL_W + 1.5)
            bar_width = 0.18
            font_size = 8

            fig3, ax3 = plt.subplots(figsize=(fig_width, 5))
            fig3.set_facecolor(FIG_BG)
            ax3.set_facecolor(PITCH_BG)

            x_pos   = range(num_players)
            gap     = 0.11
            max_val = max(eff_df['is_goal'].max(), eff_df['xg'].max())
            ax3.set_ylim(0, max(1.2, max_val + max_val * 0.18 + 0.3))

            # xG bars (left of center)
            ax3.bar(
                [p - gap for p in x_pos], eff_df['xg'],
                width=bar_width, label='xG',
                color='#1b5e35', alpha=0.95,
                edgecolor='#3a6649', linewidth=0.4,
            )
            # Goals bars (right of center)
            ax3.bar(
                [p + gap for p in x_pos], eff_df['is_goal'],
                width=bar_width, label='Γκολ',
                color='#00a651',
                edgecolor='#5dd68a', linewidth=0.4,
            )

            # Value labels on top of bars
            for i, (_, row) in enumerate(eff_df.iterrows()):
                if row['xg'] > 0:
                    ax3.text(i - gap, row['xg'] + max_val * 0.02,
                             f"{row['xg']:.2f}", ha='center', va='bottom',
                             color='#7a9c85', fontsize=font_size - 0.5)
                ax3.text(i + gap, row['is_goal'] + max_val * 0.02,
                         f"{int(row['is_goal'])}", ha='center', va='bottom',
                         color='#e8f0eb', fontsize=font_size - 0.5)

            ax3.set_xticks(x_pos)
            ax3.set_xticklabels(
                eff_df['player_name'],
                rotation=40, ha='right',
                color='#e8f0eb', fontsize=font_size,
            )
            ax3.tick_params(axis='y', colors='#7a9c85', labelsize=font_size)
            ax3.tick_params(axis='x', length=0)
            ax3.yaxis.grid(True, color='#1e3528', linewidth=0.5, linestyle='--')
            ax3.set_axisbelow(True)
            ax3.legend(
                facecolor=PITCH_BG, labelcolor='#e8f0eb',
                fontsize=8, loc='upper right',
                edgecolor='#1e3528', framealpha=0.9,
            )
            for spine in ['top', 'right']:
                ax3.spines[spine].set_visible(False)
            ax3.spines['left'].set_color('#1e3528')
            ax3.spines['bottom'].set_color('#1e3528')

            plt.tight_layout(pad=0.8)
            st.pyplot(fig3)
            plt.close(fig3)
        else:
            st.info("Δεν υπάρχουν δεδομένα.")

else:
    st.error("Σφάλμα φόρτωσης CSV.")