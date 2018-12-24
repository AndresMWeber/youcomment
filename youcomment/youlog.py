import yaml
import os
import logging.config
from youcomment.conf import LOG_CONFIG_PATH, LOG_PATH

if os.path.exists(LOG_CONFIG_PATH):
    with open(LOG_CONFIG_PATH, 'rt') as f:
        DICT_CONFIG = yaml.safe_load(f.read())

    DICT_CONFIG['handlers']['info_file_handler']['filename'] = LOG_PATH

    logging.config.dictConfig(DICT_CONFIG)
else:
    logging.basicConfig(level=logging.INFO)

log = logging.getLogger('youcomment')
