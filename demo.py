"""
demo.py — Simulación de al menos 10 operaciones completas para SoftwareFJ.

Demuestra:
  • Registros válidos e inválidos de clientes
  • Creación correcta e incorrecta de servicios
  • Reservas exitosas y fallidas
  • Ciclo completo: crear → confirmar → procesar
  • Manejo de excepciones: try/except, try/except/else, try/except/finally
  • Encadenamiento de excepciones
  • Registro en archivo de log
"""

from models.servicio import SalaReuniones, AlquilerEquipo, Asesoria
from models.excepciones import SoftwareFJError
from utils import log_info, log_error, log_warning


def ejecutar_demo(
    gestor_clientes,
    gestor_servicios,
    gestor_reservas,
    cb=None,
) -> list[str]:
    """
    Ejecuta la secuencia de demostración.

    Args:
        gestor_clientes: instancia de GestorClientes
        gestor_servicios: instancia de GestorServicios
        gestor_reservas: instancia de GestorReservas
        cb: callback opcional str → None para mostrar mensajes en la UI

    Returns:
        Lista de strings con el resumen de cada operación.
    """
    resultados: list[str] = []

    def _ok(msg: str):
        log_info(msg)
        resultados.append(f"  ✔  {msg}")
        if cb:
            cb(f"✔  {msg}")

    def _err(msg: str, exc: Exception = None):
        log_error(msg, exc)
        detalle = f" [{type(exc).__name__}: {exc}]" if exc else ""
        resultados.append(f"  ✘  {msg}{detalle}")
        if cb:
            cb(f"✘  {msg}{detalle}")

    def _sep(titulo: str):
        linea = f"── {titulo} " + "─" * max(0, 50 - len(titulo))
        resultados.append(linea)
        if cb:
            cb(linea)
        log_info(linea)

    # ═══════════════════════════════════════════════════════════════════════
    _sep("OPERACIÓN 1-4: Registro de Clientes")

    # 1 ── Cliente válido ──────────────────────────────────────────────────
    try:
        c1 = gestor_clientes.registrar(
            "10203040", "Carlos", "García", "carlos.garcia@softwarefj.co", "3001234567"
        )
        _ok(f"Cliente registrado: {c1.nombre_completo} (Céd. {c1.cedula})")
    except SoftwareFJError as exc:
        _err("Fallo al registrar Carlos García", exc)

    # 2 ── Cliente válido ──────────────────────────────────────────────────
    try:
        c2 = gestor_clientes.registrar(
            "20304050", "Ana", "López", "ana.lopez@empresa.com", "3109876543"
        )
        _ok(f"Cliente registrado: {c2.nombre_completo} (Céd. {c2.cedula})")
    except SoftwareFJError as exc:
        _err("Fallo al registrar Ana López", exc)

    # 3 ── Cliente inválido: email sin dominio ─────────────────────────────
    try:
        gestor_clientes.registrar(
            "30405060", "Pedro", "Martínez", "pedro.martinez-correo_invalido", "3202222222"
        )
        _err("Se esperaba error por email inválido, pero no se lanzó excepción")
    except SoftwareFJError as exc:
        _err("(Esperado) Email inválido rechazado", exc)

    # 4 ── Cliente inválido: cédula con letras ─────────────────────────────
    try:
        gestor_clientes.registrar(
            "ABCDEF", "Lucía", "Torres", "lucia@correo.com", "3115555555"
        )
        _err("Se esperaba error por cédula con letras, pero no se lanzó excepción")
    except SoftwareFJError as exc:
        _err("(Esperado) Cédula con letras rechazada", exc)

    # ═══════════════════════════════════════════════════════════════════════
    _sep("OPERACIÓN 5-8: Registro de Servicios")

    # 5 ── SalaReuniones válida ────────────────────────────────────────────
    try:
        s1 = SalaReuniones("SALA-A", "Sala Azul", 80_000, capacidad=10)
        gestor_servicios.registrar(s1)
        _ok(f"Servicio registrado: {s1.describir()}")
    except SoftwareFJError as exc:
        _err("Fallo al registrar Sala Azul", exc)

    # 6 ── AlquilerEquipo válido ───────────────────────────────────────────
    try:
        s2 = AlquilerEquipo("EQ-LAPTOP", "Laptop Pro", 25_000, tipo_equipo="laptop", cantidad=3)
        gestor_servicios.registrar(s2)
        _ok(f"Servicio registrado: {s2.describir()}")
    except SoftwareFJError as exc:
        _err("Fallo al registrar Laptop Pro", exc)

    # 7 ── Asesoría válida (nivel experto) ─────────────────────────────────
    try:
        s3 = Asesoria("ASES-TEC", "Asesoría Cloud", 120_000, especialidad="tecnologica", nivel="experto")
        gestor_servicios.registrar(s3)
        _ok(f"Servicio registrado: {s3.describir()}")
    except SoftwareFJError as exc:
        _err("Fallo al registrar Asesoría Cloud", exc)

    # 8 ── Servicio inválido: precio negativo ──────────────────────────────
    try:
        s_malo = SalaReuniones("SALA-X", "Sala Fantasma", -5000, capacidad=10)
        gestor_servicios.registrar(s_malo)
        _err("Se esperaba error por precio negativo, pero no se lanzó excepción")
    except SoftwareFJError as exc:
        _err("(Esperado) Precio negativo rechazado", exc)

    # ═══════════════════════════════════════════════════════════════════════
    _sep("OPERACIÓN 9: Reserva válida → confirmar → procesar")

    # 9 ── Reserva completa (try/except/else) ─────────────────────────────
    try:
        c1_ref = gestor_clientes.buscar("10203040")
        s1_ref = gestor_servicios.buscar("SALA-A")
        r1 = gestor_reservas.crear(c1_ref, s1_ref, duracion_horas=4, con_iva=True, descuento=0.05)
        _ok(f"Reserva creada: {r1.obtener_informacion()}")
    except SoftwareFJError as exc:
        _err("Fallo al crear reserva SALA-A", exc)
        r1 = None

    if r1:
        try:
            r1.confirmar()
        except SoftwareFJError as exc:
            _err("Fallo al confirmar reserva", exc)
        else:
            _ok(f"Reserva {r1.id} confirmada correctamente")

        try:
            r1.procesar()
        except SoftwareFJError as exc:
            _err("Fallo al procesar reserva", exc)
        else:
            _ok(f"Reserva {r1.id} procesada — Costo final: ${r1.costo_total:,.2f}")

    # ═══════════════════════════════════════════════════════════════════════
    _sep("OPERACIÓN 10: Reserva válida → confirmar → cancelar")

    try:
        c2_ref = gestor_clientes.buscar("20304050")
        s2_ref = gestor_servicios.buscar("EQ-LAPTOP")
        r2 = gestor_reservas.crear(c2_ref, s2_ref, duracion_horas=8, con_iva=False, descuento=0.10)
        _ok(f"Reserva creada: {r2.obtener_informacion()}")
        r2.confirmar()
        _ok(f"Reserva {r2.id} confirmada")
        r2.cancelar(motivo="Cliente solicitó cambio de fecha")
        _ok(f"Reserva {r2.id} cancelada correctamente")
    except SoftwareFJError as exc:
        _err("Error en ciclo de reserva EQ-LAPTOP", exc)

    # ═══════════════════════════════════════════════════════════════════════
    _sep("OPERACIÓN 11: Reserva con duración inválida")

    try:
        c1_ref = gestor_clientes.buscar("10203040")
        s3_ref = gestor_servicios.buscar("ASES-TEC")
        # Asesoría máximo 8h; enviar 10h debe fallar
        gestor_reservas.crear(c1_ref, s3_ref, duracion_horas=10)
        _err("Se esperaba error por duración excedida, pero no se lanzó excepción")
    except SoftwareFJError as exc:
        _err("(Esperado) Duración inválida rechazada", exc)

    # ═══════════════════════════════════════════════════════════════════════
    _sep("OPERACIÓN 12: Reserva para servicio no disponible")

    try:
        s1_ref = gestor_servicios.buscar("SALA-A")
        s1_ref.disponible = False
        log_warning("SALA-A marcada como no disponible para prueba de error")

        c1_ref = gestor_clientes.buscar("10203040")
        gestor_reservas.crear(c1_ref, s1_ref, duracion_horas=2)
        _err("Se esperaba error por servicio no disponible, pero no se lanzó excepción")
    except SoftwareFJError as exc:
        _err("(Esperado) Servicio no disponible rechazado", exc)
    finally:
        # Restaurar disponibilidad para uso posterior
        try:
            gestor_servicios.buscar("SALA-A").disponible = True
            log_info("SALA-A restaurada como disponible")
        except SoftwareFJError:
            pass

    # ═══════════════════════════════════════════════════════════════════════
    _sep("OPERACIÓN 13: Cancelar reserva ya procesada")

    try:
        r1_ref = gestor_reservas.buscar("RES-0001")
        r1_ref.cancelar(motivo="Intento indebido")
        _err("Se esperaba ReservaNoPermitidaError al cancelar reserva PROCESADA")
    except SoftwareFJError as exc:
        _err("(Esperado) Cancelación de reserva procesada rechazada", exc)

    # ═══════════════════════════════════════════════════════════════════════
    _sep("OPERACIÓN 14: Reserva con IVA + descuento (cálculo sobrecargado)")

    try:
        c2_ref = gestor_clientes.buscar("20304050")
        s3_ref = gestor_servicios.buscar("ASES-TEC")
        # Sobrecarga Forma 4: calcular_costo(horas, con_iva=True, descuento=0.20)
        r3 = gestor_reservas.crear(c2_ref, s3_ref, duracion_horas=3, con_iva=True, descuento=0.20)
        costo_sin_extras = s3_ref.calcular_costo(3)
        costo_con_iva    = s3_ref.calcular_costo(3, con_iva=True)
        costo_con_desc   = s3_ref.calcular_costo(3, descuento=0.20)
        costo_completo   = s3_ref.calcular_costo(3, con_iva=True, descuento=0.20)
        _ok(
            f"Demostración de sobrecarga calcular_costo — "
            f"Base: ${costo_sin_extras:,.2f} | "
            f"+IVA: ${costo_con_iva:,.2f} | "
            f"-20%: ${costo_con_desc:,.2f} | "
            f"IVA-20%: ${costo_completo:,.2f}"
        )
        r3.confirmar()
        r3.procesar()
        _ok(f"Reserva {r3.id} procesada con IVA y descuento — Total: ${r3.costo_total:,.2f}")
    except SoftwareFJError as exc:
        _err("Error en reserva con IVA + descuento", exc)

    # ═══════════════════════════════════════════════════════════════════════
    _sep("DEMOSTRACIÓN COMPLETADA")
    total = gestor_clientes.total
    total_s = gestor_servicios.total
    total_r = gestor_reservas.total
    resumen = (
        f"Clientes registrados: {total} | "
        f"Servicios en catálogo: {total_s} | "
        f"Reservas totales: {total_r}"
    )
    _ok(resumen)
    log_info(f"Demo finalizada — {resumen}")

    return resultados
