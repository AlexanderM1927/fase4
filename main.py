import tkinter as tk

from frames.LoginFrame import LoginFrame
from frames.MainFrame  import MainFrame
from services.gestor_clientes  import GestorClientes
from services.gestor_servicios import GestorServicios
from services.gestor_reservas  import GestorReservas
from utils import log_info


class App(tk.Tk):
    """
    Aplicación principal de SoftwareFJ.

    Gestiona la navegación entre frames y mantiene los tres gestores
    de negocio (clientes, servicios, reservas) como estado central.
    """

    def __init__(self):
        super().__init__()
        self.title("Software FJ — Sistema Integral de Gestión")
        self.geometry("1150x680")
        self.resizable(False, False)
        self.configure(bg="#2C3E50")

        # ── Gestores de negocio (estado central) ─────────────────────────
        self.gestor_clientes  = GestorClientes()
        self.gestor_servicios = GestorServicios()
        self.gestor_reservas  = GestorReservas()

        # ── Contenedor de frames ──────────────────────────────────────────
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._frames: dict[str, tk.Frame] = {}
        for FrameClass in (LoginFrame, MainFrame):
            frame = FrameClass(parent=container, controller=self)
            self._frames[FrameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar("LoginFrame")
        log_info("Aplicación SoftwareFJ iniciada")

    def mostrar(self, frame_name: str) -> None:
        """Trae al frente el frame indicado por nombre."""
        self._frames[frame_name].tkraise()

    def logout(self) -> None:
        """Regresa a la pantalla de login."""
        self.mostrar("LoginFrame")
        log_info("Sesión cerrada")


if __name__ == "__main__":
    app = App()
    app.mainloop()
