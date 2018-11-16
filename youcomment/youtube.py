import re
from googleapiclient.discovery import build

import youcomment.conf as conf

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
NEXT_PAGE_TOKEN = 'nextPageToken'
PAGE_TOKEN = 'pageToken'
POSTS_PER_PAGE = 20
POST_PART_QUERY = '{SNIPPET},{REPLIES}'.format(SNIPPET=SNIPPET, REPLIES=REPLIES)
YOUTUBE_KWARGS = {'maxResults': conf.YOUTUBE_COMMENTS_PER_PAGE,
                  'textFormat': "plainText",
                  'key': conf.YOUTUBE_API_KEY,
                  'part': POST_PART_QUERY}


class YoutubeVideoBot(object):

    def __init__(self, video_url=None, cache_discovery=False):
        self.client = None
        self.url = video_url
        self.login(YOUTUBE_API_SERVICE_NAME,
                   YOUTUBE_API_VERSION,
                   developerKey=conf.YOUTUBE_API_KEY,
                   cache_discovery=cache_discovery)

    def login(self, *args, **kwargs):
        self.client = build(*args, **kwargs)

    def run(self, url=None):
        return self.top_comments(videoId=self.parse_url(url or self.url))

    def get_all_comments(self, **kwargs):
        """ Obtains up to conf.YOUTUBE_COMMENTS_MAX_NUM comments for video at self.url

        """
        num_comments = 0
        results = self.client.commentThreads().list(**kwargs).execute()
        kwargs[PAGE_TOKEN] = results.get(NEXT_PAGE_TOKEN)

        while kwargs[PAGE_TOKEN] and num_comments < conf.YOUTUBE_COMMENTS_MAX_NUM:
            results.update(self.client.commentThreads().list(**kwargs).execute())
            kwargs[PAGE_TOKEN] = results.get(NEXT_PAGE_TOKEN)
            num_comments += POSTS_PER_PAGE

        return results[ITEMS]

    def top_comments(self, **kwargs):
        """ Obtains the top comments (up to conf.YOUTUBE_NUM_TOP_COMMENTS) and stores them in a list

        :return: list(dict), list of YouTube API json data for each comment
        """
        kwargs.update(YOUTUBE_KWARGS)
        top_ten_comments = []
        for comment in self.get_all_comments(**kwargs):
            if len(top_ten_comments) == conf.YOUTUBE_NUM_TOP_COMMENTS:
                break
            comment_id = comment[ID]
            comment = comment[SNIPPET][TOP_COMMENT][SNIPPET]
            comment_likes = comment[LIKE_COUNT]

            if comment_likes >= conf.YOUTUBE_LIKE_THRESHOLD:
                comment[URL] = YOUTUBE_URL_TEMPLATE.format(URL=kwargs.get(VIDEO_ID), COMMENT=comment_id)
                top_ten_comments.append(comment)

        top_ten_comments.sort(key=lambda d: d[LIKE_COUNT])
        return top_ten_comments

    @staticmethod
    def parse_url(url):
        try:
            return re.search(YOUTUBE_URL_VID_ID_REGEX, url).group(ID)
        except AttributeError:
            raise IOError('Invalid Youtube link format inputted: %s' % url)
