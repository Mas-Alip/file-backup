# ui/kriteria_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import database

class KriteriaFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_ui()
        self.load_kriteria()

    def build_ui(self):
        form = tk.Frame(self)
        form.pack(padx=12, pady=8, anchor="nw")

        tk.Label(form, text="Nama Kriteria").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.entry_nama = tk.Entry(form, width=30)
        self.entry_nama.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(form, text="Bobot (mis. 0.25)").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        self.entry_bobot = tk.Entry(form, width=30)
        self.entry_bobot.grid(row=1, column=1, padx=6, pady=6)

        btn_frame = tk.Frame(form)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="Tambah", bg="#2ecc71", fg="white", command=self.tambah_kriteria).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Update Terpilih", bg="#f39c12", fg="white", command=self.update_kriteria).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Hapus Terpilih", bg="#e74c3c", fg="white", command=self.hapus_kriteria).pack(side="left", padx=6)

        # tabel
        table = tk.Frame(self)
        table.pack(fill="both", expand=True, padx=12, pady=8)

        cols = ("ID", "Nama", "Bobot")
        self.tree = ttk.Treeview(table, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150)
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def tambah_kriteria(self):
        nama = self.entry_nama.get().strip()
        bobot = self.entry_bobot.get().strip()
        if not nama or not bobot:
            messagebox.showerror("Error", "Nama dan bobot harus diisi.")
            return
        try:
            b = float(bobot)
        except:
            messagebox.showerror("Error", "Bobot harus angka (mis. 0.25).")
            return

        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO kriteria (nama, bobot) VALUES (?, ?)", (nama, b))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukses", "Kriteria ditambahkan.")
        self.entry_nama.delete(0, tk.END)
        self.entry_bobot.delete(0, tk.END)
        self.load_kriteria()

    def load_kriteria(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nama, bobot FROM kriteria ORDER BY id")
        rows = cur.fetchall()
        conn.close()
        for r in rows:
            self.tree.insert("", "end", values=r)

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self.entry_nama.delete(0, tk.END)
        self.entry_nama.insert(0, vals[1])
        self.entry_bobot.delete(0, tk.END)
        self.entry_bobot.insert(0, vals[2])

    def update_kriteria(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Pilih kriteria terlebih dahulu.")
            return
        id_ = self.tree.item(sel[0])["values"][0]
        nama = self.entry_nama.get().strip()
        bobot = self.entry_bobot.get().strip()
        try:
            b = float(bobot)
        except:
            messagebox.showerror("Error", "Bobot harus angka.")
            return
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE kriteria SET nama=?, bobot=? WHERE id=?", (nama, b, id_))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukses", "Kriteria diperbarui.")
        self.load_kriteria()

    def hapus_kriteria(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Pilih kriteria yang ingin dihapus.")
            return
        id_ = self.tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Konfirmasi", "Hapus kriteria terpilih?"):
            return
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM kriteria WHERE id=?", (id_,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukses", "Kriteria dihapus.")
        self.load_kriteria()
