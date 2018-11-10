import os
import re

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import youcomment.conf as conf


class YoutubeVideoBot(object):

    def __init__(self, video_url=None):
        self.client = build(conf.YOUTUBE_API_SERVICE_NAME,
                            conf.YOUTUBE_API_VERSION,
                            developerKey=conf.YOUTUBE_API_KEY)
        self.url = video_url        

    def run(self, url=None):
        part = 'snippet,replies'
        try:
            result = self.top_comments(part=part,
                                       maxResults=conf.YOUTUBE_COMMENTS_PER_PAGE,
                                       textFormat="plainText",
                                       key=conf.YOUTUBE_API_KEY,
                                       videoId=self.parse_url(url or self.url))
        except IOError as e:
            raise(e)
        return result

    def gather_comments(self, **kwargs):
        num_comments = 0
        results = self.client.commentThreads().list(**kwargs).execute()
        nextPageToken = results.get('nextPageToken')
        truncated = max(results['pageInfo']['totalResults'] -
                        conf.YOUTUBE_COMMENTS_MAX_NUM, 0)

        while nextPageToken and num_comments < conf.YOUTUBE_COMMENTS_MAX_NUM:
            results.update(self.client.commentThreads().list(
                pageToken=nextPageToken, **kwargs).execute())
            nextPageToken = results.get('nextPageToken')
            num_comments += 20
            
        return results['items']

    def top_comments(self, **kwargs):
        top_ten_comments = []
        for comment in self.gather_comments(**kwargs):
            comment_id = comment['id']
            comment = comment['snippet']['topLevelComment']['snippet']
            if comment['likeCount'] >= conf.YOUTUBE_LIKE_THRESHOLD:
                comment['url'] = conf.YOUTUBE_COMMENT_URL_TEMPLATE.format(URL=kwargs.get('videoId'),
                                                                            COMMENT=comment_id)
                top_ten_comments.append(comment)
        top_ten_comments.sort(key=lambda d: d['likeCount'])
        return top_ten_comments[:10]

    @staticmethod
    def parse_url(url):
        try:
            return re.search(conf.YOUTUBE_URL_VID_ID_REGEX, url).group('id')
        except AttributeError:
            raise IOError('Invalid Youtube link format inputted: %s' % url)
