from praw import Reddit
from praw.models import Comment
from prawcore.exceptions import OAuthException
import peewee

from youcomment.mixins import BotMixin, ensure_instance_env_var_dependencies
import youcomment.youtube as yt
import youcomment.conf as conf
import youcomment.youlog as youlog
from youcomment.database import RedditPost, Subreddit


class RedditYoutubeBot(Reddit, BotMixin):
    REDDIT_MAX_POSTS = conf.REDDIT_MAX_POSTS
    ENV_VAR_DEPENDENCIES = {'YC_REDDIT_PASS': conf.REDDIT_PASS,
                            'YC_REDDIT_CLIENT_ID': conf.REDDIT_CLIENT_ID,
                            'YC_REDDIT_CLIENT_SECRET': conf.REDDIT_CLIENT_SECRET}

    @ensure_instance_env_var_dependencies
    def __init__(self, subreddits=None):
        """

        :param subreddits: list(str), list of subreddits to check
        """
        super(RedditYoutubeBot, self).__init__(client_id=conf.REDDIT_CLIENT_ID,
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
                if post:
                    youlog.log.info('Checking reddit post %s.' % post.id)

                post_count += 1

                if post is None or self.REDDIT_MAX_POSTS != 0 and post_count > self.REDDIT_MAX_POSTS:
                    break
                try:
                    RedditPost.get((RedditPost.post_id == post.id) & (not RedditPost.subreddit.blacklisted))

                except peewee.DoesNotExist:
                    subreddit, _ = Subreddit.get_or_create(name=post.subreddit.display_name)
                    RedditPost.create(post_id=post.id, subreddit=subreddit)
                    processed_post = self.process_post(post)
                    if processed_post:
                        yield processed_post

        except OAuthException as e:
            youlog.log.error('Failed Reddit log in with the account credentials, check your env vars and restart.')
            raise e

    def resolve_blacklists(self):
        self.subreddit_list = [subreddit for subreddit in self.subreddit_list if not self.subreddit(subreddit).banned]

    @staticmethod
    def process_post(post):
        try:
            yt.YoutubeVideoBot.parse_url(post.url)
            return post
        except IOError:
            pass

    @staticmethod
    def get_top_n_comments(post, num_comments=25):
        comments = [comment for comment in post.comments if isinstance(comment, Comment)]
        comments.sort(key=lambda comment: comment.score, reverse=True)
        return comments[:num_comments]

    @staticmethod
    def resolve_subreddit_list(subreddit_list):
        if isinstance(subreddit_list, str):
            return subreddit_list.split('+')
        elif isinstance(subreddit_list, list):
            return subreddit_list
        else:
            return subreddit_list or conf.DEFAULT_SUBREDDITS
