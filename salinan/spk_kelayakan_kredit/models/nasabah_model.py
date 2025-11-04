from .database import get_connection

def tambah_nasabah(nama, usia, pekerjaan, pendapatan, jaminan):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO nasabah (nama, usia, pekerjaan, pendapatan, jaminan)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, usia, pekerjaan, pendapatan, jaminan))
    conn.commit()
    conn.close()

def get_all_nasabah():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM nasabah")
    data = cur.fetchall()
    conn.close()
    return data
