import sqlite3, os

def log_result(idea, results):
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect("data/experiment_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            name TEXT,
            revenue REAL,
            visits INTEGER,
            leads INTEGER,
            strategy TEXT
        )
    """)
    cursor.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?)", (
        idea['name'],
        results['revenue'],
        results['visits'],
        results['leads'],
        idea['concept']
    ))
    conn.commit()
    conn.close()
