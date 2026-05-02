from datetime import datetime
from models.exceptions import (
    ReservaInvalidaError,
    ReservaNoPermitidaError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class EstadoReserva:
    PENDIENTE  = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA  = "CANCELADA"
    PROCESADA  = "PROCESADA"


class Reserva:
    """
    Integra un Cliente, un Servicio, una duración y un estado.
    Implementa el ciclo de vida: PENDIENTE → CONFIRMADA → PROCESADA
                                 PENDIENTE → CANCELADA
                                 CONFIRMADA → CANCELADA
    Maneja excepciones en confirmar(), cancelar() y procesar() con
    try/except, try/except/else y try/except/finally.
    """

    _contador: int = 0

    def __init__(
        self,
        cliente,
        servicio,
        duracion_horas: float,
        con_iva: bool = False,
        descuento: float = 0.0,
    ):
        # ── Validaciones de parámetros de entrada ─────────────────────────
        if cliente is None:
            raise ParametroFaltanteError("El cliente es requerido para crear una reserva.")
        if servicio is None:
            raise ParametroFaltanteError("El servicio es requerido para crear una reserva.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' ({servicio.codigo}) no está disponible."
            )
        if not cliente.activo:
            raise ReservaInvalidaError(
                f"El cliente '{cliente.nombre_completo}' no está activo."
            )

        # Validación específica del servicio (polimorfismo)
        servicio.validar_parametros(duracion_horas)

        # ── Asignación ────────────────────────────────────────────────────
        Reserva._contador += 1
        self._id: str = f"RES-{Reserva._contador:04d}"
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas: float = float(duracion_horas)
        self._con_iva: bool = bool(con_iva)
        self._descuento: float = float(descuento)
        self._estado: str = EstadoReserva.PENDIENTE
        self._fecha_creacion: datetime = datetime.now()
        self._fecha_modificacion: datetime = datetime.now()
        self._historial: list[str] = [
            f"Creada el {self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
        ]

        # Calcular costo en el momento de la creación
        self._costo_total: float = servicio.calcular_costo(
            duracion_horas, con_iva, descuento
        )

    # ── Propiedades (solo lectura) ────────────────────────────────────────
    @property
    def id(self) -> str:
        return self._id

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion_horas(self) -> float:
        return self._duracion_horas

    @property
    def con_iva(self) -> bool:
        return self._con_iva

    @property
    def descuento(self) -> float:
        return self._descuento

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @property
    def historial(self) -> list:
        return list(self._historial)

    # ── Operaciones de ciclo de vida ──────────────────────────────────────
    def confirmar(self) -> None:
        """
        Confirma la reserva si está en estado PENDIENTE.
        Usa try/except/else para separar el flujo exitoso del manejo de error.
        """
        try:
            if self._estado != EstadoReserva.PENDIENTE:
                raise ReservaNoPermitidaError(
                    f"Solo se pueden confirmar reservas PENDIENTES. "
                    f"Estado actual: '{self._estado}'."
                )
            if not self._cliente.activo:
                raise ReservaInvalidaError(
                    "No se puede confirmar: el cliente no está activo."
                )
        except (ReservaNoPermitidaError, ReservaInvalidaError):
            raise
        except Exception as exc:
            raise ReservaInvalidaError(
                "Error inesperado al validar la confirmación."
            ) from exc
        else:
            # Solo se ejecuta si no hubo excepción en try
            self._estado = EstadoReserva.CONFIRMADA
            self._fecha_modificacion = datetime.now()
            self._historial.append(
                f"Confirmada el {self._fecha_modificacion.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    def cancelar(self, motivo: str = "") -> None:
        """
        Cancela la reserva si no está ya cancelada ni procesada.
        Usa try/except/finally para garantizar registro del intento.
        """
        intento_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            if self._estado == EstadoReserva.CANCELADA:
                raise ReservaNoPermitidaError("La reserva ya está cancelada.")
            if self._estado == EstadoReserva.PROCESADA:
                raise ReservaNoPermitidaError(
                    "No se puede cancelar una reserva que ya fue procesada."
                )
            self._estado = EstadoReserva.CANCELADA
            self._fecha_modificacion = datetime.now()
            nota = (
                f"Cancelada el {self._fecha_modificacion.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            if motivo:
                nota += f" — Motivo: {motivo}"
            self._historial.append(nota)
        except ReservaNoPermitidaError:
            raise
        except Exception as exc:
            raise ReservaInvalidaError(
                "Error inesperado durante la cancelación."
            ) from exc
        finally:
            # Se ejecuta siempre, registra el intento
            _ = intento_ts  # referencia utilizada en logs externos

    def procesar(self) -> None:
        """
        Procesa la reserva si está CONFIRMADA, verificando consistencia del costo.
        Encadena excepciones cuando detecta inconsistencias.
        """
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise ReservaNoPermitidaError(
                    f"Solo se pueden procesar reservas CONFIRMADAS. "
                    f"Estado actual: '{self._estado}'."
                )
            # Recalcular para verificar consistencia (encadenamiento de excepciones)
            try:
                costo_verificado = self._servicio.calcular_costo(
                    self._duracion_horas, self._con_iva, self._descuento
                )
            except Exception as exc:
                raise CalculoInconsistenteError(
                    "No se pudo recalcular el costo para verificación."
                ) from exc

            if abs(costo_verificado - self._costo_total) > 0.01:
                raise CalculoInconsistenteError(
                    f"Inconsistencia detectada: costo original ${self._costo_total:,.2f} "
                    f"vs. recalculado ${costo_verificado:,.2f}."
                )
        except (ReservaNoPermitidaError, CalculoInconsistenteError):
            raise
        except Exception as exc:
            raise ReservaInvalidaError(
                "Error inesperado durante el procesamiento."
            ) from exc
        else:
            self._estado = EstadoReserva.PROCESADA
            self._fecha_modificacion = datetime.now()
            self._historial.append(
                f"Procesada el {self._fecha_modificacion.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    # ── Representación ────────────────────────────────────────────────────
    def obtener_informacion(self) -> str:
        return (
            f"[{self._id}] {self._cliente.nombre_completo} → "
            f"{self._servicio.nombre} | {self._duracion_horas}h | "
            f"${self._costo_total:,.2f} | {self._estado}"
        )

    def obtener_detalle(self) -> str:
        sep = "═" * 52
        lineas = [
            sep,
            f"  Reserva ID  : {self._id}",
            f"  Cliente     : {self._cliente.nombre_completo} (Céd. {self._cliente.cedula})",
            f"  Servicio    : {self._servicio.nombre} [{self._servicio.codigo}]",
            f"  Tipo        : {self._servicio.__class__.__name__}",
            f"  Duración    : {self._duracion_horas} hora(s)",
            f"  Costo total : ${self._costo_total:,.2f}"
            + (" (con IVA 19%)" if self._con_iva else ""),
            f"  Descuento   : {self._descuento * 100:.0f}%",
            f"  Estado      : {self._estado}",
            f"  Creada      : {self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        if self._historial:
            lineas.append(f"  Historial   :")
            for h in self._historial:
                lineas.append(f"    • {h}")
        lineas.append(sep)
        return "\n".join(lineas)
