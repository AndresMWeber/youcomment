from os import getenv, environ, path
from six import iteritems

import youcomment.version as version


__here__ = path.abspath(path.dirname(__file__))
DEFAULT_SUBREDDITS = ["test123456123456"]
CHECKED_FILE = path.join(__here__, 'checked.txt')
POST_TEMPLATE = path.join(__here__, 'post_template.txt')
SIMILARITY_LIMIT = 0.85

REDDIT_AGENT = 'windows:youtube_compare_bot:v%s by /u/daemonecles' % version.__version__
REDDIT_USER = getenv('YC_REDDIT_USER', 'youtube_compare_bot')
REDDIT_PASS = getenv('YC_REDDIT_PASS')
REDDIT_CLIENT_ID = getenv('YC_REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = getenv('YC_REDDIT_CLIENT_SECRET')
REDDIT_MAXPOSTS = 50
WAIT = 30

YOUTUBE_API_KEY = getenv('YC_YOUTUBE_API_KEY')
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_URL_VID_ID_REGEX = r'(?:(?:v%3D)|(?<=(v|V))(?:=+|/+)|(?<=be)|(?<=(\?|\&)v=)|(?<=embed/))(?:/?)(?P<id>[\w_-]{3,})'
YOUTUBE_COMMENT_URL_TEMPLATE = 'https://www.youtube.com/watch?v={URL}&lc={COMMENT}'
YOUTUBE_COMMENTS_PER_PAGE = 100
YOUTUBE_COMMENTS_MAX_NUM = 1000
YOUTUBE_LIKE_THRESHOLD = 3


ENV = {'YC_REDDIT_USER': REDDIT_USER,
       'YC_REDDIT_PASS': REDDIT_PASS,
       'YC_CLIENT_ID': REDDIT_CLIENT_ID,
       'YC_CLIENT_SECRET': REDDIT_CLIENT_SECRET,
       'YC_YOUTUBE_API_KEY': YOUTUBE_API_KEY}

for k, v in iteritems(ENV):
    if not v:
        EnvironmentError('No environment variable %s' % k)
