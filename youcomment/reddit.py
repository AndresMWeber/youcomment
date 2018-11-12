from collections import Counter
from os import path
from praw import Reddit
from praw.models import Comment

import youcomment.youtube as yt
import youcomment.conf as conf


class RedditYoutubeBot(Reddit):
    SUBMISSION_TRACKER = Counter()
    CHECKED_POSTS = []
    CHECKED_POST_FILE_PATH = conf.CHECKED_FILE

    def __init__(self, subreddits=None):
        super(RedditYoutubeBot, self).__init__(client_id=conf.REDDIT_CLIENT_ID,
                                               client_secret=conf.REDDIT_CLIENT_SECRET,
                                               username=conf.REDDIT_USER,
                                               password=conf.REDDIT_PASS,
                                               user_agent=conf.REDDIT_AGENT)
        subreddits = subreddits or []
        self.subreddit_list = subreddits or conf.DEFAULT_SUBREDDITS
        self.CHECKED_POSTS.extend(self._get_checked_posts(self.CHECKED_POST_FILE_PATH))

    def run(self, subreddit_list=None):
        submissions = 0
        posts = []
        subreddit_list = subreddit_list or self.subreddit_list
        try:
            for submission in self.subreddit('+'.join(subreddit_list)).stream.submissions(pause_after=2):
                if not submission.id in self.CHECKED_POSTS:
                    self.CHECKED_POSTS.append(submission.id)
                    posts.extend(self.process_post(submission))
                if submissions >= conf.REDDIT_MAXPOSTS:
                    break
                submissions += 1
        except AttributeError:
            pass

        self._write_checked_posts(self.CHECKED_POSTS)
        return posts

    @staticmethod
    def process_post(post):
        try:
            yt.YoutubeVideoBot.parse_url(post.url)
            return [post]
        except IOError:
            pass
        return []

    @staticmethod
    def _get_checked_posts(checked_posts_file_path):
        if path.exists(checked_posts_file_path):
            with open(checked_posts_file_path, 'r') as checked_posts_file:
                return [line for line in checked_posts_file.read().split() if line]
        else:
            return []

    @staticmethod
    def get_top_n_comments(post, num_comments=25):
        comments = [comment for comment in post.comments if isinstance(comment, Comment)]
        comments.sort(key=lambda comment: comment.score, reverse=True)
        return comments[:num_comments]

    def _write_checked_posts(self, posts):
        """ Internal function to write the checked posts to file

        :param posts: list, list of post ids that have been checked
        """
        with open(self.CHECKED_POST_FILE_PATH, 'w') as checked_posts_file:
            checked_posts_file.write('\n'.join(posts))
