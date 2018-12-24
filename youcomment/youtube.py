import re
from logging import getLogger, ERROR
from googleapiclient.discovery import build

import youcomment.conf as conf
from youcomment.database import YoutubeVideo
from youcomment.errors import InvalidYoutubeURL
from youcomment.mixins import BotMixin, ensure_instance_env_var_dependencies

getLogger('googleapiclient.discovery').setLevel(ERROR)
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_URL_VID_ID_REGEX = r'(?:(?:v%3D)|(?<=(v|V))(?:=+|/+)|(?<=be)|(?<=(\?|\&)v=)|(?<=embed/))(?:/?)(?P<id>[\w_-]{3,})'
YOUTUBE_URL_TEMPLATE = 'https://www.youtube.com/watch?v={URL}&lc={COMMENT}'

LIKE_COUNT = 'likeCount'
SNIPPET = 'snippet'
REPLIES = 'replies'
TOP_COMMENT = 'topLevelComment'
ID = 'id'
URL = 'url'
ITEMS = 'items'
VIDEO_ID = 'videoId'
TEXT = 'textDisplay'
NEXT_PAGE_TOKEN = 'nextPageToken'
PAGE_TOKEN = 'pageToken'
POSTS_PER_PAGE = 20
POST_PART_QUERY = '{SNIPPET},{REPLIES}'.format(SNIPPET=SNIPPET, REPLIES=REPLIES)
YOUTUBE_KWARGS = {'maxResults': conf.YOUTUBE_COMMENTS_PER_PAGE,
                  'textFormat': "plainText",
                  'key': conf.YOUTUBE_API_KEY,
                  'part': POST_PART_QUERY}


class YoutubeVideoBot(BotMixin):
    ENV_VAR_DEPENDENCIES = {'YC_YOUTUBE_API_KEY': conf.YOUTUBE_API_KEY}

    @ensure_instance_env_var_dependencies
    def __init__(self, video_url=None, cache_discovery=False):
        super(YoutubeVideoBot, self).__init__()
        self.client = None
        self.url = video_url
        self.login(YOUTUBE_API_SERVICE_NAME,
                   YOUTUBE_API_VERSION,
                   developerKey=conf.YOUTUBE_API_KEY,
                   cache_discovery=cache_discovery)

    def login(self, *args, **kwargs):
        self.client = build(*args, **kwargs)

    def get_top_comments_from_url(self, url=None):
        self.url = url or self.url
        video_id = self.get_video_id_from_url(self.url)
        top_comments = self.get_top_comments(videoId=video_id)
        YoutubeVideo.get_or_create(video_id=video_id, video_url=self.url)
        return top_comments

    def get_all_comments(self, **kwargs):
        """ Obtains up to conf.YOUTUBE_COMMENTS_MAX_NUM comments for video at self.url

        """
        num_comments = 0
        comment_tree_result = self.client.commentThreads().list(**kwargs).execute()
        comments = []
        kwargs[PAGE_TOKEN] = comment_tree_result.get(NEXT_PAGE_TOKEN)

        while kwargs[PAGE_TOKEN] and num_comments < conf.YOUTUBE_COMMENTS_MAX_NUM:
            comment_tree_result.update(self.client.commentThreads().list(**kwargs).execute())
            comments.extend(comment_tree_result[ITEMS])
            kwargs[PAGE_TOKEN] = comment_tree_result.get(NEXT_PAGE_TOKEN)
            num_comments += POSTS_PER_PAGE

        return comments

    def get_top_comments(self, **kwargs):
        """ Obtains the top comments (up to conf.YOUTUBE_NUM_TOP_COMMENTS) and stores them in a list

        :return: list(dict), list of YouTube API json data for each comment
        """
        kwargs.update(YOUTUBE_KWARGS)
        top_n_comments = []

        for comment in self.get_all_comments(**kwargs):
            comment_id = comment[ID]
            comment = comment[SNIPPET][TOP_COMMENT][SNIPPET]
            comment[ID] = comment_id
            comment_likes = comment[LIKE_COUNT]

            if comment_likes >= conf.YOUTUBE_LIKE_THRESHOLD:
                comment[URL] = self.build_url(kwargs.get(VIDEO_ID), comment_id)
                top_n_comments.append(comment)

        top_n_comments.sort(key=lambda d: d[LIKE_COUNT], reverse=True)
        return top_n_comments[:conf.YOUTUBE_NUM_TOP_COMMENTS]

    @staticmethod
    def build_url(video_id, comment_id):
        return YOUTUBE_URL_TEMPLATE.format(URL=video_id, COMMENT=comment_id)

    @staticmethod
    def get_video_id_from_url(url):
        try:
            return re.search(YOUTUBE_URL_VID_ID_REGEX, url).group(ID)
        except AttributeError:
            raise InvalidYoutubeURL('The given URL was not a Youtube URL: %s' % url)
