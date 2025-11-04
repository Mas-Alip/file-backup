# main.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox

# UI frames (from ui package)
from ui.login import LoginFrame
from ui.dashboard_ui import DashboardFrame
from ui.nasabah_ui import NasabahFrame
from ui.kriteria_ui import KriteriaFrame
from ui.perhitungan_ui import PerhitunganFrame
from ui.report_ui import ReportFrame

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("SPK Kelayakan Kredit")
        self.geometry("1200x700")
        self.minsize(1000,600)

        # state: user logged in or not
        self.user = None

        # top-level layout containers
        self.sidebar = tk.Frame(self, bg="#2b2f33", width=230)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self, bg="white")
        self.content.pack(side="right", fill="both", expand=True)

        # theme state
        self.current_theme = "cosmo"
        self.alt_theme = "darkly"

        # At start, show login in content area and only minimal sidebar (Logout disabled)
        self.active_frame = None

        # build sidebar buttons (some will be enabled after login)
        self._build_sidebar_buttons()
        # show login
        self.show_login()

    def _build_sidebar_buttons(self):
        # header label
        header = tb.Label(self.sidebar, text="SPK Koperasi", bootstyle="inverse-dark", font=("Segoe UI", 14, "bold"))
        header.pack(fill="x", pady=(12,10), padx=10)

        # create buttons (we'll keep references to enable/disable)
        self.btn_dashboard = tb.Button(self.sidebar, text="Dashboard", bootstyle="secondary-outline", command=self.show_dashboard)
        self.btn_nasabah = tb.Button(self.sidebar, text="Kelola Nasabah", bootstyle="secondary-outline", command=self.show_nasabah)
        self.btn_kriteria = tb.Button(self.sidebar, text="Kelola Kriteria", bootstyle="secondary-outline", command=self.show_kriteria)
        self.btn_perhitungan = tb.Button(self.sidebar, text="Perhitungan (AHP & SAW)", bootstyle="secondary-outline", command=self.show_perhitungan)
        self.btn_report = tb.Button(self.sidebar, text="Hasil & Laporan", bootstyle="secondary-outline", command=self.show_report)
        self.btn_logout = tb.Button(self.sidebar, text="Logout", bootstyle="danger-outline", command=self.logout)

        # pack them, but disable until login
        for w in (self.btn_dashboard, self.btn_nasabah, self.btn_kriteria, self.btn_perhitungan, self.btn_report):
            w.pack(fill="x", padx=12, pady=6)
            w.configure(state="disabled")

        # logout below
        self.btn_logout.pack(side="bottom", fill="x", padx=12, pady=12)
        self.btn_logout.configure(state="disabled")

        # theme switch
        self.theme_btn = tb.Button(self.sidebar, text="Switch Theme", bootstyle="info-outline", command=self.switch_theme)
        self.theme_btn.pack(side="bottom", fill="x", padx=12, pady=(0,12))

    def enable_main_buttons(self, enable=True):
        state = "normal" if enable else "disabled"
        for w in (self.btn_dashboard, self.btn_nasabah, self.btn_kriteria, self.btn_perhitungan, self.btn_report):
            w.configure(state=state)
        self.btn_logout.configure(state=state)

    def clear_content(self):
        if self.active_frame is not None:
            try:
                self.active_frame.destroy()
            except:
                pass
            self.active_frame = None

    # --- Show frames ---
    def show_login(self):
        self.clear_content()
        self.user = None
        # disable main buttons
        self.enable_main_buttons(False)
        self.active_frame = LoginFrame(self.content, on_login=self._on_login_success)
        self.active_frame.pack(fill="both", expand=True)

    def _on_login_success(self, username):
        # callback from LoginFrame when login success
        self.user = username
        self.enable_main_buttons(True)
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_content()
        self.active_frame = DashboardFrame(self.content)
        self.active_frame.pack(fill="both", expand=True)

    def show_nasabah(self):
        self.clear_content()
        self.active_frame = NasabahFrame(self.content)
        self.active_frame.pack(fill="both", expand=True)

    def show_kriteria(self):
        self.clear_content()
        self.active_frame = KriteriaFrame(self.content)
        self.active_frame.pack(fill="both", expand=True)

    def show_perhitungan(self):
        self.clear_content()
        self.active_frame = PerhitunganFrame(self.content)
        self.active_frame.pack(fill="both", expand=True)

    def show_report(self):
        self.clear_content()
        self.active_frame = ReportFrame(self.content)
        self.active_frame.pack(fill="both", expand=True)

    def logout(self):
        if messagebox.askyesno("Logout", "Yakin ingin logout?"):
            # destroy active frame & show login
            self.show_login()

    def switch_theme(self):
        # toggle between two themes
        if self.current_theme == self.alt_theme:
            self.style.theme_use(self.alt_theme)
            self.current_theme = "cosmo"
            self.style.theme_use("cosmo")
        else:
            self.style.theme_use(self.alt_theme)
            self.current_theme = self.alt_theme

if __name__ == "__main__":
    app = App()
    app.mainloop()