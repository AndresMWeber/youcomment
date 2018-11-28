from os import getenv, path
from six import iteritems

import youcomment.version as version

# Modifiable Settings
DEFAULT_SUBREDDITS = ["you_comment_bot"]
SIMILARITY_LIMIT = 0.75
YOUTUBE_COMMENTS_PER_PAGE = 100
YOUTUBE_COMMENTS_MAX_NUM = 500
YOUTUBE_LIKE_THRESHOLD = 3
YOUTUBE_NUM_TOP_COMMENTS = 50
REDDIT_MAX_POSTS = 50
REDDIT_NUM_RETRIES = 3
REDDIT_REPLY_INTERVAL = 600

# Env Var Settings
YC_LIVE_MODE = getenv('YC_LIVE_MODE', False)
REDDIT_AGENT = 'windows:youtube_compare_bot:v%s by /u/daemonecles' % version.__version__
REDDIT_USER = getenv('YC_REDDIT_USER', 'youtube_compare_bot')
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

# Env Var Checks
for k, v in iteritems({'YC_REDDIT_USER': REDDIT_USER,
                       'YC_REDDIT_PASS': REDDIT_PASS,
                       'YC_CLIENT_ID': REDDIT_CLIENT_ID,
                       'YC_CLIENT_SECRET': REDDIT_CLIENT_SECRET,
                       'YC_YOUTUBE_API_KEY': YOUTUBE_API_KEY}):
    if not v:
        EnvironmentError('No environment variable %s' % k)
