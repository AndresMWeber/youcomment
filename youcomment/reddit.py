#!/usr/bin/python
from collections import Counter
import re
import random
from os import getenv, path

from youcomment.youtube import YoutubeVideoBot
from youcomment.version import __version__
import youcomment.config as config

import praw
from praw import Reddit


class RedditYoutubeBot(Reddit):
    SUBMISSION_TRACKER = Counter()
    CHECKED_POSTS = []

    def __init__(self, subreddits=None):
        super(RedditYoutubeBot, self).__init__(client_id=config.REDDIT_CLIENT_ID,
                                               client_secret=config.REDDIT_CLIENT_SECRET,
                                               username=config.REDDIT_USER,
                                               password=config.REDDIT_PASS,
                                               user_agent=config.REDDIT_AGENT)
        subreddits = subreddits or []
        self.subreddit_list = subreddits or config.DEFAULT_SUBREDDITS
        self.CHECKED_POSTS.extend(self._get_checked_posts())

    def run(self, subreddit_list=None):
        submissions = 0
        posts = []
        subreddit_list = subreddit_list or self.subreddit_list
        try:
            for submission in self.subreddit('+'.join(subreddit_list)).stream.submissions(pause_after=2):
                if not submission.id in self.CHECKED_POSTS:
                    self.CHECKED_POSTS.append(submission.id)
                    posts.extend(self.process_post(submission))
                if submissions >= config.REDDIT_MAXPOSTS:
                    break
                submissions += 1
        except AttributeError as e:
            pass

        self._write_checked_posts()
        return posts

    def process_post(self, post):
        try:
            YoutubeVideoBot.parse_url(post.url)
            return [post]
        except IOError:
            pass
        return []

    def _get_checked_posts(self):
        if path.exists(config.CHECKED_FILE):
            with open(config.CHECKED_FILE, 'r') as checked_posts_file:
                return [line for line in checked_posts_file.read().split() if line]
        else:
            return []

    def _write_checked_posts(self):
        with open(config.CHECKED_FILE, 'w') as checked_posts_file:
            checked_posts_file.write('\n'.join(self.CHECKED_POSTS))


    @staticmethod
    def get_top_25_comments(post):
        comments = [comment for comment in post.comments if isinstance(comment, praw.models.Comment)]
        comments.sort(key=lambda comment: comment.score, reverse=True)
        return comments[:25] #top 25 comments
