from abc import abstractmethod
from models.entidad import Entidad
from models.excepciones import (
    ServicioInvalidoError,
    DuracionInvalidaError,
    ParametroFaltanteError,
    CalculoInconsistenteError,
)

# Tasa de IVA colombiana
IVA: float = 0.19


# ══════════════════════════════════════════════════════════════════════════════
class Servicio(Entidad):
    """
    Clase abstracta que representa un servicio ofrecido por SoftwareFJ.
    Implementa polimorfismo mediante métodos abstractos que cada subclase sobreescribe.

    Sobrecarga simulada de calcular_costo():
      Forma 1: calcular_costo(horas)                       → costo base
      Forma 2: calcular_costo(horas, con_iva=True)         → costo con IVA
      Forma 3: calcular_costo(horas, descuento=0.15)       → costo con descuento
      Forma 4: calcular_costo(horas, con_iva=True,
                              descuento=0.10)              → costo completo
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio_base: float,
        disponible: bool = True,
    ):
        if not codigo or not str(codigo).strip():
            raise ParametroFaltanteError("El código del servicio es requerido.")
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es requerido.")
        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise ServicioInvalidoError(
                f"El precio base debe ser un número mayor a 0. Recibido: {precio_base!r}"
            )

        self._codigo: str = str(codigo).strip().upper()
        self._nombre: str = str(nombre).strip()
        self._precio_base: float = float(precio_base)
        self._disponible: bool = bool(disponible)

    # ── Propiedades ───────────────────────────────────────────────────────
    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, value: bool):
        self._disponible = bool(value)

    # ── Métodos abstractos (polimorfismo) ─────────────────────────────────
    @abstractmethod
    def calcular_costo(
        self,
        duracion_horas: float,
        con_iva: bool = False,
        descuento: float = 0.0,
    ) -> float:
        """Calcula el costo total del servicio según duración y parámetros opcionales."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción detallada del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        """Valida que los parámetros sean coherentes con las reglas del servicio."""
        pass

    # ── Helpers protegidos ────────────────────────────────────────────────
    def _validar_duracion(self, duracion_horas: float) -> None:
        if duracion_horas is None:
            raise ParametroFaltanteError("La duración es requerida.")
        if not isinstance(duracion_horas, (int, float)):
            raise DuracionInvalidaError(
                f"La duración debe ser numérica. Recibido: {type(duracion_horas).__name__}"
            )
        if duracion_horas <= 0:
            raise DuracionInvalidaError(
                f"La duración debe ser mayor a 0. Recibido: {duracion_horas}"
            )

    def _aplicar_calculo(
        self, costo_base: float, con_iva: bool, descuento: float
    ) -> float:
        if descuento < 0 or descuento > 1:
            raise ServicioInvalidoError(
                f"El descuento debe estar entre 0.0 y 1.0. Recibido: {descuento}"
            )
        if costo_base < 0:
            raise CalculoInconsistenteError(
                f"El costo base no puede ser negativo. Calculado: {costo_base}"
            )
        costo = costo_base * (1.0 - descuento)
        if con_iva:
            costo *= 1.0 + IVA
        return round(costo, 2)

    # ── Entidad abstracta ─────────────────────────────────────────────────
    def validar(self) -> bool:
        return bool(self._codigo and self._nombre and self._precio_base > 0)

    def obtener_informacion(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[{self.__class__.__name__}] {self._codigo} — {self._nombre} | "
            f"Base: ${self._precio_base:,.2f}/h | {estado}"
        )


# ══════════════════════════════════════════════════════════════════════════════
class SalaReuniones(Servicio):
    """
    Sala de reuniones con capacidad configurable.
    Recargo del 15 % para salas de más de 10 personas.
    Máximo 12 horas continuas.
    """

    CAPACIDADES_VALIDAS = [5, 10, 20, 50]

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio_base: float,
        capacidad: int = 10,
        disponible: bool = True,
    ):
        super().__init__(codigo, nombre, precio_base, disponible)
        if capacidad not in self.CAPACIDADES_VALIDAS:
            raise ServicioInvalidoError(
                f"Capacidad inválida: {capacidad}. "
                f"Valores permitidos: {self.CAPACIDADES_VALIDAS}"
            )
        self._capacidad: int = int(capacidad)

    @property
    def capacidad(self) -> int:
        return self._capacidad

    # Sobrecarga: Forma 1/2/3/4 según parámetros opcionales
    def calcular_costo(
        self,
        duracion_horas: float,
        con_iva: bool = False,
        descuento: float = 0.0,
    ) -> float:
        self._validar_duracion(duracion_horas)
        costo_base = self._precio_base * duracion_horas
        # Recargo por sala grande
        if self._capacidad > 10:
            costo_base *= 1.15
        return self._aplicar_calculo(costo_base, con_iva, descuento)

    def describir(self) -> str:
        return (
            f"Sala de Reuniones '{self._nombre}' | "
            f"Capacidad: {self._capacidad} personas | "
            f"Precio: ${self._precio_base:,.2f}/hora"
            + (" (+15% recargo)" if self._capacidad > 10 else "")
        )

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        self._validar_duracion(duracion_horas)
        if duracion_horas > 12:
            raise ServicioInvalidoError(
                "Las salas no pueden reservarse por más de 12 horas consecutivas."
            )
        return True

    def obtener_informacion(self) -> str:
        return super().obtener_informacion() + f" | Cap: {self._capacidad} personas"


# ══════════════════════════════════════════════════════════════════════════════
class AlquilerEquipo(Servicio):
    """
    Alquiler de equipos tecnológicos.
    Descuento automático del 10 % cuando se alquilan más de 5 unidades.
    Máximo 72 horas por alquiler.
    """

    TIPOS_EQUIPO = ["laptop", "proyector", "camara", "servidor", "tablet"]

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio_base: float,
        tipo_equipo: str = "laptop",
        cantidad: int = 1,
        disponible: bool = True,
    ):
        super().__init__(codigo, nombre, precio_base, disponible)
        tipo = str(tipo_equipo).lower().strip()
        if tipo not in self.TIPOS_EQUIPO:
            raise ServicioInvalidoError(
                f"Tipo de equipo inválido: '{tipo_equipo}'. "
                f"Válidos: {self.TIPOS_EQUIPO}"
            )
        if not isinstance(cantidad, int) or cantidad < 1:
            raise ServicioInvalidoError(
                f"La cantidad debe ser un entero ≥ 1. Recibido: {cantidad}"
            )
        self._tipo_equipo: str = tipo
        self._cantidad: int = cantidad

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @property
    def cantidad(self) -> int:
        return self._cantidad

    # Sobrecarga: Forma 1/2/3/4 según parámetros opcionales
    def calcular_costo(
        self,
        duracion_horas: float,
        con_iva: bool = False,
        descuento: float = 0.0,
    ) -> float:
        self._validar_duracion(duracion_horas)
        costo_base = self._precio_base * duracion_horas * self._cantidad
        # Descuento por volumen (> 5 unidades)
        if self._cantidad > 5:
            costo_base *= 0.90
        return self._aplicar_calculo(costo_base, con_iva, descuento)

    def describir(self) -> str:
        descuento_vol = " (descuento vol. 10%)" if self._cantidad > 5 else ""
        return (
            f"Alquiler de Equipo '{self._nombre}' | "
            f"Tipo: {self._tipo_equipo} | Cantidad: {self._cantidad}{descuento_vol} | "
            f"Precio: ${self._precio_base:,.2f}/hora por unidad"
        )

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        self._validar_duracion(duracion_horas)
        if duracion_horas > 72:
            raise ServicioInvalidoError(
                "Los equipos no pueden alquilarse por más de 72 horas continuas."
            )
        return True

    def obtener_informacion(self) -> str:
        return (
            super().obtener_informacion()
            + f" | {self._tipo_equipo} x{self._cantidad}"
        )


# ══════════════════════════════════════════════════════════════════════════════
class Asesoria(Servicio):
    """
    Asesoría especializada por experto.
    Multiplicador de nivel: junior×1.0 | senior×1.5 | experto×2.2
    Rango permitido: 1–8 horas por sesión.
    """

    ESPECIALIDADES = ["juridica", "financiera", "tecnologica", "administrativa", "marketing"]
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.2}

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio_base: float,
        especialidad: str = "tecnologica",
        nivel: str = "junior",
        disponible: bool = True,
    ):
        super().__init__(codigo, nombre, precio_base, disponible)
        esp = str(especialidad).lower().strip()
        niv = str(nivel).lower().strip()
        if esp not in self.ESPECIALIDADES:
            raise ServicioInvalidoError(
                f"Especialidad inválida: '{especialidad}'. Válidas: {self.ESPECIALIDADES}"
            )
        if niv not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel inválido: '{nivel}'. Válidos: {list(self.NIVELES.keys())}"
            )
        self._especialidad: str = esp
        self._nivel: str = niv

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @property
    def nivel(self) -> str:
        return self._nivel

    # Sobrecarga: Forma 1/2/3/4 según parámetros opcionales
    def calcular_costo(
        self,
        duracion_horas: float,
        con_iva: bool = False,
        descuento: float = 0.0,
    ) -> float:
        self._validar_duracion(duracion_horas)
        multiplicador = self.NIVELES[self._nivel]
        costo_base = self._precio_base * duracion_horas * multiplicador
        return self._aplicar_calculo(costo_base, con_iva, descuento)

    def describir(self) -> str:
        mult = self.NIVELES[self._nivel]
        return (
            f"Asesoría {self._especialidad.capitalize()} | "
            f"Nivel: {self._nivel.capitalize()} (×{mult}) | "
            f"Precio base: ${self._precio_base:,.2f}/hora"
        )

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        self._validar_duracion(duracion_horas)
        if duracion_horas < 1:
            raise ServicioInvalidoError(
                "Las asesorías deben tener una duración mínima de 1 hora."
            )
        if duracion_horas > 8:
            raise ServicioInvalidoError(
                "Las asesorías no pueden durar más de 8 horas por sesión."
            )
        return True

    def obtener_informacion(self) -> str:
        return (
            super().obtener_informacion()
            + f" | {self._especialidad.capitalize()} ({self._nivel})"
        )
