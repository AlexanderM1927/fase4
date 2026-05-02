import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from models.exceptions import SoftwareFJError
from utils import log_info, log_error

CLR = {
    "bg":    "#F4F6F7",
    "panel": "#FFFFFF",
    "accent": "#2980B9",
    "ok":    "#27AE60",
    "err":   "#C0392B",
    "warn":  "#E67E22",
}


class ClientesFrame(tk.Frame):
    """Pestaña de gestión de clientes."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=CLR["bg"])
        self.controller = controller
        self._build_ui()

    # ── Interfaz ──────────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_left()
        self._build_right()

    def _build_left(self):
        left = tk.Frame(self, bg=CLR["bg"])
        left.pack(side="left", fill="y", padx=(8, 4), pady=8)

        # Formulario
        form = tk.LabelFrame(left, text=" Nuevo Cliente ", bg=CLR["panel"],
                             font=("Segoe UI", 9, "bold"))
        form.pack(fill="x")

        campos = [
            ("Cédula:",    "ced_var"),
            ("Nombre:",    "nom_var"),
            ("Apellido:",  "ape_var"),
            ("Email:",     "ema_var"),
            ("Teléfono:",  "tel_var"),
        ]
        for label, attr in campos:
            tk.Label(form, text=label, bg=CLR["panel"],
                     font=("Segoe UI", 9)).pack(anchor="w", padx=8, pady=(5, 0))
            var = tk.StringVar()
            setattr(self, attr, var)
            tk.Entry(form, textvariable=var, width=26,
                     font=("Segoe UI", 10)).pack(padx=8, fill="x")

        tk.Button(
            form, text="Registrar Cliente",
            bg=CLR["accent"], fg="white",
            font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
            command=self._registrar,
        ).pack(fill="x", padx=8, pady=8)

        # Lista
        lista = tk.LabelFrame(left, text=" Clientes Registrados ", bg=CLR["panel"],
                              font=("Segoe UI", 9, "bold"))
        lista.pack(fill="both", expand=True, pady=(6, 0))

        cols = ("cedula", "nombre", "email", "estado")
        self.tree = ttk.Treeview(lista, columns=cols, show="headings", height=10)
        for col, txt, w in [
            ("cedula", "Cédula",  90),
            ("nombre", "Nombre", 140),
            ("email",  "Email",  150),
            ("estado", "Estado",  70),
        ]:
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        sb.pack(side="right", fill="y", pady=5)

    def _build_right(self):
        right = tk.Frame(self, bg=CLR["bg"])
        right.pack(side="left", fill="both", expand=True, padx=(4, 8), pady=8)

        # Operaciones
        ops = tk.LabelFrame(right, text=" Operaciones ", bg=CLR["panel"],
                            font=("Segoe UI", 9, "bold"))
        ops.pack(fill="x", pady=(0, 6))

        row_btns = tk.Frame(ops, bg=CLR["panel"])
        row_btns.pack(fill="x", padx=10, pady=8)

        tk.Button(row_btns, text="Ver detalle", bg=CLR["accent"], fg="white",
                  relief="flat", cursor="hand2", width=14,
                  command=self._ver_detalle).pack(side="left", padx=(0, 6))
        tk.Button(row_btns, text="Desactivar cliente", bg=CLR["err"], fg="white",
                  relief="flat", cursor="hand2", width=16,
                  command=self._desactivar).pack(side="left")

        # Detalle
        det = tk.LabelFrame(right, text=" Detalle del cliente seleccionado ",
                            bg=CLR["panel"], font=("Segoe UI", 9, "bold"))
        det.pack(fill="x", pady=(0, 6))
        self.detalle_text = tk.Text(det, height=4, state="disabled",
                                    font=("Consolas", 9), wrap="word",
                                    bg="#FDFEFE", relief="flat")
        self.detalle_text.pack(fill="x", padx=6, pady=6)

        # Log
        log_frame = tk.LabelFrame(right, text=" Registro de operaciones ",
                                  bg=CLR["panel"], font=("Segoe UI", 9, "bold"))
        log_frame.pack(fill="both", expand=True)
        self.log = scrolledtext.ScrolledText(
            log_frame, state="disabled", font=("Consolas", 9), wrap="word", height=14
        )
        self.log.pack(fill="both", expand=True, padx=6, pady=6)
        tk.Button(log_frame, text="Limpiar", command=self._limpiar_log,
                  relief="flat", bg="#ECF0F1").pack(anchor="e", padx=6, pady=(0, 4))

        self._log("Módulo de Clientes listo.")

    # ── Acciones ──────────────────────────────────────────────────────────
    def _registrar(self):
        ced = self.ced_var.get().strip()
        nom = self.nom_var.get().strip()
        ape = self.ape_var.get().strip()
        ema = self.ema_var.get().strip()
        tel = self.tel_var.get().strip()

        try:
            cliente = self.controller.gestor_clientes.registrar(ced, nom, ape, ema, tel)
            self._log(f"+ Cliente registrado: {cliente.obtener_informacion()}")
            log_info(f"Cliente registrado: {cliente.cedula} — {cliente.nombre_completo}")
            self.refrescar_lista()
            self._limpiar_form()
        except SoftwareFJError as exc:
            msg = str(exc)
            self._log(f"✘ Error: {msg}")
            log_error("Error al registrar cliente", exc)
            messagebox.showerror("Error de validación", msg)
        except Exception as exc:
            self._log(f"✘ Error inesperado: {exc}")
            log_error("Error inesperado al registrar cliente", exc)
            messagebox.showerror("Error", str(exc))

    def _ver_detalle(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un cliente de la lista.")
            return
        cedula = self.tree.item(sel[0])["values"][0]
        try:
            cliente = self.controller.gestor_clientes.buscar(str(cedula))
            info = cliente.obtener_informacion()
            self.detalle_text.config(state="normal")
            self.detalle_text.delete("1.0", "end")
            self.detalle_text.insert("end", info)
            self.detalle_text.config(state="disabled")
            self._log(f"ℹ  {info}")
        except SoftwareFJError as exc:
            log_error("Error al buscar cliente", exc)
            messagebox.showerror("Error", str(exc))

    def _desactivar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un cliente de la lista.")
            return
        cedula = self.tree.item(sel[0])["values"][0]
        try:
            cliente = self.controller.gestor_clientes.desactivar(str(cedula))
            self._log(f"⊘  Cliente desactivado: {cliente.nombre_completo}")
            log_info(f"Cliente desactivado: {cliente.cedula}")
            self.refrescar_lista()
        except SoftwareFJError as exc:
            log_error("Error al desactivar cliente", exc)
            messagebox.showerror("Error", str(exc))

    # ── Helpers ───────────────────────────────────────────────────────────
    def refrescar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in self.controller.gestor_clientes.listar():
            self.tree.insert(
                "", "end",
                values=(
                    c.cedula,
                    c.nombre_completo,
                    c.email,
                    "Activo" if c.activo else "Inactivo",
                ),
            )

    def _limpiar_form(self):
        for attr in ("ced_var", "nom_var", "ape_var", "ema_var", "tel_var"):
            getattr(self, attr).set("")

    def _log(self, msg: str):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def _limpiar_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")
