# api/logging_config.py
# This file configures JSON logging for the whole FastAPI app

import logging
from pythonjsonlogger import jsonlogger

def setup_logging():
    """
    Configure global JSON logging.
    This will convert all logs (uvicorn, fastapi, print logs)
    into structured JSON logs for Loki.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)

    # Clear old handlers and attach JSON handler
    logger.handlers = []
    logger.addHandler(handler)