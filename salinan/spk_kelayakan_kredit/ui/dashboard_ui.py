# ui/dashboard_ui.py
import tkinter as tk
from ttkbootstrap import ttk
from models import database

class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")
        self.build_ui()
        self.load_stats()

    def build_ui(self):
        header = ttk.Label(self, text="Dashboard", font=("Helvetica", 18, "bold"))
        header.pack(pady=12)

        # stats frame
        self.stats_frame = ttk.Frame(self)
        self.stats_frame.pack(fill="x", padx=16, pady=8)

        self.lbl_total = ttk.Label(self.stats_frame, text="Total Nasabah: -", font=("Helvetica", 12))
        self.lbl_total.grid(row=0, column=0, padx=8, pady=6, sticky="w")

        self.lbl_kriteria = ttk.Label(self.stats_frame, text="Total Kriteria: -", font=("Helvetica", 12))
        self.lbl_kriteria.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        # quick actions
        quick = ttk.Frame(self)
        quick.pack(fill="x", padx=16, pady=12)

        ttk.Button(quick, text="Kelola Nasabah", command=self.go_nasabah).pack(side="left", padx=6)
        ttk.Button(quick, text="Kelola Kriteria", command=self.go_kriteria).pack(side="left", padx=6)
        ttk.Button(quick, text="Perhitungan", command=self.go_perhitungan).pack(side="left", padx=6)

    def load_stats(self):
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM nasabah")
        total_nasabah = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM kriteria")
        total_kriteria = cur.fetchone()[0]
        conn.close()

        self.lbl_total.config(text=f"Total Nasabah: {total_nasabah}")
        self.lbl_kriteria.config(text=f"Total Kriteria: {total_kriteria}")

    # callbacks require parent App to change frame; we'll find and call parent's methods if exist
    def go_nasabah(self):
        root = self._get_root_app()
        if root and hasattr(root, "show_nasabah"):
            root.show_nasabah()

    def go_kriteria(self):
        root = self._get_root_app()
        if root and hasattr(root, "show_kriteria"):
            root.show_kriteria()

    def go_perhitungan(self):
        root = self._get_root_app()
        if root and hasattr(root, "show_perhitungan"):
            root.show_perhitungan()

    def _get_root_app(self):
        # find top-level window (App)
        p = self
        while p.master:
            p = p.master
            # tb.Window has attribute style, we can detect by attribute
            if hasattr(p, "style"):
                return p
        return None
