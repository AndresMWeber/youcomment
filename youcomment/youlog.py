import logging
from six import iteritems
from youcomment.conf import __here__, LOG_PATH

for name, logger in iteritems(logging.root.manager.loggerDict):
    logger.disabled = True

log = logging.getLogger(__here__)
logging.basicConfig(level=logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s][%(name)s] [%(levelname)-5.5s] - %(message)s")

fileHandler = logging.FileHandler(LOG_PATH)
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# log.addHandler(consoleHandler)
