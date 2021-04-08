"""
Implements logging.

.. func:: setup_logging(config_path: pathlib.Path, default_level: Union[int, str] = logging.INFO) -> None
    Setup logging
"""

import logging
import logging.config
import pathlib
from typing import (
    Union
)

import yaml

from ...settings import CORE_DIR
from ... import settings

def setup_logging(config_path: pathlib.Path, default_level: Union[int, str] = logging.INFO) -> None:
    """
    Setup logging.

    :param config_path: path to yaml file config
    :type config_path: pathlib.Path
    :param default_level: logging level that used if config setting is crashed
    :type default_level: Union[int, str]

    :return: None
    :rtype: None
    """

    if config_path.exists():
        with open(config_path, 'r') as config_file:
            try:
                config = yaml.safe_load(config_file.read())

                for handler_name in config['handlers']:
                    if 'file' in handler_name:
                        log_path_from_main_package = config['handlers'][handler_name]['filename']
                        log_path = (CORE_DIR / log_path_from_main_package).resolve()

                        print(settings.PROJECT_DIR)
                        print(settings.CORE_DIR)
                        print(settings.LOGGING_CONFIG_PATH)
                        print(log_path)

                        log_dir_path = log_path.parent

                        print(log_path)
                        
                        log_dir_path.mkdir(parents=True, exist_ok=True)

                logging.config.dictConfig(config)
            except Exception as error:
                raise error
    else:
        logging.basicConfig(level=default_level)

        logging.info('Failed to load the configuration file. Default config is using!')
