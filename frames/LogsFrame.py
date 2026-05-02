import tkinter as tk
from tkinter import scrolledtext

from utils import leer_logs

CLR = {
    "bg":    "#F4F6F7",
    "panel": "#FFFFFF",
    "accent": "#2980B9",
}


class LogsFrame(tk.Frame):
    """Pestaña de visualización del archivo de log del sistema."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=CLR["bg"])
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=CLR["bg"])
        header.pack(fill="x", padx=10, pady=(10, 4))

        tk.Label(
            header,
            text="Registro de Eventos y Errores del Sistema",
            font=("Segoe UI", 11, "bold"),
            bg=CLR["bg"],
        ).pack(side="left")

        tk.Button(
            header,
            text="↺  Actualizar",
            bg=CLR["accent"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.cargar_logs,
        ).pack(side="right")

        panel = tk.LabelFrame(self, text=" logs/app.log ", bg=CLR["panel"],
                              font=("Segoe UI", 9, "bold"))
        panel.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(
            panel,
            font=("Consolas", 9),
            wrap="none",
            state="disabled",
            bg="#1E2022",
            fg="#A8FF60",
            insertbackground="white",
        )
        self.log_text.pack(fill="both", expand=True, padx=6, pady=6)

        # Barra de scroll horizontal
        hscroll = tk.Scrollbar(panel, orient="horizontal",
                               command=self.log_text.xview)
        hscroll.pack(fill="x", padx=6, pady=(0, 4))
        self.log_text.configure(xscrollcommand=hscroll.set)

        self.cargar_logs()

    def cargar_logs(self):
        contenido = leer_logs()
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("end", contenido if contenido else "(Sin registros aún)")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
