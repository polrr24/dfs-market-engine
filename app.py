import streamlit as st
import sqlite3
import pandas as pd

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: #0f1117;
    color: #cdd6f4;
}

h1, h2, h3 {
    color: #89b4fa;
}

.stDataFrame {
    background-color: #1e1e2e;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="DFS Edge Dashboard", layout="wide")

st.title("DFS Market Edge Dashboard")

conn = sqlite3.connect("data/dfs.db")

st.subheader("Current Edges")

df = pd.read_sql("""
SELECT app, player, stat, line, true_prob, edge, tier, timestamp
FROM edges
ORDER BY edge DESC
""", conn)

if df.empty:
    st.info("No edges yet — scraper coming soon 🚧")
else:
    st.dataframe(df, use_container_width=True)
