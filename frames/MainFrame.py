import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from frames.ClientesFrame  import ClientesFrame
from frames.ServiciosFrame import ServiciosFrame
from frames.ReservasFrame  import ReservasFrame
from frames.LogsFrame      import LogsFrame
from utils import log_info, log_error

CLR = {
    "bg":     "#F4F6F7",
    "header": "#2C3E50",
    "hdr_fg": "#ECF0F1",
    "accent": "#2980B9",
    "ok":     "#27AE60",
    "sub":    "#BDC3C7",
}


class MainFrame(tk.Frame):
    """
    Marco principal del sistema.  Contiene un Notebook con las pestañas:
    Clientes · Servicios · Reservas · Logs
    También expone el botón de Demostración que ejecuta 14+ operaciones.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()

    # ── Construcción ──────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        self._build_notebook()

    def _build_header(self):
        hdr = tk.Frame(self, bg=CLR["header"], pady=8)
        hdr.pack(fill="x")

        tk.Label(
            hdr,
            text="Software FJ  —  Sistema Integral de Gestión",
            font=("Segoe UI", 14, "bold"),
            bg=CLR["header"],
            fg=CLR["hdr_fg"],
        ).pack(side="left", padx=14)

        # Botones del lado derecho
        btn_frame = tk.Frame(hdr, bg=CLR["header"])
        btn_frame.pack(side="right", padx=10)

        tk.Button(
            btn_frame,
            text="▶  Ejecutar Demostración",
            font=("Segoe UI", 9, "bold"),
            bg=CLR["ok"],
            fg="white",
            activebackground="#1E8449",
            relief="flat",
            cursor="hand2",
            command=self._ejecutar_demo,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            btn_frame,
            text="Cerrar sesión",
            font=("Segoe UI", 9),
            bg="#7F8C8D",
            fg="white",
            activebackground="#626567",
            relief="flat",
            cursor="hand2",
            command=self._logout,
        ).pack(side="left")

    def _build_notebook(self):
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=[12, 5])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        self.clientes_frame  = ClientesFrame(nb,  self.controller)
        self.servicios_frame = ServiciosFrame(nb, self.controller)
        self.reservas_frame  = ReservasFrame(nb,  self.controller)
        self.logs_frame      = LogsFrame(nb,      self.controller)

        nb.add(self.clientes_frame,  text="  👤 Clientes  ")
        nb.add(self.servicios_frame, text="  🗂 Servicios  ")
        nb.add(self.reservas_frame,  text="  📋 Reservas  ")
        nb.add(self.logs_frame,      text="  📄 Logs  ")

        self._notebook = nb
        nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

    # ── Eventos ───────────────────────────────────────────────────────────
    def _on_tab_change(self, _event=None):
        """Actualiza logs automáticamente al cambiar a la pestaña de Logs."""
        try:
            current = self._notebook.select()
            if self._notebook.tab(current, "text").strip().endswith("Logs  "):
                self.logs_frame.cargar_logs()
        except Exception:
            pass

    def _logout(self):
        self.controller.logout()

    def _ejecutar_demo(self):
        """Ejecuta la demostración de 14 operaciones en una ventana modal."""
        from demo import ejecutar_demo

        ventana = tk.Toplevel(self)
        ventana.title("Demostración — SoftwareFJ")
        ventana.geometry("760x520")
        ventana.resizable(False, False)
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Simulación de 14 Operaciones del Sistema",
            font=("Segoe UI", 12, "bold"),
            bg="#2C3E50",
            fg="white",
        ).pack(fill="x", ipady=8)

        log_area = scrolledtext.ScrolledText(
            ventana, font=("Consolas", 9), wrap="word", state="disabled",
            bg="#1E2022", fg="#ECF0F1"
        )
        log_area.pack(fill="both", expand=True, padx=8, pady=8)

        def cb(msg: str):
            log_area.config(state="normal")
            log_area.insert("end", msg + "\n")
            log_area.see("end")
            log_area.config(state="disabled")
            ventana.update_idletasks()

        try:
            log_info("=== INICIO DE DEMOSTRACIÓN ===")
            resultados = ejecutar_demo(
                self.controller.gestor_clientes,
                self.controller.gestor_servicios,
                self.controller.gestor_reservas,
                cb=cb,
            )
            log_info(f"=== FIN DE DEMOSTRACIÓN — {len(resultados)} operaciones ===")
        except Exception as exc:
            cb(f"\n[ERROR CRÍTICO en la demo] {exc}")
            log_error("Error crítico en demostración", exc)

        # Refrescar todos los módulos
        self.clientes_frame.refrescar_lista()
        self.servicios_frame.refrescar_lista()
        self.reservas_frame.refrescar_lista()
        self.logs_frame.cargar_logs()

        tk.Button(
            ventana,
            text="Cerrar",
            font=("Segoe UI", 10),
            bg=CLR["accent"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=ventana.destroy,
        ).pack(pady=(0, 10))
