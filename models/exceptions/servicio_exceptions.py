from models.exceptions.base import SoftwareFJError


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un servicio son incorrectos."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza al intentar reservar un servicio marcado como no disponible."""
    pass


class ServicioDuplicadoError(ServicioInvalidoError):
    """Se lanza al intentar registrar un servicio con código ya existente."""
    pass
