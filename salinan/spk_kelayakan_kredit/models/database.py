import sqlite3

DB_NAME = "spk_kredit.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Tabel Users
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    # Tabel Nasabah
    cur.execute('''
        CREATE TABLE IF NOT EXISTS nasabah (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            usia INTEGER NOT NULL,
            pekerjaan TEXT NOT NULL,
            pendapatan REAL NOT NULL,
            jaminan TEXT NOT NULL
        )
    ''')

    # Tabel Kriteria
    cur.execute('''
        CREATE TABLE IF NOT EXISTS kriteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            bobot REAL NOT NULL
        )
    ''')

    # Tabel untuk menyimpan matriks pairwise kriteria (serialized JSON)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS kriteria_pairwise (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            matrix TEXT
        )
    ''')

    # User default
    cur.execute("SELECT * FROM users")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "123"))

    conn.commit()
    conn.close()
