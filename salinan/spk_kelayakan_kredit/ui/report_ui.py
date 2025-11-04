# ui/report_ui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from models import database

class ReportFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_ui()
        self.load_data()

    def build_ui(self):
        header = ttk.Label(self, text="Laporan Data Nasabah", font=("Helvetica", 16, "bold"))
        header.pack(pady=8)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Refresh", command=self.load_data, bg="#3498db", fg="white").pack(side="left", padx=6)
        tk.Button(btn_frame, text="Export Excel", command=self.export_excel, bg="#27ae60", fg="white").pack(side="left", padx=6)
        tk.Button(btn_frame, text="Export PDF", command=self.export_pdf, bg="#34495e", fg="white").pack(side="left", padx=6)

        self.tree = ttk.Treeview(self, columns=("id","nama","usia","pendapatan","pekerjaan","jaminan"), show="headings")
        for col, w in [("id",50),("nama",180),("usia",120),("pendapatan",120),("pekerjaan",160),("jaminan",160)]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=w)
        self.tree.pack(fill="both", expand=True, padx=12, pady=8)

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nama, usia, pendapatan, pekerjaan, jaminan FROM nasabah")
        rows = cur.fetchall()
        conn.close()

        usia_map = {1: "<25 tahun", 2: "25-35 tahun", 3: "36-50 tahun", 4: ">50 tahun"}
        pend_map = {1: "<2 juta", 2: "2-5 juta", 3: "5-10 juta", 4: ">10 juta"}
        kerja_map = {1: "PNS/Karyawan Tetap", 2: "Wiraswasta", 3: "Buruh/Kontrak", 4: "Lainnya"}
        jam_map = {1: "Sertifikat", 2: "BPKB", 3: "Tanpa Jaminan"}

        for row in rows:
            id_, nama, usia, pend, kerja, jam = row
            self.tree.insert("", "end", values=(
                id_, nama,
                usia_map.get(usia, usia),
                pend_map.get(pend, pend),
                kerja_map.get(kerja, kerja),
                jam_map.get(jam, jam)
            ))

    def export_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files","*.xlsx")])
        if not file_path:
            return
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["ID","Nama","Usia","Pendapatan","Pekerjaan","Jaminan"])
        for iid in self.tree.get_children():
            ws.append(self.tree.item(iid)["values"])
        wb.save(file_path)
        messagebox.showinfo("Sukses", f"Disimpan ke {file_path}")

    def export_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
        if not file_path:
            return
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(200, y, "Laporan Data Nasabah")
        y -= 30
        headers = ["ID","Nama","Usia","Pendapatan","Pekerjaan","Jaminan"]
        x_positions = [30, 70, 260, 360, 460, 560]
        for i, h in enumerate(headers):
            c.drawString(x_positions[i], y, h)
        y -= 20
        c.setFont("Helvetica", 9)
        for iid in self.tree.get_children():
            vals = self.tree.item(iid)["values"]
            for i, v in enumerate(vals):
                c.drawString(x_positions[i], y, str(v))
            y -= 15
            if y < 60:
                c.showPage()
                y = height - 40
        c.save()
        messagebox.showinfo("Sukses", f"PDF tersimpan di {file_path}")
