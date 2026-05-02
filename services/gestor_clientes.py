from models.cliente import Cliente
from models.exceptions import ClienteInvalidoError, ParametroFaltanteError, ClienteDuplicadoError


class GestorClientes:
    """Gestiona el ciclo de vida de los clientes en memoria."""

    def __init__(self):
        self._clientes: dict[str, Cliente] = {}

    def registrar(
        self,
        cedula: str,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
    ) -> Cliente:
        """
        Registra un nuevo cliente. Lanza ClienteDuplicadoError si la cédula ya existe.
        Propaga cualquier excepción de validación del modelo.
        """
        if not cedula or not str(cedula).strip():
            raise ParametroFaltanteError("La cédula es requerida para registrar un cliente.")
        cedula_key = str(cedula).strip()
        if cedula_key in self._clientes:
            raise ClienteDuplicadoError(
                f"Ya existe un cliente registrado con cédula '{cedula_key}'."
            )
        cliente = Cliente(cedula, nombre, apellido, email, telefono)
        self._clientes[cedula_key] = cliente
        return cliente

    def buscar(self, cedula: str) -> Cliente:
        """Busca un cliente por cédula. Lanza ClienteInvalidoError si no existe."""
        if not cedula or not str(cedula).strip():
            raise ParametroFaltanteError("La cédula es requerida para buscar un cliente.")
        key = str(cedula).strip()
        if key not in self._clientes:
            raise ClienteInvalidoError(
                f"No se encontró ningún cliente con cédula '{key}'."
            )
        return self._clientes[key]

    def listar(self) -> list[Cliente]:
        """Retorna todos los clientes registrados."""
        return list(self._clientes.values())

    def listar_activos(self) -> list[Cliente]:
        """Retorna únicamente los clientes activos."""
        return [c for c in self._clientes.values() if c.activo]

    def desactivar(self, cedula: str) -> Cliente:
        """Desactiva un cliente sin eliminarlo del sistema."""
        cliente = self.buscar(cedula)
        cliente.desactivar()
        return cliente

    @property
    def total(self) -> int:
        return len(self._clientes)
