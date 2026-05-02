from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta base que representa cualquier entidad del sistema SoftwareFJ."""

    @abstractmethod
    def obtener_informacion(self) -> str:
        """Retorna una descripción completa de la entidad."""
        pass

    @abstractmethod
    def validar(self) -> bool:
        """Valida que la entidad tenga todos sus datos correctos."""
        pass

    def __str__(self) -> str:
        return self.obtener_informacion()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.obtener_informacion()!r})"
