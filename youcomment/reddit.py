from praw import Reddit
from praw.models import Comment
from praw.exceptions import APIException
from prawcore.exceptions import OAuthException
import time
import peewee

from youcomment.mixins import BotMixin, ensure_instance_env_var_dependencies
import youcomment.youtube as yt
import youcomment.conf as conf
import youcomment.youlog as youlog
from youcomment.database import RedditPost, Subreddit


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
        self.subreddit_list = self.resolve_subreddit_list(subreddits)
        youlog.log.info('Initializing Reddit Bot with subreddits: %s' % self.subreddit_list)

    def run(self, subreddits=None):
        """ Obtains up to self.REDDIT_MAX_POSTS number of posts from the subreddit_list stream.
            Set self.REDDIT_MAX_POSTS to 0 to run indefinitely.

        :param subreddit_list: list or str, list of subreddit names or just a name
        :return: iter(praw.models.reddit.submission.Submission), generator list of submissions
        """
        post_count = 0
        self.subreddit_list = self.resolve_subreddit_list(subreddits)
        multi_reddit_string = '+'.join(self.subreddit_list)
        youlog.log.info('Scanning multi-reddit: %s' % multi_reddit_string)

        try:
            for post in self.subreddit(multi_reddit_string).stream.submissions(pause_after=2):
                post_count += 1

                if post is None or self.REDDIT_MAX_POSTS != 0 and post_count > self.REDDIT_MAX_POSTS:
                    break

                youlog.log.info('Checking reddit post %s.' % post.id)
                try:
                    RedditPost.get(RedditPost.post_id == post.id)
                except peewee.DoesNotExist:
                    subreddit, _ = Subreddit.get_or_create(name=post.subreddit.display_name)
                    RedditPost.create(post_id=post.id,
                                      subreddit=subreddit,
                                      permalink='http://reddit.com' + post.permalink)
                    processed_post = self.process_post(post)
                    if processed_post:
                        yield processed_post

        except OAuthException as e:
            youlog.log.error('Failed Reddit log in with the account credentials, check your env vars and restart.')
            raise e

    def bot_reply(self, comment_id, body):
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

    @staticmethod
    def process_post(post):
        try:
            yt.YoutubeVideoBot.parse_url(post.url)
            youlog.log.debug('Post %s is YouTube url post...processing.' % post.id)
            return post
        except IOError:
            youlog.log.debug('Post %s is not a YouTube url post...skipping.' % post.id)

    def get_top_comments(self, post):
        comments = [comment for comment in post.comments if isinstance(comment, Comment)]
        comments.sort(key=lambda comment: comment.score, reverse=True)
        return comments[:self.REDDIT_COMMENTS_MAX_NUM]

    @staticmethod
    def resolve_subreddit_list(subreddit_list):
        if isinstance(subreddit_list, str):
            return subreddit_list.split('+')
        elif isinstance(subreddit_list, list):
            return subreddit_list
        else:
            return subreddit_list or conf.DEFAULT_SUBREDDITS
