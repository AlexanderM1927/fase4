import re
from models.entidad import Entidad
from models.excepciones import ClienteInvalidoError, ParametroFaltanteError


class Cliente(Entidad):
    """
    Representa un cliente de SoftwareFJ con datos personales encapsulados
    y validados de forma estricta mediante propiedades.
    """

    def __init__(
        self,
        cedula: str,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
    ):
        # Inicializar atributos privados antes de usar setters
        self._cedula: str = ""
        self._nombre: str = ""
        self._apellido: str = ""
        self._email: str = ""
        self._telefono: str = ""
        self._activo: bool = True

        # Setters realizan todas las validaciones
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono

    # ── Propiedad: cédula ─────────────────────────────────────────────────
    @property
    def cedula(self) -> str:
        return self._cedula

    @cedula.setter
    def cedula(self, value: str):
        if not value or not str(value).strip():
            raise ParametroFaltanteError("La cédula es requerida.")
        v = str(value).strip()
        if not re.match(r"^\d{6,12}$", v):
            raise ClienteInvalidoError(
                f"Cédula inválida: '{v}'. Debe contener entre 6 y 12 dígitos numéricos."
            )
        self._cedula = v

    # ── Propiedad: nombre ─────────────────────────────────────────────────
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        if not value or not str(value).strip():
            raise ParametroFaltanteError("El nombre es requerido.")
        v = str(value).strip()
        if len(v) < 2 or len(v) > 50:
            raise ClienteInvalidoError(
                f"Nombre inválido: '{v}'. Debe tener entre 2 y 50 caracteres."
            )
        self._nombre = v

    # ── Propiedad: apellido ───────────────────────────────────────────────
    @property
    def apellido(self) -> str:
        return self._apellido

    @apellido.setter
    def apellido(self, value: str):
        if not value or not str(value).strip():
            raise ParametroFaltanteError("El apellido es requerido.")
        v = str(value).strip()
        if len(v) < 2 or len(v) > 50:
            raise ClienteInvalidoError(
                f"Apellido inválido: '{v}'. Debe tener entre 2 y 50 caracteres."
            )
        self._apellido = v

    # ── Propiedad: email ──────────────────────────────────────────────────
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not value or not str(value).strip():
            raise ParametroFaltanteError("El email es requerido.")
        v = str(value).strip().lower()
        if not re.match(r"^[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", v):
            raise ClienteInvalidoError(f"Email inválido: '{value}'. Formato esperado: usuario@dominio.com")
        self._email = v

    # ── Propiedad: teléfono ───────────────────────────────────────────────
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, value: str):
        if not value or not str(value).strip():
            raise ParametroFaltanteError("El teléfono es requerido.")
        # Eliminar espacios, guiones y paréntesis antes de validar
        v = re.sub(r"[\s\-()+]", "", str(value).strip())
        if not re.match(r"^\d{7,15}$", v):
            raise ClienteInvalidoError(
                f"Teléfono inválido: '{value}'. Debe tener entre 7 y 15 dígitos."
            )
        self._telefono = v

    # ── Propiedad: activo (solo lectura pública) ──────────────────────────
    @property
    def activo(self) -> bool:
        return self._activo

    # ── Nombre completo (calculado) ───────────────────────────────────────
    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    # ── Métodos de negocio ────────────────────────────────────────────────
    def desactivar(self):
        """Desactiva el cliente (no lo elimina del sistema)."""
        self._activo = False

    def activar(self):
        """Reactiva un cliente previamente desactivado."""
        self._activo = True

    # ── Entidad abstracta ─────────────────────────────────────────────────
    def validar(self) -> bool:
        return bool(self._cedula and self._nombre and self._apellido and self._email and self._telefono)

    def obtener_informacion(self) -> str:
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"[Cliente] {self._nombre} {self._apellido} | "
            f"Cédula: {self._cedula} | Email: {self._email} | "
            f"Tel: {self._telefono} | {estado}"
        )
