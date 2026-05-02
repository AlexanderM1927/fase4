from models.exceptions.base import SoftwareFJError


class DuracionInvalidaError(SoftwareFJError):
    """Se lanza cuando la duración proporcionada no es válida."""
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio en cualquier operación."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce resultados inconsistentes."""
    pass
