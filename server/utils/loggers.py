import logging
from datetime import datetime
from uvicorn.logging import ColourizedFormatter
from logging.handlers import TimedRotatingFileHandler

ACCESS_LOG_DIR = "logs"


def access_handler_hook():
    handler = TimedRotatingFileHandler(
        # FIXME: log file change
        # filename=ACCESS_LOG_DIR + f"/{datetime.now()}.log",
        filename=ACCESS_LOG_DIR + "/access.log",
        when="midnight",
        interval=1,
        backupCount=1
    )
    console_formatter = ColourizedFormatter("{asctime} - {message}", style="{", use_colors=True)
    handler.setFormatter(console_formatter)

    logger = logging.getLogger("uvicorn.access")
    logger.addHandler(handler)
