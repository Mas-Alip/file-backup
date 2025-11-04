import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
from models import nasabah_model, kriteria_model, result_model
from methods import saw
from ui import export_excel

class HasilWindow:
    def __init__(self, root):
        self.top = Toplevel(root)
        self.top.title("Hasil Keputusan & Export")
        w, h = 700, 480
        sw = self.top.winfo_screenwidth(); sh = self.top.winfo_screenheight()
        x = int((sw/2)-(w/2)); y = int((sh/2)-(h/2))
        self.top.geometry(f"{w}x{h}+{x}+{y}")
        self.top.resizable(False, False)

        frm = tk.Frame(self.top, padx=10, pady=10)
        frm.pack(fill='both', expand=True)

        tk.Button(frm, text="Proses SAW (Hitung Skor)", width=22, command=self.proses_saw).pack(pady=8)
        tk.Button(frm, text="Refresh Hasil", width=22, command=self.refresh_results).pack(pady=4)
        tk.Button(frm, text="Export Hasil", width=22, command=self.export_hasil).pack(pady=4)

        cols = ("id","nama","skor","status","waktu")
        self.tree = ttk.Treeview(frm, columns=cols, show="headings", height=15)
        for col, wcol in zip(cols, (40,220,80,120,160)):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=wcol)
        self.tree.pack(fill='both', expand=True)
        self.refresh_results()

    def proses_saw(self):
        nasabah = nasabah_model.get_all_nasabah()
        kriteria = kriteria_model.ambil_semua_kriteria()
        if not nasabah:
            messagebox.showwarning("Peringatan", "Belum ada data nasabah.")
            return
        if not kriteria:
            messagebox.showwarning("Peringatan", "Belum ada kriteria. Silakan tambahkan kriteria dulu.")
            return

        # ensure weights sum to 1; if not, normalize
        total_bobot = sum([k[2] for k in kriteria])
        if total_bobot == 0:
            messagebox.showwarning("Peringatan", "Bobot kriteria semua nol. Atur bobot dulu.")
            return
        if abs(total_bobot - 1.0) > 1e-6:
            # normalize locally and update DB
            normalized = [ (k[0], k[1], k[2]/total_bobot, k[3]) for k in kriteria ]
            for kid, _, nb, _ in normalized:
                kriteria_model.update_bobot_kriteria(kid, nb)
            kriteria = kriteria_model.ambil_semua_kriteria()

        # compute SAW scores
        hasil = saw(nasabah, kriteria)
        # determine threshold simple rule: skor >= 0.5 => Layak (you can adapt)
        for nasabah_id, nama, skor in hasil:
            status = "Layak" if skor >= 0.5 else "Tidak Layak"
            result_model.simpan_hasil(nasabah_id, nama, skor, status)

        messagebox.showinfo("Selesai", "Proses penilaian SAW selesai dan hasil disimpan.")
        self.refresh_results()

    def refresh_results(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = result_model.ambil_semua_hasil()
        for r in rows:
            self.tree.insert("", "end", values=(r[0], r[2], f"{r[3]:.4f}", r[4], r[5]))

    def export_hasil(self):
        rows = result_model.ambil_semua_hasil()
        if not rows:
            messagebox.showinfo("Info", "Belum ada hasil untuk diexport.")
            return
        data = [(r[2], r[3], r[4], r[5]) for r in rows]  # nama, skor, status, waktu
        filename = export_excel(data)
        if filename:
            messagebox.showinfo("Selesai", f"Hasil diexport ke: {filename}")
