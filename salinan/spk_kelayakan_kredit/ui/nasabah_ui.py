# ui/nasabah_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import database

class NasabahFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_ui()
        self.load_data()

    def build_ui(self):
        # form
        form = tk.Frame(self)
        form.pack(padx=12, pady=8, anchor="nw")

        tk.Label(form, text="Nama").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.entry_nama = tk.Entry(form, width=30)
        self.entry_nama.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(form, text="Usia (Kategori)").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        self.combo_usia = ttk.Combobox(form, values=[
            "1 - <25 tahun", "2 - 25-35 tahun", "3 - 36-50 tahun", "4 - >50 tahun"
        ], width=28, state="readonly")
        self.combo_usia.grid(row=1, column=1, padx=6, pady=6)

        tk.Label(form, text="Pendapatan (Kategori)").grid(row=2, column=0, padx=6, pady=6, sticky="e")
        self.combo_pendapatan = ttk.Combobox(form, values=[
            "1 - <2 juta", "2 - 2-5 juta", "3 - 5-10 juta", "4 - >10 juta"
        ], width=28, state="readonly")
        self.combo_pendapatan.grid(row=2, column=1, padx=6, pady=6)

        tk.Label(form, text="Pekerjaan").grid(row=3, column=0, padx=6, pady=6, sticky="e")
        self.combo_pekerjaan = ttk.Combobox(form, values=[
            "1 - PNS/Karyawan Tetap", "2 - Wiraswasta", "3 - Buruh/Karyawan Kontrak", "4 - Lainnya"
        ], width=28, state="readonly")
        self.combo_pekerjaan.grid(row=3, column=1, padx=6, pady=6)

        tk.Label(form, text="Jaminan").grid(row=4, column=0, padx=6, pady=6, sticky="e")
        self.combo_jaminan = ttk.Combobox(form, values=[
            "1 - Sertifikat Rumah/Tanah", "2 - BPKB Kendaraan", "3 - Tanpa Jaminan"
        ], width=28, state="readonly")
        self.combo_jaminan.grid(row=4, column=1, padx=6, pady=6)

        btn_frame = tk.Frame(form)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Simpan", command=self.simpan_nasabah, bg="#2ecc71", fg="white").pack(side="left", padx=6)
        tk.Button(btn_frame, text="Reset", command=self.reset_form, bg="#e67e22", fg="white").pack(side="left", padx=6)

        # tabel dengan fitur seleksi (ceklist style) dan tombol aksi
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=12, pady=8)

        # Add a 'Sel' column to act like a checkbox (☐ / ☑) for UI selection
        cols = ("Sel", "ID", "Nama", "Usia", "Pendapatan", "Pekerjaan", "Jaminan")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            # narrow column for selection
            if c == "Sel":
                self.tree.column(c, width=40, anchor='center')
            elif c == "Nama":
                self.tree.column(c, width=220)
            else:
                self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True)

        # maintain selected set of nasabah ids shown in the table
        self._selected_ids = set()

        # bind click to toggle selection checkbox
        self.tree.bind('<Button-1>', self._on_tree_click)

        # actions for selection and deletion/move
        action_frame = tk.Frame(self)
        action_frame.pack(fill='x', padx=12, pady=(0,8))
        ttk.Button(action_frame, text='Pilih Semua', command=self._select_all).pack(side='left', padx=4)
        ttk.Button(action_frame, text='Batal Pilih Semua', command=self._clear_selection).pack(side='left', padx=4)
        ttk.Button(action_frame, text='Hapus Terpilih', command=self._delete_selected).pack(side='left', padx=4)
        ttk.Button(action_frame, text='Pindah ke Processed', command=self._move_selected_to_processed).pack(side='left', padx=4)
        ttk.Button(action_frame, text='Tampilkan Processed', command=self._show_processed).pack(side='left', padx=4)

    def simpan_nasabah(self):
        nama = self.entry_nama.get().strip()
        usia = self.combo_usia.get().split(" - ")[0] if self.combo_usia.get() else None
        pendapatan = self.combo_pendapatan.get().split(" - ")[0] if self.combo_pendapatan.get() else None
        pekerjaan = self.combo_pekerjaan.get().split(" - ")[0] if self.combo_pekerjaan.get() else None
        jaminan = self.combo_jaminan.get().split(" - ")[0] if self.combo_jaminan.get() else None

        if not all([nama, usia, pendapatan, pekerjaan, jaminan]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO nasabah (nama, usia, pendapatan, pekerjaan, jaminan) VALUES (?, ?, ?, ?, ?)",
            (nama, int(usia), int(pendapatan), int(pekerjaan), int(jaminan))
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Sukses", "Data nasabah berhasil ditambahkan.")
        # clear form
        self.reset_form()
        self.load_data()

    def reset_form(self):
        self.entry_nama.delete(0, tk.END)
        self.combo_usia.set("")
        self.combo_pendapatan.set("")
        self.combo_pekerjaan.set("")
        self.combo_jaminan.set("")

    def load_data(self):
        # clear existing rows
        for r in self.tree.get_children():
            self.tree.delete(r)

        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nama, usia, pendapatan, pekerjaan, jaminan FROM nasabah")
        rows = cur.fetchall()
        conn.close()

        usia_map = {1: "<25 tahun", 2: "25-35 tahun", 3: "36-50 tahun", 4: ">50 tahun"}
        pend_map = {1: "<2 juta", 2: "2-5 juta", 3: "5-10 juta", 4: ">10 juta"}
        kerja_map = {1: "PNS/Karyawan Tetap", 2: "Wiraswasta", 3: "Buruh/Karyawan Kontrak", 4: "Lainnya"}
        jam_map = {1: "Sertifikat Rumah/Tanah", 2: "BPKB Kendaraan", 3: "Tanpa Jaminan"}

        for row in rows:
            id_, nama, usia, pend, kerja, jam = row
            sel_symbol = '☑' if id_ in self._selected_ids else '☐'
            self.tree.insert("", "end", values=(
                sel_symbol,
                id_, nama,
                usia_map.get(usia, usia),
                pend_map.get(pend, pend),
                kerja_map.get(kerja, kerja),
                jam_map.get(jam, jam)
            ))

    # ---------------- Selection helpers ----------------
    def _on_tree_click(self, event):
        # identify row clicked and toggle selection checkbox
        region = self.tree.identify('region', event.x, event.y)
        if region != 'cell':
            return
        col = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)
        if not item:
            return
        # only toggle when Sel column (first column #1) is clicked
        if col == '#1':
            vals = self.tree.item(item, 'values')
            try:
                id_val = int(vals[1])
            except Exception:
                return
            if id_val in self._selected_ids:
                self._selected_ids.remove(id_val)
            else:
                self._selected_ids.add(id_val)
            # update symbol
            # rebuild values tuple
            new_sel = '☑' if id_val in self._selected_ids else '☐'
            new_vals = list(vals)
            new_vals[0] = new_sel
            self.tree.item(item, values=new_vals)

    def _select_all(self):
        # add all displayed ids to selected set
        for item in self.tree.get_children():
            vals = self.tree.item(item, 'values')
            try:
                id_val = int(vals[1])
            except Exception:
                continue
            self._selected_ids.add(id_val)
            new_vals = list(vals)
            new_vals[0] = '☑'
            self.tree.item(item, values=new_vals)

    def _clear_selection(self):
        self._selected_ids.clear()
        for item in self.tree.get_children():
            vals = list(self.tree.item(item, 'values'))
            vals[0] = '☐'
            self.tree.item(item, values=vals)

    def _delete_selected(self):
        if not self._selected_ids:
            messagebox.showinfo('Info', 'Belum ada nasabah yang dipilih.')
            return
        ok = messagebox.askyesno('Hapus Nasabah', f'Yakin ingin menghapus {len(self._selected_ids)} nasabah terpilih?')
        if not ok:
            return
        try:
            ids = list(self._selected_ids)
            q_marks = ','.join(['?'] * len(ids))
            conn = database.get_connection()
            cur = conn.cursor()
            cur.execute(f'DELETE FROM nasabah WHERE id IN ({q_marks})', ids)
            conn.commit()
            conn.close()
            messagebox.showinfo('Sukses', 'Nasabah terpilih berhasil dihapus.')
            self._selected_ids.clear()
            self.load_data()
        except Exception as e:
            messagebox.showerror('Error', f'Gagal menghapus nasabah: {e}')

    def _move_selected_to_processed(self):
        if not self._selected_ids:
            messagebox.showinfo('Info', 'Belum ada nasabah yang dipilih.')
            return
        ok = messagebox.askyesno('Pindah ke Processed', f'Pindahkan {len(self._selected_ids)} nasabah terpilih ke grup processed?')
        if not ok:
            return
        try:
            ids = list(self._selected_ids)
            q_marks = ','.join(['?'] * len(ids))
            conn = database.get_connection()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS processed_nasabah (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_id INTEGER,
                    nama TEXT,
                    usia INTEGER,
                    pendapatan REAL,
                    pekerjaan TEXT,
                    jaminan TEXT,
                    processed_at TEXT
                )
            ''')
            cur.execute(f"SELECT id, nama, usia, pendapatan, pekerjaan, jaminan FROM nasabah WHERE id IN ({q_marks})", ids)
            rows = cur.fetchall()
            import datetime
            now = datetime.datetime.now().isoformat()
            for row in rows:
                orig_id, nama, usia, pendapatan, pekerjaan, jaminan = row
                cur.execute('''INSERT INTO processed_nasabah (original_id, nama, usia, pendapatan, pekerjaan, jaminan, processed_at)
                               VALUES (?, ?, ?, ?, ?, ?, ?)''', (orig_id, nama, usia, pendapatan, pekerjaan, jaminan, now))
            cur.execute(f'DELETE FROM nasabah WHERE id IN ({q_marks})', ids)
            conn.commit()
            conn.close()
            messagebox.showinfo('Sukses', 'Nasabah terpilih telah dipindahkan ke processed.')
            self._selected_ids.clear()
            self.load_data()
        except Exception as e:
            messagebox.showerror('Error', f'Gagal memindahkan nasabah: {e}')

    def _show_processed(self):
        # show processed_nasabah in a new window
        try:
            conn = database.get_connection()
            cur = conn.cursor()
            cur.execute('SELECT id, original_id, nama, usia, pendapatan, pekerjaan, jaminan, processed_at FROM processed_nasabah')
            rows = cur.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror('Error', f'Gagal membaca processed_nasabah: {e}')
            return
        win = tk.Toplevel(self)
        win.title('Processed Nasabah')
        tree = ttk.Treeview(win, columns=('ID','OrigID','Nama','Usia','Pendapatan','Pekerjaan','Jaminan','ProcessedAt'), show='headings')
        for c in ('ID','OrigID','Nama','Usia','Pendapatan','Pekerjaan','Jaminan','ProcessedAt'):
            tree.heading(c, text=c)
            tree.column(c, width=120)
        tree.pack(fill='both', expand=True)
        for r in rows:
            tree.insert('', 'end', values=r)
