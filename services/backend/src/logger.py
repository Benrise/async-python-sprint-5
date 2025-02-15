import json
import logging
import os
import uuid

from config import settings
from logging.handlers import RotatingFileHandler


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', ]

# В логгере настраивается логгирование uvicorn-сервера.
# Про логирование в Python можно прочитать в документации
# https://docs.python.org/3/howto/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'DEBUG',
        },
        'uvicorn.error': {
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}

LOGS_DIR = './logs'

os.makedirs(LOGS_DIR, exist_ok=True)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_message = {
            'message': record.getMessage(),
            'request_id': getattr(record, 'request_id', uuid.uuid4().hex),
            'host': getattr(record, 'host', settings.service_host),
            'method': getattr(record, 'method', None),
            'query_params': getattr(record, 'query_params', None),
            'status_code': getattr(record, 'status_code', None),
            'elapsed_time': getattr(record, 'elapsed_time', None)
        }

        return json.dumps(log_message)


log_file = os.path.join(LOGS_DIR, "logs.log")
max_bytes = 10 * 1024 * 1024
backup_count = 5

logger = logging.getLogger(settings.project_name)
logger.setLevel(logging.INFO)

formatter = JsonFormatter()

rotating_file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
rotating_file_handler.setFormatter(formatter)
rotating_file_handler.setLevel(logging.INFO)

logger.addHandler(rotating_file_handler)