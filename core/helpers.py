import logging
import os
from typing import NewType

import requests

from core.constant import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

LogLevel = NewType("LogLevel", int)


def check_allow_log_level(level: int) -> LogLevel:
    if level in [0, 10, 20]:
        return LogLevel(level)
    raise ValueError("Log level not allow", level)


def configure_logger(logger_name: str, verbose: LogLevel = 0):
    """Настраивает логгер."""
    logger_ = logging.getLogger(logger_name)

    console_handler = logging.StreamHandler()

    console_handler.setLevel(verbose)
    formatter = logging.Formatter(f'%(asctime)s:%(levelname)-5s:%(module)s:%(message)s')
    console_handler.setFormatter(formatter)

    logger_.setLevel(verbose)
    logger_.addHandler(console_handler)


def download_image(url: str, path: str):
    """Скачивает файл.

    :param url: url до файла
    :param path: Путь куда сохранить скачанный файл
    """
    logger.debug(f"Скачивание по ссылке {url}")
    response = requests.get(url)
    response.raise_for_status()

    with open(path, 'wb') as f:
        f.write(response.content)

    logger.debug(f'Скачано и сохранено изображение: {os.path.abspath(path)}')
