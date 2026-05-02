from models.servicio import Servicio
from models.excepciones import ServicioInvalidoError, ParametroFaltanteError, ServicioDuplicadoError


class GestorServicios:
    """Gestiona el catálogo de servicios de SoftwareFJ en memoria."""

    def __init__(self):
        self._servicios: dict[str, Servicio] = {}

    def registrar(self, servicio: Servicio) -> Servicio:
        """
        Registra un servicio en el catálogo.
        Lanza ServicioDuplicadoError si el código ya existe.
        """
        if servicio is None:
            raise ParametroFaltanteError("El servicio no puede ser None.")
        if servicio.codigo in self._servicios:
            raise ServicioDuplicadoError(
                f"Ya existe un servicio con código '{servicio.codigo}'."
            )
        self._servicios[servicio.codigo] = servicio
        return servicio

    def buscar(self, codigo: str) -> Servicio:
        """Busca un servicio por código. Lanza ServicioInvalidoError si no existe."""
        if not codigo or not str(codigo).strip():
            raise ParametroFaltanteError("El código del servicio es requerido.")
        key = str(codigo).strip().upper()
        if key not in self._servicios:
            raise ServicioInvalidoError(
                f"No se encontró ningún servicio con código '{key}'."
            )
        return self._servicios[key]

    def listar(self) -> list[Servicio]:
        """Retorna todos los servicios del catálogo."""
        return list(self._servicios.values())

    def listar_disponibles(self) -> list[Servicio]:
        """Retorna únicamente los servicios marcados como disponibles."""
        return [s for s in self._servicios.values() if s.disponible]

    def cambiar_disponibilidad(self, codigo: str, disponible: bool) -> Servicio:
        """Activa o desactiva un servicio."""
        servicio = self.buscar(codigo)
        servicio.disponible = disponible
        return servicio

    @property
    def total(self) -> int:
        return len(self._servicios)
