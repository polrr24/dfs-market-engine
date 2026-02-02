import streamlit as st
import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="DFS Market Edge",
    layout="wide",
    initial_sidebar_state="collapsed",
)

REFRESH_MS = 90_000  # 90 seconds
DB_PATH = "data/dfs.db"

st_autorefresh(interval=REFRESH_MS, key="auto_refresh")

# ============================================================
# GLOBAL THEME / CSS - PRODUCTION POLISH
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Azeret+Mono:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

:root {
    --bg-primary: #0a0e14;
    --bg-secondary: #0d1117;
    --bg-panel: #13171f;
    --bg-panel-light: #161b24;
    --bg-hover: #1a2030;
    --border-primary: #21262d;
    --border-secondary: #30363d;
    --border-accent: #3d4450;
    
    --text-primary: #e6edf3;
    --text-secondary: #7d8590;
    --text-tertiary: #656d76;
    
    --accent-green: #3fb950;
    --accent-green-bright: #56d364;
    --accent-cyan: #39c5cf;
    --accent-yellow: #d29922;
    --accent-orange: #f66a0a;
    --accent-red: #f85149;
    
    --glow-green: rgba(63, 185, 80, 0.4);
    --glow-cyan: rgba(57, 197, 207, 0.4);
    --glow-yellow: rgba(210, 153, 34, 0.4);
    
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.5);
}

* {
    font-family: 'Azeret Mono', 'Share Tech Mono', monospace !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

html, body, [class*="css"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary);
}

section[data-testid="stSidebar"] {
    display: none !important;
}

.block-container {
    padding: 1.75rem 2.5rem 2rem 2.5rem;
    max-width: 100%;
}

/* ===== HEADER BAR ===== */
.main-header {
    background: var(--bg-secondary);
    border: 1px solid var(--border-secondary);
    border-radius: 6px;
    padding: 0;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-md);
    overflow: hidden;
}

.header-top {
    background: linear-gradient(135deg, #0f1419 0%, #0a0e14 100%);
    padding: 0.8rem 1.5rem;
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--border-primary);
}

.header-title {
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.08rem;
    color: var(--accent-green-bright);
    text-shadow: 0 0 12px var(--glow-green);
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.header-title::before {
    content: '▸';
    font-size: 1.1rem;
    opacity: 0.8;
}

.header-bottom {
    padding: 0.85rem 1.5rem;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 2rem;
    background: var(--bg-secondary);
}

.header-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.3rem 0.8rem;
    background: rgba(63, 185, 80, 0.12);
    border: 1px solid var(--accent-green);
    border-radius: 4px;
    color: var(--accent-green-bright);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12rem;
    text-transform: uppercase;
    box-shadow: 0 0 8px var(--glow-green);
}

.header-badge::before {
    content: '●';
    margin-right: 0.5rem;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.header-meta {
    display: flex;
    gap: 1.5rem;
    font-size: 0.7rem;
    color: var(--text-secondary);
    letter-spacing: 0.05rem;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.meta-label {
    color: var(--text-tertiary);
    text-transform: uppercase;
}

.meta-value {
    color: var(--text-primary);
    font-weight: 500;
}

/* ===== PANELS ===== */
.panel {
    background: linear-gradient(135deg, var(--bg-panel) 0%, var(--bg-secondary) 100%);
    border: 1px solid var(--border-secondary);
    border-radius: 6px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-md);
    position: relative;
}

.panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan) 50%, transparent);
    opacity: 0.2;
}

/* ===== SECTION HEADERS ===== */
.section-header {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--accent-cyan);
    text-transform: uppercase;
    letter-spacing: 0.15rem;
    margin-bottom: 1.25rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid var(--border-accent);
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.section-header::before {
    content: '◆';
    font-size: 0.65rem;
    color: var(--accent-cyan);
    opacity: 0.7;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 80px;
    height: 2px;
    background: var(--accent-cyan);
    box-shadow: 0 0 8px var(--glow-cyan);
}

