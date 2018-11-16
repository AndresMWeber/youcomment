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
    REDDIT_MAX_POSTS = conf.REDDIT_MAX_POSTS

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
        """ Obtains up to self.REDDIT_MAX_POSTS number of posts from the subreddit_list stream.
            Set self.REDDIT_MAX_POSTS to 0 to run indefinitely.

        :param subreddit_list: list or str, list of subreddit names or just a name
        :return: iter(praw.models.reddit.submission.Submission), generator list of submissions
        """
        submission_count = 0
        subreddit_list = subreddit_list or self.subreddit_list

        try:
            for submission in self.subreddit('+'.join(subreddit_list)).stream.submissions(pause_after=2):
                submission_count += 1

                if submission is None or self.REDDIT_MAX_POSTS != 0 and submission_count > self.REDDIT_MAX_POSTS:
                    print(submission_count, self.REDDIT_MAX_POSTS)
                    break

                if not submission.id in self.CHECKED_POSTS:
                    self.CHECKED_POSTS.append(submission.id)
                    print(self.subreddit('+'.join(subreddit_list)).banned())
                    with open(self.CHECKED_POST_FILE_PATH, 'a') as checked_posts_file:
                        checked_posts_file.write('\n'.join(submission.id))

                    yield self.process_post(submission)

        except AttributeError:
            pass


    @staticmethod
    def process_post(post):
        try:
            yt.YoutubeVideoBot.parse_url(post.url)
            return post
        except IOError:
            pass

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

