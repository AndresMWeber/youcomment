from collections import Counter
from praw import Reddit
from praw.models import Comment

import youcomment.youtube as yt
import youcomment.conf as conf
from youcomment.database import RedditPost, Subreddit
import peewee


class RedditYoutubeBot(Reddit):
    SUBMISSION_TRACKER = Counter()
    REDDIT_MAX_POSTS = conf.REDDIT_MAX_POSTS

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

    def run(self, subreddits=None):
        """ Obtains up to self.REDDIT_MAX_POSTS number of posts from the subreddit_list stream.
            Set self.REDDIT_MAX_POSTS to 0 to run indefinitely.

        :param subreddit_list: list or str, list of subreddit names or just a name
        :return: iter(praw.models.reddit.submission.Submission), generator list of submissions
        """
        post_count = 0
        self.subreddit_list = self.resolve_subreddit_list(subreddits)

        for post in self.subreddit('+'.join(self.subreddit_list)).stream.submissions(pause_after=2):
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
