import logging
import os

# ── Directorio y archivo de log ───────────────────────────────────────────────
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# ── Configurar logger (sin duplicar handlers en recargas) ─────────────────────
logger = logging.getLogger("SoftwareFJ")
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    _fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    _fh.setLevel(logging.DEBUG)
    _fh.setFormatter(
        logging.Formatter("%(asctime)s  [%(levelname)-8s]  %(message)s",
                          datefmt="%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(_fh)


def log_info(msg: str) -> None:
    logger.info(msg)


def log_error(msg: str, exc: Exception = None) -> None:
    if exc:
        logger.error("%s — %s: %s", msg, type(exc).__name__, exc)
    else:
        logger.error(msg)


def log_warning(msg: str) -> None:
    logger.warning(msg)


def log_debug(msg: str) -> None:
    logger.debug(msg)


def leer_logs() -> str:
    """Lee el archivo de log completo y lo retorna como cadena."""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "(No hay logs disponibles aún)"
    except OSError as exc:
        return f"(Error al leer el archivo de log: {exc})"
