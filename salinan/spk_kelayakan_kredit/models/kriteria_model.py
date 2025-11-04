from .database import get_connection
import json

def tambah_kriteria(nama, bobot):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO kriteria (nama, bobot) VALUES (?, ?)", (nama, bobot))
    conn.commit()
    conn.close()

def get_all_kriteria():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM kriteria")
    data = cur.fetchall()
    conn.close()
    return data


def save_pairwise_matrix(name, matrix):
    """Simpan matrix pairwise (2D list/array) sebagai JSON teks, keyed by name."""
    conn = get_connection()
    cur = conn.cursor()
    # ensure table exists (in case create_tables() wasn't run)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS kriteria_pairwise (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            matrix TEXT
        )
    ''')
    mat_json = json.dumps(matrix)
    # upsert
    cur.execute("INSERT OR REPLACE INTO kriteria_pairwise (name, matrix) VALUES (?, ?)", (name, mat_json))
    conn.commit()
    conn.close()


def load_pairwise_matrix(name):
    conn = get_connection()
    cur = conn.cursor()
    # ensure table exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS kriteria_pairwise (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            matrix TEXT
        )
    ''')
    cur.execute("SELECT matrix FROM kriteria_pairwise WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    try:
        return json.loads(row[0])
    except Exception:
        return None


def delete_pairwise_matrix(name):
    """Hapus entry pairwise dengan nama tertentu dari tabel (dipakai untuk reset awal jika perlu)."""
    conn = get_connection()
    cur = conn.cursor()
    # ensure table exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS kriteria_pairwise (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            matrix TEXT
        )
    ''')
    cur.execute("DELETE FROM kriteria_pairwise WHERE name = ?", (name,))
    conn.commit()
    conn.close()
