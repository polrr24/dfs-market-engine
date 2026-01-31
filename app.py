import streamlit as st
import sqlite3
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="DFS Market Edge",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500&display=swap');

/* FORCE MONOSPACE EVERYWHERE */
html, body, * {
    font-family: 'JetBrains Mono', monospace !important;
}

/* App background */
.stApp {
    background-color: #0b0e14;
    color: #c9d1d9;
}

/* Headers */
h1, h2, h3 {
    color: #e6edf3;
    font-weight: 500;
    letter-spacing: 0.3px;
}

/* Paragraphs / labels */
p, li, span, div {
    color: #c9d1d9;
}

/* Tables */
.stDataFrame {
    background-color: #0f1420;
    border: 1px solid #1f2937;
}

.dataframe {
    font-size: 13px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1f2937;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER / STATUS BAR
# --------------------------------------------------
left_status, right_status = st.columns([3, 2])

with st.container():
    st.markdown("""
<div style="
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #020617;
    padding: 0.6rem 1rem;
    border: 1px solid #1f2937;
    margin-bottom: 1.5rem;
">
    <div>
        <div><strong>DFS MARKET EDGE :: LOCAL NODE</strong></div>
        <div>SOURCE : DFS / MARKET</div>
        <div>REFRESH: 90s</div>
    </div>
    <div style="text-align: right;">
        <div><strong>MODE : RESEARCH</strong></div>
        <div>ENGINE : IDLE</div>
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
DB_PATH = "data/dfs.db"
conn = sqlite3.connect(DB_PATH)

# --------------------------------------------------
# MAIN LAYOUT
# --------------------------------------------------
left, right = st.columns([2, 3])

# -------------------------
# LEFT PANEL — SYSTEM INFO
# -------------------------
with left:
    st.markdown("### SYSTEM STATUS")

    st.markdown("""
- **Scraper**  : OFFLINE  
- **Edges**    : 0 active  
- **Last Tick**: —  
- **Node**     : Localhost  
    """)

    st.markdown("---")

    st.markdown("### PIPELINE LOG")

    st.markdown("""
> Waiting for ingestion pipeline…  
> No DFS props loaded.  
> Monitoring system health.
    """)

# -------------------------
# RIGHT PANEL — EDGE TABLE
# -------------------------
with right:
    st.markdown("### CURRENT EDGES")

    try:
        df = pd.read_sql("""
            SELECT
                app,
                player,
                stat,
                line,
                true_prob,
                edge,
                tier,
                timestamp
            FROM edges
            ORDER BY edge DESC
        """, conn)
    except Exception:
        df = pd.DataFrame()

    if df.empty:
        st.markdown("""
> STATUS  
> No active edges detected.  
> Awaiting DFS + market data alignment…
        """)
    else:
        st.dataframe(df, use_container_width=True)

conn.close()
