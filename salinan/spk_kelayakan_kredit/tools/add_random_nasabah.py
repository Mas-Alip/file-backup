"""Add random nasabah entries to existing spk_kredit.db without deleting existing data.
Usage: python tools\add_random_nasabah.py [count]
Default count = 30
"""
import sqlite3
import random
import sys
import os
from models import database as dbmod

DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spk_kredit.db')

# Simple random name generator
first = ["Andi","Budi","Citra","Dewi","Eko","Fajar","Gita","Hendra","Intan","Joko",
         "Kiki","Lina","Made","Nisa","Oka","Putra","Qori","Rian","Sinta","Tono",
         "Uli","Vina","Wahyu","Xena","Yoga","Zaki","Amanda","Bayu","Clara","Dani"]
last = ["Pratama","Santoso","Wijaya","Rahma","Saputra","Kusuma","Suryanto","Irawan","Putri","Halim"]

pekerjaan_choices = ["PNS","Karyawan","Wiraswasta","Petani","Mahasiswa"]
jaminan_choices = ["Sertifikat","BPKB Mobil","BPKB Motor","-"]

# encoding functions (same logic as existing seed_nasabah.py)
def encode_pekerjaan(pekerjaan):
    mapping = {"PNS": 4, "Karyawan": 3, "Wiraswasta": 2, "Petani": 2, "Mahasiswa": 1}
    return mapping.get(pekerjaan, 1)

def encode_jaminan(jaminan):
    mapping = {"Sertifikat": 4, "BPKB Mobil": 3, "BPKB Motor": 2, "-": 1}
    return mapping.get(jaminan, 1)

def normalize_usia(usia):
    if 20 <= usia <= 40:
        return 4
    elif 41 <= usia <= 55:
        return 3
    elif 56 <= usia <= 65:
        return 2
    else:
        return 1

def normalize_pendapatan(pendapatan):
    # pendapatan in full amount (IDR), normalize to 1..4
    if pendapatan >= 6000000:
        return 4
    elif pendapatan >= 4000000:
        return 3
    elif pendapatan >= 2000000:
        return 2
    else:
        return 1


def get_conn():
    # use models.database.get_connection if available to maintain same DB location
    try:
        conn = dbmod.get_connection()
    except Exception:
        conn = sqlite3.connect(DB)
    return conn


def count_nasabah(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM nasabah")
        return cur.fetchone()[0]
    except Exception:
        return 0


def ensure_tables(conn):
    # create minimal tables if missing (non-destructive)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS nasabah (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        usia INTEGER NOT NULL,
        pekerjaan INTEGER NOT NULL,
        pendapatan INTEGER NOT NULL,
        jaminan INTEGER NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS kriteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        bobot REAL
    )''')
    conn.commit()


def gen_random_record():
    nama = random.choice(first) + ' ' + random.choice(last)
    usia_raw = random.randint(20, 60)
    pendapatan_raw = random.choice([1500000, 2200000, 3200000, 4500000, 5500000, 7000000, 9000000])
    pekerjaan = random.choice(pekerjaan_choices)
    jaminan = random.choice(jaminan_choices)

    usia_enc = normalize_usia(usia_raw)
    pekerjaan_enc = encode_pekerjaan(pekerjaan)
    pendapatan_enc = normalize_pendapatan(pendapatan_raw)
    jaminan_enc = encode_jaminan(jaminan)

    return (nama, usia_enc, pekerjaan_enc, pendapatan_enc, jaminan_enc, usia_raw, pendapatan_raw, pekerjaan, jaminan)


def seed_random(count=30):
    conn = get_conn()
    ensure_tables(conn)
    cur = conn.cursor()

    before = count_nasabah(conn)
    print(f"Before: {before} nasabah in DB")

    for _ in range(count):
        nama, usia_enc, pekerjaan_enc, pendapatan_enc, jaminan_enc, usia_raw, pendapatan_raw, pekerjaan_raw, jaminan_raw = gen_random_record()
        cur.execute("INSERT INTO nasabah (nama, usia, pekerjaan, pendapatan, jaminan) VALUES (?, ?, ?, ?, ?)",
                    (nama, usia_enc, pekerjaan_enc, pendapatan_enc, jaminan_enc))
    conn.commit()
    after = count_nasabah(conn)
    print(f"Inserted {count} new nasabah. After: {after} nasabah in DB")
    conn.close()


if __name__ == '__main__':
    cnt = 30
    if len(sys.argv) > 1:
        try:
            cnt = int(sys.argv[1])
        except:
            pass
    seed_random(cnt)
    print('Done')
