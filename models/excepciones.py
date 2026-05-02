# ── Excepciones personalizadas del sistema SoftwareFJ ────────────────────────


class SoftwareFJError(Exception):
    """Excepción base del sistema. Toda excepción personalizada hereda de esta."""
    pass


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente son inválidos o inconsistentes."""
    pass


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un servicio son incorrectos."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza al intentar reservar un servicio marcado como no disponible."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando los datos de una reserva son incorrectos o inconsistentes."""
    pass


class ReservaNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operación no permitida sobre una reserva."""
    pass


class DuracionInvalidaError(SoftwareFJError):
    """Se lanza cuando la duración proporcionada no es válida."""
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio en cualquier operación."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce resultados inconsistentes."""
    pass


class ClienteDuplicadoError(ClienteInvalidoError):
    """Se lanza al intentar registrar un cliente con cédula ya existente."""
    pass


class ServicioDuplicadoError(ServicioInvalidoError):
    """Se lanza al intentar registrar un servicio con código ya existente."""
    pass
