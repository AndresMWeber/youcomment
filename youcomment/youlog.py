import logging
from six import iteritems
from youcomment.conf import __here__, LOG_PATH

logging.basicConfig(level=logging.INFO)

for name, logger in iteritems(logging.root.manager.loggerDict):
    logger.disabled=True

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s][%(name)s] [%(levelname)-5.5s] - %(message)s")
log = logging.getLogger(__here__)

fileHandler = logging.FileHandler(LOG_PATH)
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# log.addHandler(consoleHandler)
