from models.reserva import Reserva, EstadoReserva
from models.excepciones import ReservaInvalidaError, ParametroFaltanteError


class GestorReservas:
    """Gestiona el ciclo de vida de las reservas en memoria."""

    def __init__(self):
        self._reservas: list[Reserva] = []

    def crear(
        self,
        cliente,
        servicio,
        duracion_horas: float,
        con_iva: bool = False,
        descuento: float = 0.0,
    ) -> Reserva:
        """
        Crea y almacena una nueva reserva.
        Propaga todas las excepciones del modelo Reserva.
        """
        reserva = Reserva(cliente, servicio, duracion_horas, con_iva, descuento)
        self._reservas.append(reserva)
        return reserva

    def buscar(self, reserva_id: str) -> Reserva:
        """Busca una reserva por ID. Lanza ReservaInvalidaError si no existe."""
        if not reserva_id or not str(reserva_id).strip():
            raise ParametroFaltanteError("El ID de reserva es requerido.")
        for r in self._reservas:
            if r.id == str(reserva_id).strip().upper():
                return r
        raise ReservaInvalidaError(
            f"No se encontró ninguna reserva con ID '{reserva_id}'."
        )

    def listar(self) -> list[Reserva]:
        """Retorna todas las reservas registradas."""
        return list(self._reservas)

    def listar_por_estado(self, estado: str) -> list[Reserva]:
        """Filtra reservas por estado."""
        return [r for r in self._reservas if r.estado == estado]

    def listar_por_cliente(self, cedula: str) -> list[Reserva]:
        """Filtra reservas por cédula del cliente."""
        return [r for r in self._reservas if r.cliente.cedula == cedula]

    @property
    def total(self) -> int:
        return len(self._reservas)

    @property
    def estados(self):
        return EstadoReserva
