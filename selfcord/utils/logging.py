import logging
import logging.config

logging.getLogger("websockets.client").disabled = True
logging.getLogger("urllib3.connectionpool").disabled = True

FMT = "[{asctime}][{levelname:^9}] {name}: {message}"

FORMATS = {
    logging.DEBUG: f"\33[93m{FMT}\33[0m",
    logging.INFO: f"\33[34m{FMT}\33[0m",
    logging.WARNING: f"\33[33m{FMT}\33[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: "\33[31m{message}\33[0m",
}


class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{", datefmt="%H:%M:%S")
        return formatter.format(record)


handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
