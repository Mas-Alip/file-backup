# methods/saw.py
import numpy as np

def build_decision_matrix(rows, criteria_names):
    """
    rows: list of sqlite3.Row or dict-like dengan keys 'id','nama','usia','pekerjaan','pendapatan','jaminan'
    criteria_names: list of criteria nama (string) sesuai table kriteria urut
    
    Returns:
      matrix: numpy array shape (n_alternatives, n_criteria)
      labels: list of tuples (id, nama) untuk tiap baris
    """
    def extract_value(r, crit):
        c = crit.lower()
        # mapping otomatis ke kolom nasabah
        if "usia" in c:
            return float(r["usia"])
        if "pendapatan" in c or "income" in c or "gaji" in c:
            return float(r["pendapatan"])
        if "pekerjaan" in c or "job" in c:
            return float(r["pekerjaan"])
        if "jaminan" in c or "agunan" in c or "collateral" in c:
            return float(r["jaminan"])
        # fallback: jika kriterianya sesuai nama kolom
        if c in r.keys():
            return float(r[c])
        raise KeyError(f"Tidak tahu cara mengambil nilai untuk kriteria '{crit}'")

    matrix = []
    labels = []
    for r in rows:
        row_vals = []
        for crit in criteria_names:
            val = extract_value(r, crit)
            row_vals.append(val)
        matrix.append(row_vals)
        labels.append((r["id"], r["nama"]))
    return np.array(matrix, dtype=float), labels

def saw(matrix, weights, benefit_flags=None):
    """
    matrix: numpy array shape (n_alt, n_crit)
    weights: iterable length n_crit (should sum to 1 or not - kita akan normalisasi di luar)
    benefit_flags: list/array boolean len n_crit: True jika benefit (lebih besar lebih baik)
    
    Returns:
      scores: numpy array shape (n_alt,)
      norm_matrix: normalized matrix used in scoring
    """
    M = np.array(matrix, dtype=float)
    w = np.array(weights, dtype=float)
    n_alt, n_crit = M.shape

    if w.size != n_crit:
        raise ValueError(f"Jumlah bobot ({w.size}) tidak cocok dengan jumlah kriteria ({n_crit}).")

    # jika bobot belum normalized, normalisasi
    if not np.isclose(w.sum(), 1.0):
        w = w / w.sum()

    if benefit_flags is None:
        benefit_flags = [True] * n_crit
    if len(benefit_flags) != n_crit:
        raise ValueError("benefit_flags harus panjangnya sama dengan jumlah kriteria")

    # normalisasi SAW
    norm = np.zeros_like(M, dtype=float)
    for j in range(n_crit):
        col = M[:, j]
        if benefit_flags[j]:
            maxv = np.max(col) if np.max(col) != 0 else 1.0
            norm[:, j] = col / maxv
        else:
            minv = np.min(col) if np.min(col) != 0 else 1.0
            # cost -> smaller better
            # hati-hati pembagian nol
            norm[:, j] = minv / np.where(col == 0, 1e-9, col)

    scores = norm.dot(w)
    return scores, norm
