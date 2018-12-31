from os import getenv, path, environ
from pbr.version import VersionInfo
import platform

PROJECT_NAME = 'youcomment'
MANUAL_VERSION = '0.6.6'

try:
    info = VersionInfo(PROJECT_NAME)
except Exception:
    environ['PBR_VERSION'] = MANUAL_VERSION
    info = VersionInfo(PROJECT_NAME)

VERSION = info.version_string()
VERSION_VCS = info.version_string_with_vcs()
PLATFORM = platform.system()

# Modifiable Settings
REDDIT_AUTHOR_USERNAME = 'daemonecles'
DEFAULT_SUBREDDITS = ["you_comment_bot"]
DEFAULT_BOT_RUN_INTERVAL_MINS = 3
SIMILARITY_LIMIT = 0.75
YOUTUBE_COMMENTS_PER_PAGE = 100
YOUTUBE_COMMENTS_MAX_NUM = 500
YOUTUBE_LIKE_THRESHOLD = 3
YOUTUBE_NUM_TOP_COMMENTS = 50
REDDIT_MAX_POSTS = 50
REDDIT_COMMENTS_MAX_NUM = 25
REDDIT_NUM_RETRIES = 3
REDDIT_REPLY_INTERVAL = 60 * 10  # Default is usually 9 minutes, but 10 just in case.
DEV_MODE = 'DEV'
LIVE_MODE = 'LIVE'

# Env Var Settings
YC_LIVE_MODE = getenv('YC_LIVE_MODE', False)
REDDIT_USER = getenv('YC_REDDIT_USER', 'youtube_compare_bot')
AGENT_KWARGS = {'PLAT': PLATFORM, 'BOT': REDDIT_USER, 'V': VERSION_VCS, 'USER': REDDIT_AUTHOR_USERNAME}
REDDIT_AGENT = '{PLAT}:{BOT}:v{V} by /u/{USER}'.format(**AGENT_KWARGS)
REDDIT_PASS = getenv('YC_REDDIT_PASS')
REDDIT_CLIENT_ID = getenv('YC_REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = getenv('YC_REDDIT_CLIENT_SECRET')
YOUTUBE_API_KEY = getenv('YC_YOUTUBE_API_KEY')

# Files
DB_NAME = 'bot_runtime.db'
LOG_FILE = 'youcomment.log'
LOG_CONFIG_FILE = 'log_config.yaml'
TEMPLATE_FILE = 'template.md'

# Paths
DATA_DIR = 'data'
__here__ = path.abspath(path.dirname(__file__))
TEMPLATE_PATH = path.join(__here__, DATA_DIR, TEMPLATE_FILE)
DB_PATH = path.join(__here__, DATA_DIR, DB_NAME)
LOG_PATH = path.join(__here__, DATA_DIR, LOG_FILE)
LOG_CONFIG_PATH = path.join(__here__, DATA_DIR, LOG_CONFIG_FILE)
