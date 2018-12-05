from os import getenv, path
import youcomment.version as version

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
REDDIT_NUM_RETRIES = 3
REDDIT_REPLY_INTERVAL = 600
LOG_FILE = 'youcomment'

# Env Var Settings
YC_LIVE_MODE = getenv('YC_LIVE_MODE', False)
REDDIT_USER = getenv('YC_REDDIT_USER', 'youtube_compare_bot')
REDDIT_AGENT = 'windows:{BOT_USER}:v{V} by /u/{USER}'.format(BOT_USER=REDDIT_USER,
                                                             V=version.__version__,
                                                             USER=REDDIT_AUTHOR_USERNAME)
REDDIT_PASS = getenv('YC_REDDIT_PASS')
REDDIT_CLIENT_ID = getenv('YC_REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = getenv('YC_REDDIT_CLIENT_SECRET')
YOUTUBE_API_KEY = getenv('YC_YOUTUBE_API_KEY')

# Dir Settings
DATA_DIR = 'data'
DB_NAME = 'bot_runtime.db'
__here__ = path.abspath(path.dirname(__file__))
POST_TEMPLATE = path.join(__here__, DATA_DIR, 'post_template.txt')
DB_PATH = path.join(__here__, DATA_DIR, DB_NAME)
