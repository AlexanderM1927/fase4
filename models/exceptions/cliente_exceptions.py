from models.exceptions.base import SoftwareFJError


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente son inválidos o inconsistentes."""
    pass


class ClienteDuplicadoError(ClienteInvalidoError):
    """Se lanza al intentar registrar un cliente con cédula ya existente."""
    pass
