import tkinter as tk
from tkinter import messagebox


class LoginFrame(tk.Frame):
    """Pantalla de inicio de sesión de SoftwareFJ."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # ── Encabezado ────────────────────────────────────────────────────
        tk.Label(
            self,
            text="Software FJ",
            font=("Segoe UI", 28, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1",
        ).pack(pady=(60, 4))

        tk.Label(
            self,
            text="Sistema Integral de Gestión",
            font=("Segoe UI", 13),
            bg="#2C3E50",
            fg="#BDC3C7",
        ).pack(pady=(0, 40))

        # ── Caja de login ─────────────────────────────────────────────────
        box = tk.Frame(self, bg="#34495E", padx=30, pady=30)
        box.pack(ipadx=10, ipady=6)

        tk.Label(box, text="Usuario", font=("Segoe UI", 10), bg="#34495E", fg="#BDC3C7").grid(
            row=0, column=0, sticky="w", pady=(0, 2)
        )
        self.user_var = tk.StringVar()
        entry_user = tk.Entry(
            box, textvariable=self.user_var, width=26,
            font=("Segoe UI", 11), relief="flat",
            bg="#2C3E50", fg="white", insertbackground="white",
        )
        entry_user.grid(row=1, column=0, pady=(0, 14), ipady=4)

        tk.Label(box, text="Contraseña", font=("Segoe UI", 10), bg="#34495E", fg="#BDC3C7").grid(
            row=2, column=0, sticky="w", pady=(0, 2)
        )
        self.pass_var = tk.StringVar()
        entry_pass = tk.Entry(
            box, textvariable=self.pass_var, width=26, show="•",
            font=("Segoe UI", 11), relief="flat",
            bg="#2C3E50", fg="white", insertbackground="white",
        )
        entry_pass.grid(row=3, column=0, pady=(0, 20), ipady=4)

        tk.Button(
            box,
            text="  Ingresar  ",
            font=("Segoe UI", 11, "bold"),
            bg="#2980B9",
            fg="white",
            activebackground="#1F618D",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._login,
        ).grid(row=4, column=0, sticky="ew", ipady=6)

        tk.Label(
            box,
            text="Credenciales: admin / admin",
            font=("Segoe UI", 8),
            bg="#34495E",
            fg="#7F8C8D",
        ).grid(row=5, column=0, pady=(10, 0))

        entry_user.focus_set()
        self.bind_all("<Return>", lambda _e: self._login())

    def _login(self):
        u = self.user_var.get().strip()
        p = self.pass_var.get().strip()
        if u == "admin" and p == "admin":
            self.user_var.set("")
            self.pass_var.set("")
            self.controller.mostrar("MainFrame")
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
