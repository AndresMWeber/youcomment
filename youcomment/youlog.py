import logging
import os
from youcomment.conf import LOG_FILE, __here__

logging.basicConfig(level=logging.INFO)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__here__)

fileHandler = logging.FileHandler(os.path.join(__here__, "{}.{}".format(LOG_FILE, 'log')))
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)