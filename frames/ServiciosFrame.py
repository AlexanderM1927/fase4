import tkinter as tk
from tkinter import ttk, messagebox

from models.exceptions import SoftwareFJError
from utils import log_info, log_error, log_warning
from models.servicio import SalaReuniones, AlquilerEquipo, Asesoria


# Paleta de colores compartida
CLR = {
    "bg":      "#F4F6F7",
    "header":  "#2C3E50",
    "hdr_fg":  "#ECF0F1",
    "accent":  "#2980B9",
    "ok":      "#27AE60",
    "err":     "#C0392B",
    "warn":    "#E67E22",
    "panel":   "#FFFFFF",
}

TIPOS_SERVICIO = ["SalaReuniones", "AlquilerEquipo", "Asesoria"]
TIPOS_EQUIPO   = ["laptop", "proyector", "camara", "servidor", "tablet"]
ESPECIALIDADES = ["juridica", "financiera", "tecnologica", "administrativa", "marketing"]
NIVELES        = ["junior", "senior", "experto"]
CAPACIDADES    = ["5", "10", "20", "50"]


class ServiciosFrame(tk.Frame):
    """Pestaña de gestión del catálogo de servicios."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=CLR["bg"])
        self.controller = controller
        self._build_ui()

    # ── Construcción de la interfaz ───────────────────────────────────────
    def _build_ui(self):
        self._build_left()
        self._build_right()

    def _build_left(self):
        left = tk.Frame(self, bg=CLR["bg"])
        left.pack(side="left", fill="y", padx=(8, 4), pady=8)

        # ── Formulario ──────────────────────────────────────────────────
        form = tk.LabelFrame(left, text=" Nuevo Servicio ", bg=CLR["panel"],
                             font=("Segoe UI", 9, "bold"))
        form.pack(fill="x")

        def lbl(parent, text):
            tk.Label(parent, text=text, bg=CLR["panel"],
                     font=("Segoe UI", 9)).pack(anchor="w", padx=8, pady=(5, 0))

        def entry(parent, var, w=24):
            e = tk.Entry(parent, textvariable=var, width=w, font=("Segoe UI", 10))
            e.pack(padx=8, fill="x")
            return e

        self.tipo_var   = tk.StringVar(value=TIPOS_SERVICIO[0])
        self.cod_var    = tk.StringVar()
        self.nom_var    = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.disp_var   = tk.BooleanVar(value=True)

        lbl(form, "Tipo de servicio:")
        tipo_cb = ttk.Combobox(form, textvariable=self.tipo_var,
                               values=TIPOS_SERVICIO, state="readonly", width=22)
        tipo_cb.pack(padx=8, fill="x")
        tipo_cb.bind("<<ComboboxSelected>>", self._on_tipo_change)

        lbl(form, "Código:")
        entry(form, self.cod_var)

        lbl(form, "Nombre:")
        entry(form, self.nom_var)

        lbl(form, "Precio base ($/hora):")
        entry(form, self.precio_var)

        # ── Extra dinámico ───────────────────────────────────────────────
        self._extra_frame = tk.Frame(form, bg=CLR["panel"])
        self._extra_frame.pack(fill="x")
        self._build_extras_sala()

        tk.Checkbutton(form, text="Disponible", variable=self.disp_var,
                       bg=CLR["panel"]).pack(anchor="w", padx=8, pady=(6, 0))

        tk.Button(form, text="Agregar Servicio", bg=CLR["accent"], fg="white",
                  font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
                  command=self._agregar).pack(fill="x", padx=8, pady=8)

        # ── Lista de servicios ───────────────────────────────────────────
        lista = tk.LabelFrame(left, text=" Catálogo ", bg=CLR["panel"],
                              font=("Segoe UI", 9, "bold"))
        lista.pack(fill="both", expand=True, pady=(6, 0))

        cols = ("codigo", "tipo", "nombre", "precio", "disp")
        self.tree = ttk.Treeview(lista, columns=cols, show="headings", height=10)
        for col, txt, w in [
            ("codigo", "Código",     80),
            ("tipo",   "Tipo",      120),
            ("nombre", "Nombre",    120),
            ("precio", "$/hora",     80),
            ("disp",   "Estado",     80),
        ]:
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w, anchor="center")
        sb = ttk.Scrollbar(lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        sb.pack(side="right", fill="y", pady=5)

    def _build_extras_sala(self):
        for w in self._extra_frame.winfo_children():
            w.destroy()
        self.cap_var = tk.StringVar(value="10")
        tk.Label(self._extra_frame, text="Capacidad (personas):",
                 bg=CLR["panel"], font=("Segoe UI", 9)).pack(anchor="w", padx=8, pady=(5, 0))
        ttk.Combobox(self._extra_frame, textvariable=self.cap_var,
                     values=CAPACIDADES, state="readonly", width=22
                     ).pack(padx=8, fill="x")

    def _build_extras_equipo(self):
        for w in self._extra_frame.winfo_children():
            w.destroy()
        self.equipo_var = tk.StringVar(value="laptop")
        self.cant_var   = tk.StringVar(value="1")
        tk.Label(self._extra_frame, text="Tipo de equipo:",
                 bg=CLR["panel"], font=("Segoe UI", 9)).pack(anchor="w", padx=8, pady=(5, 0))
        ttk.Combobox(self._extra_frame, textvariable=self.equipo_var,
                     values=TIPOS_EQUIPO, state="readonly", width=22
                     ).pack(padx=8, fill="x")
        tk.Label(self._extra_frame, text="Cantidad:",
                 bg=CLR["panel"], font=("Segoe UI", 9)).pack(anchor="w", padx=8, pady=(5, 0))
        tk.Entry(self._extra_frame, textvariable=self.cant_var,
                 width=24, font=("Segoe UI", 10)).pack(padx=8, fill="x")

    def _build_extras_asesoria(self):
        for w in self._extra_frame.winfo_children():
            w.destroy()
        self.esp_var   = tk.StringVar(value="tecnologica")
        self.nivel_var = tk.StringVar(value="junior")
        tk.Label(self._extra_frame, text="Especialidad:",
                 bg=CLR["panel"], font=("Segoe UI", 9)).pack(anchor="w", padx=8, pady=(5, 0))
        ttk.Combobox(self._extra_frame, textvariable=self.esp_var,
                     values=ESPECIALIDADES, state="readonly", width=22
                     ).pack(padx=8, fill="x")
        tk.Label(self._extra_frame, text="Nivel del asesor:",
                 bg=CLR["panel"], font=("Segoe UI", 9)).pack(anchor="w", padx=8, pady=(5, 0))
        ttk.Combobox(self._extra_frame, textvariable=self.nivel_var,
                     values=NIVELES, state="readonly", width=22
                     ).pack(padx=8, fill="x")

    def _on_tipo_change(self, _event=None):
        tipo = self.tipo_var.get()
        if tipo == "SalaReuniones":
            self._build_extras_sala()
        elif tipo == "AlquilerEquipo":
            self._build_extras_equipo()
        else:
            self._build_extras_asesoria()

    def _build_right(self):
        right = tk.Frame(self, bg=CLR["bg"])
        right.pack(side="left", fill="both", expand=True, padx=(4, 8), pady=8)

        # ── Panel de operaciones ─────────────────────────────────────────
        ops = tk.LabelFrame(right, text=" Operaciones ", bg=CLR["panel"],
                            font=("Segoe UI", 9, "bold"))
        ops.pack(fill="x", pady=(0, 6))

        btn_row = tk.Frame(ops, bg=CLR["panel"])
        btn_row.pack(fill="x", padx=10, pady=8)

        tk.Button(btn_row, text="Ver descripción", bg=CLR["accent"], fg="white",
                  relief="flat", cursor="hand2", width=16,
                  command=self._ver_descripcion).pack(side="left", padx=(0, 6))
        tk.Button(btn_row, text="Activar / Desactivar", bg=CLR["warn"], fg="white",
                  relief="flat", cursor="hand2", width=18,
                  command=self._toggle_disponibilidad).pack(side="left", padx=(0, 6))

        # ── Detalle ──────────────────────────────────────────────────────
        det = tk.LabelFrame(right, text=" Detalle del servicio seleccionado ",
                            bg=CLR["panel"], font=("Segoe UI", 9, "bold"))
        det.pack(fill="x", pady=(0, 6))

        self.detalle_text = tk.Text(det, height=4, state="disabled",
                                    font=("Consolas", 9), wrap="word",
                                    bg="#FDFEFE", relief="flat")
        self.detalle_text.pack(fill="x", padx=6, pady=6)

        # ── Log de operaciones ───────────────────────────────────────────
        from tkinter import scrolledtext
        log_frame = tk.LabelFrame(right, text=" Registro de operaciones ",
                                  bg=CLR["panel"], font=("Segoe UI", 9, "bold"))
        log_frame.pack(fill="both", expand=True)

        self.log = scrolledtext.ScrolledText(
            log_frame, state="disabled", font=("Consolas", 9), wrap="word", height=14
        )
        self.log.pack(fill="both", expand=True, padx=6, pady=6)
        tk.Button(log_frame, text="Limpiar", command=self._limpiar_log,
                  relief="flat", bg="#ECF0F1").pack(anchor="e", padx=6, pady=(0, 4))

        self._log("Módulo de Servicios listo.")

    # ── Acciones ──────────────────────────────────────────────────────────
    def _agregar(self):
        tipo   = self.tipo_var.get()
        codigo = self.cod_var.get().strip()
        nombre = self.nom_var.get().strip()
        precio_str = self.precio_var.get().strip()
        disp   = self.disp_var.get()

        try:
            if not codigo:
                raise Exception("El código es obligatorio.")
            if not nombre:
                raise Exception("El nombre es obligatorio.")
            precio = float(precio_str)

            if tipo == "SalaReuniones":
                cap = int(self.cap_var.get())
                svc = SalaReuniones(codigo, nombre, precio, capacidad=cap, disponible=disp)
            elif tipo == "AlquilerEquipo":
                equipo = self.equipo_var.get()
                cant   = int(self.cant_var.get())
                svc = AlquilerEquipo(codigo, nombre, precio, tipo_equipo=equipo,
                                     cantidad=cant, disponible=disp)
            else:
                esp   = self.esp_var.get()
                nivel = self.nivel_var.get()
                svc = Asesoria(codigo, nombre, precio, especialidad=esp,
                               nivel=nivel, disponible=disp)

            self.controller.gestor_servicios.registrar(svc)
            self._log(f"+ Servicio registrado: {svc.obtener_informacion()}")
            log_info(f"Servicio registrado: {svc.codigo} — {svc.nombre}")
            self.refrescar_lista()
            self._limpiar_form()

        except SoftwareFJError as exc:
            msg = str(exc)
            self._log(f"✘ Error: {msg}")
            log_error("Error al registrar servicio", exc)
            messagebox.showerror("Error de validación", msg)
        except ValueError:
            msg = f"El precio debe ser un número válido. Recibido: '{precio_str}'"
            self._log(f"✘ {msg}")
            log_error(msg)
            messagebox.showerror("Error", msg)
        except Exception as exc:
            self._log(f"✘ Error inesperado: {exc}")
            log_error("Error inesperado al registrar servicio", exc)
            messagebox.showerror("Error", str(exc))

    def _ver_descripcion(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un servicio de la lista.")
            return
        codigo = self.tree.item(sel[0])["values"][0]
        try:
            svc = self.controller.gestor_servicios.buscar(str(codigo))
            desc = svc.describir()
            info = svc.obtener_informacion()
            self.detalle_text.config(state="normal")
            self.detalle_text.delete("1.0", "end")
            self.detalle_text.insert("end", f"{desc}\n\n{info}")
            self.detalle_text.config(state="disabled")
            self._log(f"ℹ  {desc}")
        except SoftwareFJError as exc:
            log_error("Error al buscar servicio", exc)
            messagebox.showerror("Error", str(exc))

    def _toggle_disponibilidad(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un servicio de la lista.")
            return
        codigo = self.tree.item(sel[0])["values"][0]
        try:
            svc = self.controller.gestor_servicios.buscar(str(codigo))
            nuevo = not svc.disponible
            self.controller.gestor_servicios.cambiar_disponibilidad(str(codigo), nuevo)
            estado = "disponible" if nuevo else "no disponible"
            self._log(f"↔  {svc.nombre} marcado como {estado}")
            log_info(f"Servicio {svc.codigo} cambiado a {estado}")
            self.refrescar_lista()
        except SoftwareFJError as exc:
            log_error("Error al cambiar disponibilidad", exc)
            messagebox.showerror("Error", str(exc))

    # ── Helpers ───────────────────────────────────────────────────────────
    def refrescar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for svc in self.controller.gestor_servicios.listar():
            self.tree.insert(
                "", "end",
                values=(
                    svc.codigo,
                    svc.__class__.__name__,
                    svc.nombre,
                    f"${svc.precio_base:,.0f}",
                    "✔ Sí" if svc.disponible else "✘ No",
                ),
            )

    def _limpiar_form(self):
        self.cod_var.set("")
        self.nom_var.set("")
        self.precio_var.set("")

    def _log(self, msg: str):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def _limpiar_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")