/* ===== STATUS ITEMS ===== */
.status-grid {
    display: grid;
    gap: 1rem;
}

.status-item {
    padding: 0.75rem;
    background: rgba(22, 27, 36, 0.4);
    border-left: 2px solid var(--border-accent);
    border-radius: 2px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.status-item:hover {
    background: rgba(26, 32, 48, 0.5);
    border-left-color: var(--accent-cyan);
    transform: translateX(4px);
    box-shadow: var(--shadow-sm);
}

.status-label {
    display: block;
    color: var(--text-tertiary);
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.08rem;
    margin-bottom: 0.4rem;
    font-weight: 500;
}

.status-value {
    display: block;
    color: var(--text-primary);
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.02rem;
}

.status-online {
    color: var(--accent-green-bright);
    font-weight: 700;
    text-shadow: 0 0 10px var(--glow-green);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.status-online::before {
    content: '●';
    animation: pulse 2s ease-in-out infinite;
}

/* ===== ALERT BOX ===== */
.alert-box {
    background: rgba(210, 153, 34, 0.08);
    border-left: 3px solid var(--accent-yellow);
    border-radius: 4px;
    padding: 1.25rem;
    margin: 0;
}

.alert-title {
    font-weight: 700;
    font-size: 0.8rem;
    color: var(--accent-yellow);
    text-transform: uppercase;
    letter-spacing: 0.08rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.alert-title::before {
    content: '⚠';
    font-size: 1rem;
}

.alert-body {
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.7;
    margin-bottom: 1rem;
}

.alert-checklist {
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(210, 153, 34, 0.2);
}

.checklist-item {
    font-size: 0.75rem;
    color: var(--text-tertiary);
    margin: 0.35rem 0;
    padding-left: 0.25rem;
}

.checklist-item::before {
    content: '▸';
    margin-right: 0.5rem;
    color: var(--accent-yellow);
    opacity: 0.6;
}

/* ===== FILTER SECTION ===== */
.filter-section {
    margin: 2rem 0 1.5rem 0;
}

.filter-header {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--accent-cyan);
    text-transform: uppercase;
    letter-spacing: 0.15rem;
    margin-bottom: 1rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid var(--border-accent);
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.filter-header::before {
    content: '◆';
    font-size: 0.65rem;
    color: var(--accent-cyan);
    opacity: 0.7;
}

.filter-header::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 80px;
    height: 2px;
    background: var(--accent-cyan);
    box-shadow: 0 0 8px var(--glow-cyan);
}

/* Hide the default Streamlit label */
label[data-testid="stSelectbox-label"] {
    display: none !important;
}

/* ===== DROPDOWN ===== */
div[data-baseweb="select"] {
    margin-top: 0.5rem;
}

div[data-baseweb="select"] > div {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: 5px !important;
    color: var(--text-primary) !important;
    font-size: 0.85rem !important;
    transition: all 0.2s;
}

div[data-baseweb="select"] > div:hover {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 8px var(--glow-cyan);
}

div[data-baseweb="select"] svg {
    fill: var(--text-secondary) !important;
}

/* Dropdown menu */
[role="listbox"] {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: 5px !important;
    box-shadow: var(--shadow-lg) !important;
}

[role="option"] {
    background-color: transparent !important;
    color: var(--text-primary) !important;
    font-size: 0.85rem !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.15s;
}

[role="option"]:hover {
    background-color: var(--bg-hover) !important;
    border-left: 2px solid var(--accent-cyan);
}

[aria-selected="true"] {
    background-color: var(--bg-hover) !important;
    color: var(--accent-green-bright) !important;
}

/* ===== TABLE STYLING ===== */
div[data-testid="stDataFrame"] {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-secondary) !important;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: var(--shadow-md);
}

div[data-testid="stDataFrame"] > div {
    background-color: var(--bg-secondary) !important;
}

/* Table headers */
thead tr th {
    background: linear-gradient(180deg, var(--bg-panel-light) 0%, var(--bg-panel) 100%) !important;
    color: var(--accent-cyan) !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12rem !important;
    font-weight: 700 !important;
    border-bottom: 2px solid var(--border-accent) !important;
    padding: 1rem 1.25rem !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 10 !important;
}

/* Table rows */
tbody tr {
    border-bottom: 1px solid var(--border-primary) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

tbody tr:hover {
    background: linear-gradient(90deg, rgba(57, 197, 207, 0.05) 0%, transparent 100%) !important;
    border-left: 3px solid var(--accent-cyan) !important;
    transform: translateX(2px);
}

tbody td {
    color: var(--text-primary) !important;
    font-size: 0.8rem !important;
    padding: 0.9rem 1.25rem !important;
    font-weight: 400 !important;
}

/* Alternating row colors for better readability */
tbody tr:nth-child(even) {
    background-color: rgba(13, 17, 23, 0.3) !important;
}

/* ===== LOG TERMINAL ===== */
.log-terminal {
    background: #000000;
    border: 1px solid var(--border-accent);
    border-radius: 5px;
    padding: 1.25rem;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem;
    line-height: 1.9;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6);
}

.log-line {
    display: flex;
    gap: 1rem;
    margin: 0.25rem 0;
}

.log-time {
    color: var(--text-tertiary);
    opacity: 0.7;
    min-width: 70px;
}

.log-message {
    color: var(--accent-green);
    flex: 1;
}

.log-warning {
    color: var(--accent-yellow);
}

.log-info {
    color: var(--accent-cyan);
}

/* ===== UTILITY ===== */
.spacer {
    height: 2rem;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb {
    background: var(--border-accent);
    border-radius: 5px;
    border: 2px solid var(--bg-primary);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-tertiary);
}

/* ===== REMOVE STREAMLIT BRANDING ===== */
footer { visibility: hidden; height: 0; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; height: 0; }

/* ===== ANIMATIONS ===== */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.panel {
    animation: fadeIn 0.4s ease-out;
}

/* ===== RESPONSIVE ADJUSTMENTS ===== */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1.5rem;
    }
    
    .header-bottom {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DB CONNECTION
# ============================================================
conn = sqlite3.connect(DB_PATH)

# ============================================================
# HEADER
# ============================================================
# First, get available apps for the header display
apps_df_temp = pd.read_sql("""
    SELECT DISTINCT app
    FROM dfs_props
    ORDER BY app
""", conn)
app_options_temp = apps_df_temp["app"].tolist()
default_app = app_options_temp[0] if app_options_temp else "PrizePicks"

st.markdown(f"""
<div class="main-header">
    <div class="header-top">
        <div class="header-title">DFS MARKET EDGE :: LOCAL NODE</div>
    </div>
    <div class="header-bottom">
        <div class="header-badge">LIVE</div>
        <div class="header-meta">
            <div class="meta-item">
                <span class="meta-label">Engine:</span>
                <span class="meta-value" id="current-engine">{default_app}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Refresh:</span>
                <span class="meta-value">90s</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Mode:</span>
                <span class="meta-value">Research</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SYSTEM STATUS + CURRENT EDGES
# ============================================================
col1, col2 = st.columns([1, 3])

# Use session state to track selected app, defaulting to first available
if 'selected_app' not in st.session_state:
    st.session_state.selected_app = default_app

with col1:
    total_props = pd.read_sql(
        "SELECT COUNT(*) AS c FROM dfs_props WHERE app=?",
        conn,
        params=(st.session_state.selected_app,)
    )["c"][0]

    leagues = pd.read_sql(
        "SELECT COUNT(DISTINCT league) AS c FROM dfs_props WHERE app=?",
        conn,
        params=(st.session_state.selected_app,)
    )["c"][0]

    st.markdown(f"""
    <div class="panel">
        <div class="section-header">System Status</div>
        <div class="status-grid">
            <div class="status-item">
                <span class="status-label">Scraper Status</span>
                <span class="status-online">ONLINE</span>
            </div>
            <div class="status-item">
                <span class="status-label">Props Loaded</span>
                <span class="status-value">{total_props:,}</span>
            </div>
            <div class="status-item">
                <span class="status-label">Active Leagues</span>
                <span class="status-value">{leagues}</span>
            </div>
            <div class="status-item">
                <span class="status-label">Current App</span>
                <span class="status-value">{st.session_state.selected_app}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="panel">
        <div class="section-header">Current Edges</div>
        <div class="alert-box">
            <div class="alert-title">Edge Engine: Standby</div>
            <div class="alert-body">
                No edge engine active yet.<br/>
                Awaiting true-probability model + sportsbook baseline integration...
            </div>
            <div class="alert-checklist">
                <div class="checklist-item">Initialize edge detection protocols</div>
                <div class="checklist-item">Configure probability thresholds</div>
                <div class="checklist-item">Connect baseline data sources</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# APP SELECTOR & LEAGUE FILTER
# ============================================================
st.markdown('<div class="filter-header">Select App</div>', unsafe_allow_html=True)

# Get available apps from database
apps_df = pd.read_sql("""
    SELECT DISTINCT app
    FROM dfs_props
    ORDER BY app
""", conn)

app_options = apps_df["app"].tolist()
selected_app = st.selectbox("Select App", app_options, label_visibility="collapsed", key="app_selector")

# Update session state when selection changes
st.session_state.selected_app = selected_app

st.markdown('<div style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)

# ============================================================
# LEAGUE FILTER
# ============================================================
st.markdown('<div class="filter-header">Filter by League</div>', unsafe_allow_html=True)

# Get leagues for selected app
leagues_df = pd.read_sql("""
    SELECT DISTINCT league
    FROM dfs_props
    WHERE app = ?
    ORDER BY league
""", conn, params=(selected_app,))

league_options = ["ALL"] + leagues_df["league"].tolist()
selected_league = st.selectbox("Filter by League", league_options, label_visibility="collapsed")

st.markdown('<div style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)

# ============================================================
# LIVE PROPS TABLE
# ============================================================
st.markdown('<div class="section-header">Live Props</div>', unsafe_allow_html=True)

if selected_league == "ALL":
    df = pd.read_sql("""
        SELECT player, stat, line, league, timestamp
        FROM dfs_props
        WHERE app = ?
        ORDER BY timestamp DESC
        LIMIT 500
    """, conn, params=(selected_app,))
else:
    df = pd.read_sql("""
        SELECT player, stat, line, league, timestamp
        FROM dfs_props
        WHERE app = ? AND league = ?
        ORDER BY timestamp DESC
        LIMIT 500
    """, conn, params=(selected_app, selected_league))

st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================
# PIPELINE LOG
# ============================================================
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

current_time = datetime.now().strftime('%H:%M:%S')

st.markdown(f"""
<div class="panel">
    <div class="section-header">Pipeline Log</div>
    <div class="log-terminal">
        <div class="log-line">
            <span class="log-time">[{current_time}]</span>
            <span class="log-message">Ingestion pipeline running every 90s</span>
        </div>
        <div class="log-line">
            <span class="log-time">[{current_time}]</span>
            <span class="log-message">Deduplication enforced</span>
        </div>
        <div class="log-line">
            <span class="log-time">[{current_time}]</span>
            <span class="log-warning">Edge engine not initialized</span>
        </div>
        <div class="log-line">
            <span class="log-time">[{current_time}]</span>
            <span class="log-info">Monitoring {total_props:,} props across {leagues} leagues</span>
        </div>
        <div class="log-line">
            <span class="log-time">[{current_time}]</span>
            <span class="log-message">Database connection stable</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

conn.close()