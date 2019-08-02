import logging
import sys
import time


IGNORE_MODULES = ["paramiko.transport"]

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAM, WHITE = range(8)

COLORS = {
    "WARNING": YELLOW,
    "INFO": WHITE,
    "DEBUG": BLUE,
    "CRITICAL": RED,
    "ERROR": RED,
    "FATAL": RED,
}

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

BASE_COLOR_FORMAT = "[$BOLD%(system)s$RESET][$BOLD%(subsystem)s$RESET][$BOLD%(name)s$RESET][%(color_levelname)-17s] %(message)s"
BASE_FORMAT = "[%(system)s][%(subsystem)s][%(name)s][%(levelname)s] %(message)s"
EMAIL_FORMAT = (
    "[%(asctime)s][%(system)s][%(subsystem)s][%(name)s][%(levelname)s] %(message)s"
)
DEFAULT_SYSTEM = "yani"
DEFAULT_SUBSYSTEM = "hl"


def supports_color():
    """
  Retuns True if the running system`s terminal supports color, and False
  otherwise.
  """
    unsupported_platform = sys.platform in ("win32", "Pocket PC")
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    if unsupported_platform or not is_a_tty:
        return False
    return True


def color_message(message):
    message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    return message


class ColoredFormatter(logging.Formatter):
    """
  A very basic logging formatter that not only applies color to the levels of
  the output but will also truncate the level names so that they do not alter
  the visuals of logging when presented on the terminal.
  """

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        levelname = record.levelname
        truncated_level = record.levelname[:6]
        levelname_color = (
            COLOR_SEQ % (30 + COLORS[levelname]) + truncated_level + RESET_SEQ
        )
        record.color_levelname = levelname_color
        record.system = logging.system if hasattr(logging, "system") else DEFAULT_SYSTEM
        record.subsystem = (
            logging.subsystem if hasattr(logging, "subsystem") else DEFAULT_SUBSYSTEM
        )
        return logging.Formatter.format(self, record)

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            s = time.strftime("%Y-%m-%d %H:%M:%S", ct)
        return s


def color_format():
    """
  Main entry point to get a colored formatter, it will use the
  BASE_FORMAT by default and fall back to no colors if the system
  does not support it
  """
    str_format = BASE_COLOR_FORMAT if supports_color() else BASE_FORMAT
    color_format = color_message(str_format)
    return ColoredFormatter(color_format)


def email_format():
    str_format = EMAIL_FORMAT
    color_format = color_message(str_format)
    return ColoredFormatter(color_format)


def file_format():
    return email_format()


class IgnoreFilter(logging.Filter):
    def filter(self, record):
        return not record.name in IGNORE_MODULES

