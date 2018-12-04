import logging
from youcomment.conf import LOG_FILE, __here__

logging.basicConfig(level=logging.INFO)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__here__)

fileHandler = logging.FileHandler("{0}/{1}.log".format(__here__, LOG_FILE))
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)