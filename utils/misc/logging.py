import logging
import os
import sys
from functools import lru_cache

import arrow


@lru_cache(maxsize=1)
def configure_logging(log_dir: str, log_name: str = 'smart_home', log_level=logging.INFO):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] [%(levelname)s] %(message)s')
    log_file = os.path.join(log_dir, f'log_{arrow.now().format("YYYY-MM-DDTHH_mm")}.log')
    h_file = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    h_screen = logging.StreamHandler(sys.stdout)
    h_file.setFormatter(formatter)
    h_screen.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(h_file)
    root_logger.addHandler(h_screen)
    root_logger.setLevel(log_level)

    logging.getLogger(log_name).debug(f'"{log_name}" loggers configured')


configure_logging('logs')
logger = logging.getLogger('smart_home')
