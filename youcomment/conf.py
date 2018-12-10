from os import getenv, path
import platform
from youcomment.version import __version__

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
REDDIT_REPLY_INTERVAL = 600
DEV_MODE = 'DEV'
LIVE_MODE = 'LIVE'

# Env Var Settings
YC_LIVE_MODE = getenv('YC_LIVE_MODE', False)
REDDIT_USER = getenv('YC_REDDIT_USER', 'youtube_compare_bot')
AGENT_KWARGS = {'PLAT': platform.system(), 'BOT': REDDIT_USER, 'V': __version__, 'USER': REDDIT_AUTHOR_USERNAME}
REDDIT_AGENT = '{PLAT}:{BOT}:v{V} by /u/{USER}'.format(**AGENT_KWARGS)
REDDIT_PASS = getenv('YC_REDDIT_PASS')
REDDIT_CLIENT_ID = getenv('YC_REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = getenv('YC_REDDIT_CLIENT_SECRET')
YOUTUBE_API_KEY = getenv('YC_YOUTUBE_API_KEY')

# Dir Settings
DATA_DIR = 'data'
DB_NAME = 'bot_runtime.db'
LOG_FILE = 'youcomment.log'
TEMPLATE_FILE = 'template.md'

__here__ = path.abspath(path.dirname(__file__))

TEMPLATE_PATH = path.join(__here__, DATA_DIR, TEMPLATE_FILE)
DB_PATH = path.join(__here__, DATA_DIR, DB_NAME)
LOG_PATH = path.join(__here__, DATA_DIR, LOG_FILE)