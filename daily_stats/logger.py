# !/usr/bin/env python
# encoding: utf-8

import logging
import os


def get_logger(config, script_name, log_file_name):
    if not os.path.exists(config.log_dir):
        os.mkdir(config.log_dir)
    log_path = os.path.join(config.log_dir, log_file_name)

    logger = logging.getLogger(f'daily_stats.{script_name}')
    logger.setLevel(logging.getLevelName(config.log_level))

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
