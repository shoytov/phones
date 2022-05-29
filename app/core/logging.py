import logging
import sys

from app.core.settings import LOGGING_LEVEL, LOGGING_SERIALIZE
from loguru import logger


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    @classmethod
    def make_logger(cls):
        custom_logger = cls.customize_logging(
            level=LOGGING_LEVEL, serialize=LOGGING_SERIALIZE
        )
        return custom_logger

    @classmethod
    def customize_logging(cls, level: str, serialize: bool):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            serialize=serialize,
        )
        logger.add(
            "logs/app.log",
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            serialize=serialize,
        )

        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)


app_logger = CustomizeLogger().make_logger()  # type: ignore
