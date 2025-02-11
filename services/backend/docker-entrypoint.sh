#!/bin/bash

# =================================================== #
#       Команды для первого "холодного" запуска       #
#       Вводить один раз вручную в контейнере         #
# =================================================== #

# alembic upgrade head

PORT=${BACKEND_PORT:-8080}

# Запуск в режиме разработки 
exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --reload

# Запуск в режиме производства
# exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:${PORT} main:app