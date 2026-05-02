import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog

from models.reserva import EstadoReserva
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


class ReservasFrame(tk.Frame):
    """Pestaña de gestión de reservas."""

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
        form = tk.LabelFrame(left, text=" Nueva Reserva ", bg=CLR["panel"],
                             font=("Segoe UI", 9, "bold"))
        form.pack(fill="x")

        def lbl(text):
            tk.Label(form, text=text, bg=CLR["panel"],
                     font=("Segoe UI", 9)).pack(anchor="w", padx=8, pady=(5, 0))

        def ent(var):
            tk.Entry(form, textvariable=var, width=26,
                     font=("Segoe UI", 10)).pack(padx=8, fill="x")

        self.ced_var   = tk.StringVar()
        self.cod_var   = tk.StringVar()
        self.dur_var   = tk.StringVar()
        self.iva_var   = tk.BooleanVar(value=False)
        self.desc_var  = tk.StringVar(value="0")

        lbl("Cédula del cliente:")
        ent(self.ced_var)

        lbl("Código del servicio:")
        ent(self.cod_var)

        lbl("Duración (horas):")
        ent(self.dur_var)

        lbl("Descuento (0.0 – 1.0):")
        ent(self.desc_var)

        tk.Checkbutton(form, text="Incluir IVA (19%)", variable=self.iva_var,
                       bg=CLR["panel"]).pack(anchor="w", padx=8, pady=(6, 0))

        tk.Button(
            form, text="Crear Reserva",
            bg=CLR["accent"], fg="white",
            font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
            command=self._crear,
        ).pack(fill="x", padx=8, pady=8)

        # Lista
        lista = tk.LabelFrame(left, text=" Reservas ", bg=CLR["panel"],
                              font=("Segoe UI", 9, "bold"))
        lista.pack(fill="both", expand=True, pady=(6, 0))

        cols = ("id", "cliente", "servicio", "horas", "costo", "estado")
        self.tree = ttk.Treeview(lista, columns=cols, show="headings", height=10)
        for col, txt, w in [
            ("id",       "ID",        75),
            ("cliente",  "Cliente",   110),
            ("servicio", "Servicio",  100),
            ("horas",    "Horas",      50),
            ("costo",    "Costo",      80),
            ("estado",   "Estado",     80),
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
        ops = tk.LabelFrame(right, text=" Operaciones sobre reserva seleccionada ",
                            bg=CLR["panel"], font=("Segoe UI", 9, "bold"))
        ops.pack(fill="x", pady=(0, 6))

        row1 = tk.Frame(ops, bg=CLR["panel"])
        row1.pack(fill="x", padx=10, pady=(8, 4))

        tk.Button(row1, text="✔ Confirmar", bg=CLR["ok"], fg="white",
                  relief="flat", cursor="hand2", width=13,
                  command=self._confirmar).pack(side="left", padx=(0, 6))
        tk.Button(row1, text="▶ Procesar", bg="#8E44AD", fg="white",
                  relief="flat", cursor="hand2", width=13,
                  command=self._procesar).pack(side="left", padx=(0, 6))
        tk.Button(row1, text="✘ Cancelar", bg=CLR["err"], fg="white",
                  relief="flat", cursor="hand2", width=13,
                  command=self._cancelar).pack(side="left")

        row2 = tk.Frame(ops, bg=CLR["panel"])
        row2.pack(fill="x", padx=10, pady=(0, 8))
        tk.Button(row2, text="ℹ Ver detalle completo", bg=CLR["accent"], fg="white",
                  relief="flat", cursor="hand2",
                  command=self._ver_detalle).pack(side="left")

        # Detalle
        det = tk.LabelFrame(right, text=" Detalle de la reserva seleccionada ",
                            bg=CLR["panel"], font=("Segoe UI", 9, "bold"))
        det.pack(fill="x", pady=(0, 6))
        self.detalle_text = tk.Text(det, height=7, state="disabled",
                                    font=("Consolas", 9), wrap="word",
                                    bg="#FDFEFE", relief="flat")
        self.detalle_text.pack(fill="x", padx=6, pady=6)

        # Log
        log_frame = tk.LabelFrame(right, text=" Registro de operaciones ",
                                  bg=CLR["panel"], font=("Segoe UI", 9, "bold"))
        log_frame.pack(fill="both", expand=True)
        self.log = scrolledtext.ScrolledText(
            log_frame, state="disabled", font=("Consolas", 9), wrap="word", height=8
        )
        self.log.pack(fill="both", expand=True, padx=6, pady=6)
        tk.Button(log_frame, text="Limpiar", command=self._limpiar_log,
                  relief="flat", bg="#ECF0F1").pack(anchor="e", padx=6, pady=(0, 4))

        self._log("Módulo de Reservas listo.")

    # ── Acciones ──────────────────────────────────────────────────────────
    def _crear(self):
        ced     = self.ced_var.get().strip()
        cod     = self.cod_var.get().strip()
        dur_str = self.dur_var.get().strip()
        con_iva = self.iva_var.get()
        desc_str = self.desc_var.get().strip()

        try:
            duracion  = float(dur_str)
            descuento = float(desc_str)
            cliente  = self.controller.gestor_clientes.buscar(ced)
            servicio = self.controller.gestor_servicios.buscar(cod)
            reserva  = self.controller.gestor_reservas.crear(
                cliente, servicio, duracion, con_iva, descuento
            )
            self._log(f"+ Reserva creada: {reserva.obtener_informacion()}")
            log_info(f"Reserva creada: {reserva.id}")
            self.refrescar_lista()
            self._limpiar_form()
        except SoftwareFJError as exc:
            self._log(f"✘ Error: {exc}")
            log_error("Error al crear reserva", exc)
            messagebox.showerror("Error", str(exc))
        except ValueError:
            msg = "Duración y descuento deben ser valores numéricos."
            self._log(f"✘ {msg}")
            log_error(msg)
            messagebox.showerror("Error", msg)
        except Exception as exc:
            self._log(f"✘ Error inesperado: {exc}")
            log_error("Error inesperado al crear reserva", exc)
            messagebox.showerror("Error", str(exc))

    def _get_reserva_seleccionada(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una reserva de la lista.")
            return None
        rid = self.tree.item(sel[0])["values"][0]
        try:
            return self.controller.gestor_reservas.buscar(str(rid))
        except SoftwareFJError as exc:
            messagebox.showerror("Error", str(exc))
            return None

    def _confirmar(self):
        reserva = self._get_reserva_seleccionada()
        if not reserva:
            return
        try:
            reserva.confirmar()
            self._log(f"✔  Reserva {reserva.id} confirmada")
            log_info(f"Reserva {reserva.id} confirmada")
            self.refrescar_lista()
        except SoftwareFJError as exc:
            self._log(f"✘ Error al confirmar: {exc}")
            log_error(f"Error al confirmar {reserva.id}", exc)
            messagebox.showerror("Error", str(exc))

    def _procesar(self):
        reserva = self._get_reserva_seleccionada()
        if not reserva:
            return
        try:
            reserva.procesar()
            self._log(f"▶  Reserva {reserva.id} procesada — Costo: ${reserva.costo_total:,.2f}")
            log_info(f"Reserva {reserva.id} procesada")
            self.refrescar_lista()
        except SoftwareFJError as exc:
            self._log(f"✘ Error al procesar: {exc}")
            log_error(f"Error al procesar {reserva.id}", exc)
            messagebox.showerror("Error", str(exc))

    def _cancelar(self):
        reserva = self._get_reserva_seleccionada()
        if not reserva:
            return
        motivo = simpledialog.askstring(
            "Motivo de cancelación",
            "Ingrese el motivo (opcional):",
            parent=self,
        ) or ""
        try:
            reserva.cancelar(motivo=motivo)
            self._log(f"✘  Reserva {reserva.id} cancelada")
            log_info(f"Reserva {reserva.id} cancelada. Motivo: {motivo}")
            self.refrescar_lista()
        except SoftwareFJError as exc:
            self._log(f"✘ Error al cancelar: {exc}")
            log_error(f"Error al cancelar {reserva.id}", exc)
            messagebox.showerror("Error", str(exc))

    def _ver_detalle(self):
        reserva = self._get_reserva_seleccionada()
        if not reserva:
            return
        detalle = reserva.obtener_detalle()
        self.detalle_text.config(state="normal")
        self.detalle_text.delete("1.0", "end")
        self.detalle_text.insert("end", detalle)
        self.detalle_text.config(state="disabled")
        self._log(f"ℹ  Detalle de {reserva.id} mostrado")

    # ── Helpers ───────────────────────────────────────────────────────────
    def refrescar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in self.controller.gestor_reservas.listar():
            self.tree.insert(
                "", "end",
                values=(
                    r.id,
                    r.cliente.nombre_completo,
                    r.servicio.nombre,
                    r.duracion_horas,
                    f"${r.costo_total:,.2f}",
                    r.estado,
                ),
            )

    def _limpiar_form(self):
        self.ced_var.set("")
        self.cod_var.set("")
        self.dur_var.set("")
        self.desc_var.set("0")
        self.iva_var.set(False)

    def _log(self, msg: str):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def _limpiar_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")
