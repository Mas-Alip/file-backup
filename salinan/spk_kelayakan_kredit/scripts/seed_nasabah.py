import sys, os
import sqlite3

# pastikan bisa akses models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_NAME = "spk_kredit.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # tabel user
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')

    # tabel nasabah
    cursor.execute('''CREATE TABLE IF NOT EXISTS nasabah (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        usia INTEGER NOT NULL,
        pekerjaan INTEGER NOT NULL,
        pendapatan INTEGER NOT NULL,
        jaminan INTEGER NOT NULL
    )''')

    # tabel kriteria
    cursor.execute('''CREATE TABLE IF NOT EXISTS kriteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        bobot REAL
    )''')

    # user default
    cursor.execute("SELECT * FROM users")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "123"))

    conn.commit()
    conn.close()

# fungsi encoding & normalisasi
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
    if pendapatan >= 6000000:
        return 4
    elif pendapatan >= 4000000:
        return 3
    elif pendapatan >= 2000000:
        return 2
    else:
        return 1

# dataset 30 nasabah
dataset = [
    ("Andi", 25, "Wiraswasta", 3000000, "BPKB Motor"),
    ("Budi", 40, "PNS", 6000000, "Sertifikat"),
    ("Citra", 30, "Karyawan", 4500000, "BPKB Mobil"),
    ("Dewi", 22, "Mahasiswa", 1500000, "-"),
    ("Eko", 35, "Petani", 2500000, "BPKB Motor"),
    ("Fajar", 28, "Wiraswasta", 3200000, "BPKB Mobil"),
    ("Gita", 42, "PNS", 7000000, "Sertifikat"),
    ("Hendra", 50, "Karyawan", 5500000, "BPKB Mobil"),
    ("Intan", 24, "Mahasiswa", 2000000, "-"),
    ("Joko", 33, "Petani", 2200000, "BPKB Motor"),
    ("Kiki", 29, "Wiraswasta", 3800000, "BPKB Mobil"),
    ("Lina", 38, "Karyawan", 4200000, "Sertifikat"),
    ("Made", 45, "PNS", 8500000, "Sertifikat"),
    ("Nisa", 23, "Mahasiswa", 1800000, "-"),
    ("Oka", 31, "Wiraswasta", 3600000, "BPKB Mobil"),
    ("Putra", 27, "Petani", 2400000, "BPKB Motor"),
    ("Qori", 35, "Karyawan", 4800000, "Sertifikat"),
    ("Rian", 41, "PNS", 7200000, "Sertifikat"),
    ("Sinta", 26, "Karyawan", 3900000, "BPKB Mobil"),
    ("Tono", 39, "Wiraswasta", 3400000, "BPKB Motor"),
    ("Uli", 21, "Mahasiswa", 1600000, "-"),
    ("Vina", 32, "Petani", 2800000, "BPKB Motor"),
    ("Wahyu", 36, "Karyawan", 5000000, "Sertifikat"),
    ("Xena", 29, "Wiraswasta", 3500000, "BPKB Mobil"),
    ("Yoga", 47, "PNS", 9000000, "Sertifikat"),
    ("Zaki", 34, "Petani", 2700000, "BPKB Motor"),
    ("Amanda", 28, "Karyawan", 4600000, "BPKB Mobil"),
    ("Bayu", 30, "Wiraswasta", 3300000, "BPKB Mobil"),
    ("Clara", 25, "Mahasiswa", 1900000, "-"),
    ("Dani", 37, "Petani", 2500000, "BPKB Motor"),
]

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    for nama, usia, pekerjaan, pendapatan, jaminan in dataset:
        usia_enc = normalize_usia(usia)
        pekerjaan_enc = encode_pekerjaan(pekerjaan)
        pendapatan_enc = normalize_pendapatan(pendapatan)
        jaminan_enc = encode_jaminan(jaminan)

        cursor.execute("""
            INSERT INTO nasabah (nama, usia, pekerjaan, pendapatan, jaminan)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, usia_enc, pekerjaan_enc, pendapatan_enc, jaminan_enc))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_data()
    print("✅ Database baru berhasil dibuat & 30 data nasabah sudah masuk!")
