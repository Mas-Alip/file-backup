# methods/ahp.py
import numpy as np

RI_TABLE = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}

def ahp_from_pairwise(matrix):
    """
    Hitung bobot, CI, CR dari matriks perbandingan berpasangan (square matrix).
    Menggunakan eigenvector utama.
    """
    M = np.array(matrix, dtype=float)
    n = M.shape[0]
    if n == 0 or M.shape[1] != n:
        raise ValueError("Pairwise matrix harus berbentuk n x n dan n>0")

    eigvals, eigvecs = np.linalg.eig(M)
    # pilih eigenvector yang punya eigenvalue terbesar (real part)
    max_idx = np.argmax(eigvals.real)
    max_eigval = eigvals.real[max_idx]
    principal_vec = eigvecs[:, max_idx].real
    # pastikan bobot positif dan sum=1
    principal_vec = np.abs(principal_vec)
    weights = principal_vec / principal_vec.sum()

    # consistency
    lambda_max = max_eigval
    CI = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    RI = RI_TABLE.get(n, 1.49)
    CR = CI / RI if RI != 0 else 0.0

    return weights, CI, CR

def ahp_from_weights(db_weights):
    """
    Jika user sudah punya bobot (misal dimasukkan manual di DB),
    bangun matriks pairwise konsisten dari bobot tsb lalu hitung CI/CR.
    Ini akan menghasilkan CR ~ 0 (karena matriks konsisten).
    """
    arr = np.array(db_weights, dtype=float)
    if arr.size == 0:
        raise ValueError("db_weights kosong")
    # jika bobot belum normalized, normalisasi dulu
    if not np.isclose(arr.sum(), 1.0):
        arr = arr / arr.sum()

    n = arr.size
    pairwise = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            # rasio bobot -> consistent matrix
            pairwise[i, j] = arr[i] / arr[j] if arr[j] != 0 else 0.0

    weights, CI, CR = ahp_from_pairwise(pairwise)
    return weights, CI, CR, pairwise

def aggregate_pairwise(matrices):
    """
    matrices: list of 2D lists/numpy arrays (all same shape NxN)
    returns: aggregated matrix (numpy array) computed by geometric mean (element-wise)
    """
    arrs = [np.array(m, dtype=float) for m in matrices]
    if len(arrs) == 0:
        raise ValueError("No matrices to aggregate.")
    # element-wise geometric mean: product^(1/k)
    prod = np.ones_like(arrs[0], dtype=float)
    for a in arrs:
        prod = prod * a
    agg = prod ** (1.0 / len(arrs))
    # Ensure diagonal ones (numerical safety)
    np.fill_diagonal(agg, 1.0)
    return agg


def ahp_calculation(matrix):
    """
    Menghitung bobot AHP, lambda_max, CI, dan CR
    berdasarkan pairwise comparison matrix.
    """
    try:
        # Normalisasi matriks
        col_sum = np.sum(matrix, axis=0)
        norm_matrix = matrix / col_sum

        # Bobot rata-rata dari tiap baris
        weights = np.mean(norm_matrix, axis=1)

        # Hitung lambda_max
        lambda_max = np.sum(col_sum * weights)

        # Hitung Consistency Index (CI)
        n = matrix.shape[0]
        CI = (lambda_max - n) / (n - 1) if n > 1 else 0

        # Hitung Random Index (RI) sesuai n
        RI_dict = {
            1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
            6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
        }
        RI = RI_dict.get(n, 1.49)  # default jika >10 pakai 1.49

        # Hitung Consistency Ratio (CR)
        CR = CI / RI if RI != 0 else 0

        return weights, lambda_max, CI, CR

    except Exception as e:
        raise ValueError(f"Gagal menghitung AHP: {e}")