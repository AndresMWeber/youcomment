import time
from praw import Reddit
from praw.models import Comment
from praw.exceptions import APIException
from prawcore.exceptions import OAuthException

import youcomment.youtube as yt
import youcomment.conf as conf
import youcomment.youlog as youlog
from youcomment.mixins import BotMixin, ensure_instance_env_var_dependencies
from youcomment.database import RedditPost, Subreddit
from youcomment.errors import InvalidYoutubeURL

class RedditBot(Reddit, BotMixin):
    REDDIT_MAX_POSTS = conf.REDDIT_MAX_POSTS
    ENV_VAR_DEPENDENCIES = {'YC_REDDIT_PASS': conf.REDDIT_PASS,
                            'YC_REDDIT_CLIENT_ID': conf.REDDIT_CLIENT_ID,
                            'YC_REDDIT_CLIENT_SECRET': conf.REDDIT_CLIENT_SECRET}
    REDDIT_REPLY_INTERVAL = conf.REDDIT_REPLY_INTERVAL
    REDDIT_NUM_RETRIES = conf.REDDIT_NUM_RETRIES
    REDDIT_COMMENTS_MAX_NUM = conf.REDDIT_COMMENTS_MAX_NUM

    @ensure_instance_env_var_dependencies
    def __init__(self, subreddits=None):
        """

        :param subreddits: list(str), list of subreddits to check
        """
        super(RedditBot, self).__init__(client_id=conf.REDDIT_CLIENT_ID,
                                        client_secret=conf.REDDIT_CLIENT_SECRET,
                                        username=conf.REDDIT_USER,
                                        password=conf.REDDIT_PASS,
                                        user_agent=conf.REDDIT_AGENT)
        self._subreddits = None
        self.subreddit_list = subreddits
        youlog.log.info('Initializing Reddit Bot with subreddits: %s' % self.subreddit_list)

    @property
    def subreddit_list(self):
        return self._subreddits

    @subreddit_list.setter
    def subreddit_list(self, subreddits):
        if subreddits is not None:
            self._subreddits = self.resolve_subreddit_list(subreddits)
        elif self._subreddits is None:
            self._subreddits = conf.DEFAULT_SUBREDDITS

    @property
    def multireddit_str(self):
        return '+'.join(self.subreddit_list)

    def stream(self):
        return self.subreddit(self.multireddit_str).stream.submissions(pause_after=2)

    def get_posts(self, subreddits=None):
        """ Obtains up to self.REDDIT_MAX_POSTS number of posts from the subreddit_list stream.
            Set self.REDDIT_MAX_POSTS to 0 to get_top_comments_from_url indefinitely.  Always detects bans at the start of the get_top_comments_from_url.

        :param subreddit_list: list or str, list of subreddit names or just a name
        :return: iter(praw.models.reddit.submission.Submission), generator list of submissions
        """
        post_count = 0
        self.subreddit_list = subreddits
        self.store_blacklists()

        try:
            youlog.log.info('Scanning multi-reddit: %s' % self.multireddit_str)
            for post in self.stream():
                post_count += 1

                if post is None or self.REDDIT_MAX_POSTS != 0 and post_count > self.REDDIT_MAX_POSTS:
                    break

                youlog.log.info('Checking reddit post %s.' % post.id)

                self.store_post(post)
                if self.post_has_youtube_link(post):
                    yield post

        except OAuthException as e:
            youlog.log.error('Failed Reddit log in with the account credentials, check your env vars and restart.')
            raise e

    def store_post(self, post):
        """ Stores the post and returns True/False depending on if we created a new DB entry.

        :param post: praw.models.Submission, Reddit Post to store in the DB.
        :return: bool, True if new entry was created, False if already exists in the DB.
        """
        subreddit, _ = Subreddit.get_or_create(name=post.subreddit.display_name)
        _, created = RedditPost.get_or_create(post_id=post.id, subreddit=subreddit, permalink=post.permalink)
        return created

    def store_blacklists(self):
        for subreddit in self.get_blacklists():
            subreddit, _ = Subreddit.get_or_create(name=subreddit)
            subreddit.blacklisted = True
            subreddit.save()

    def get_blacklists(self):
        if self.subreddit_list:
            return [subreddit for subreddit in self.subreddit_list if not self.subreddit(subreddit).user_is_banned]
        else:
            return []

    def comment_reply(self, comment_id, body):
        reply = None
        try_again = True
        retries = 0

        comment = self.comment(comment_id)
        youlog.log.info('Found comment from id %s...attempting to reply...' % comment.id)

        while try_again:
            try:
                reply = comment.reply(body)
                youlog.log.info('Reply successful: %s' % reply)

            except APIException:
                youlog.log.warning('Bot reply failed...retrying %d times...' % self.REDDIT_NUM_RETRIES)
                retries += 1
                time.sleep(self.REDDIT_REPLY_INTERVAL)
                try_again = True if retries < self.REDDIT_NUM_RETRIES else False

        return reply or {}

    def get_top_comments(self, post):
        comments = [comment for comment in post.comments if isinstance(comment, Comment)]
        comments.sort(key=lambda comment: comment.score, reverse=True)
        return comments[:self.REDDIT_COMMENTS_MAX_NUM]

    @staticmethod
    def post_has_youtube_link(post):
        try:
            return bool(yt.YoutubeVideoBot.get_video_id_from_url(post.url))
        except InvalidYoutubeURL:
            return False

    @staticmethod
    def resolve_subreddit_list(subreddit_list):
        if isinstance(subreddit_list, str):
            return subreddit_list.split('+')
        elif isinstance(subreddit_list, list):
            return subreddit_list
        else:
            return subreddit_list
