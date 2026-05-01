"""
plasma_checker.logger
~~~~~~~~~~~~~~~~~~~~~
Centralised logging for the plasma_checker wrapper and test suite.

Usage (wrapper):
    from logger import get_logger
    log = get_logger("plasma_checker")
    log.info("Starting run")

Usage (tests):
    from logger import get_logger
    log = get_logger(__name__)          # e.g. "tests.test_login"
    log.step("Filling login form")
    log.info("Navigating to dashboard")
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


# ── Custom level: STEP ────────────────────────────────────────────────────────
# Sits between INFO (20) and WARNING (30) — used to mark high-level test steps.
STEP_LEVEL = 25
logging.addLevelName(STEP_LEVEL, "STEP")


def _step(self: logging.Logger, message: str, *args, **kwargs) -> None:
    if self.isEnabledFor(STEP_LEVEL):
        self._log(STEP_LEVEL, message, args, **kwargs)


logging.Logger.step = _step  # type: ignore[attr-defined]


# ── Formatters ────────────────────────────────────────────────────────────────

class ConsoleFormatter(logging.Formatter):
    """Coloured, human-readable output for the terminal."""

    LEVEL_COLOURS = {
        logging.DEBUG:    "\033[37m",       # grey
        logging.INFO:     "\033[36m",       # cyan
        STEP_LEVEL:       "\033[35;1m",     # bold magenta
        logging.WARNING:  "\033[33m",       # yellow
        logging.ERROR:    "\033[31m",       # red
        logging.CRITICAL: "\033[31;1m",     # bold red
    }
    RESET = "\033[0m"
    LEVEL_WIDTH = 8  # pads level names to a fixed width

    def format(self, record: logging.LogRecord) -> str:
        colour = self.LEVEL_COLOURS.get(record.levelno, "")
        level  = f"{record.levelname:<{self.LEVEL_WIDTH}}"
        name   = f"{record.name}"
        msg    = record.getMessage()

        # Include exception info if present
        if record.exc_info:
            msg += "\n" + self.formatException(record.exc_info)

        return f"{colour}[{level}]{self.RESET} {name}: {msg}"


class FileFormatter(logging.Formatter):
    """Structured, timestamped lines suitable for log files and CI artefacts."""

    FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    DATEFMT = "%Y-%m-%d %H:%M:%S"

    def __init__(self) -> None:
        super().__init__(fmt=self.FORMAT, datefmt=self.DATEFMT)


# ── Root logger factory ───────────────────────────────────────────────────────

_configured = False  # guard against double-initialisation


def configure_logging(
    level: str | int = "INFO",
    log_dir: str | Path | None = "logs",
    log_filename: str | None = None,
) -> None:
    """
    Call once at program startup (plasma_checker.py main()).

    Args:
        level:        Minimum log level — "DEBUG", "INFO", "STEP", "WARNING", etc.
        log_dir:      Directory for log files. Pass None to disable file logging.
        log_filename: Override the auto-generated filename (e.g. "run.log").
    """
    global _configured
    if _configured:
        return
    _configured = True

    root = logging.getLogger("plasma_checker")
    root.setLevel(level if isinstance(level, int) else logging.getLevelName(level))
    root.propagate = False

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ConsoleFormatter())
    root.addHandler(console_handler)

    # File handler (optional)
    if log_dir is not None:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        if log_filename is None:
            timestamp    = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"plasma_{timestamp}.log"

        file_handler = logging.FileHandler(log_path / log_filename, encoding="utf-8")
        file_handler.setFormatter(FileFormatter())
        root.addHandler(file_handler)

        # Log the file location so it's easy to find after a run
        root.info("Log file: %s", log_path / log_filename)


def get_logger(name: str) -> logging.Logger:
    """
    Return a child logger under the 'plasma_checker' hierarchy.

    Args:
        name: Typically __name__ inside a module or test file.
               Leading 'plasma_checker.' is stripped to avoid duplication.

    Returns:
        A Logger that inherits handlers & level from the root plasma logger.
    """
    # Normalise: strip leading package name if already present
    if name.startswith("plasma_checker."):
        child_name = name
    else:
        # Strip any leading path separators from pytest node IDs
        short = name.lstrip("./").replace("/", ".").replace("\\", ".")
        child_name = f"plasma_checker.{short}"

    return logging.getLogger(child_name)
