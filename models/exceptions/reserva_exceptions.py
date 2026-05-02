from models.exceptions.base import SoftwareFJError


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando los datos de una reserva son incorrectos o inconsistentes."""
    pass


class ReservaNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operación no permitida sobre una reserva."""
    pass
