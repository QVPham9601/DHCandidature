import logging
import os

LOG_DIR = "logs"


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    FORMAT = '[%(asctime)-15s] %(levelname)-6s %(message)s'
    DATE_FORMAT = '%d/%b/%Y %H:%M:%S'
    formatter = logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    if not (os.path.exists(LOG_DIR)):
        os.mkdir(LOG_DIR)
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, "donghanh.log"), encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger
