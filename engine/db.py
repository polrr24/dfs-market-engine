import sqlite3

DB_PATH = "data/dfs.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dfs_props (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app TEXT,
        player TEXT,
        stat TEXT,
        line REAL,
        league TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS edges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app TEXT,
        player TEXT,
        stat TEXT,
        line REAL,
        true_prob REAL,
        edge REAL,
        tier TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
