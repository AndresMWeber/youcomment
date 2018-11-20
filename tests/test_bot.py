from tests.basetest import BaseTest
from youcomment.bot import YouCompareBot
from youcomment.database import RedditPost, CrossCommentRelationship
from youcomment.conf import DEFAULT_SUBREDDITS
from praw import Reddit


class TestBot(BaseTest):
    def test_default_run(self):
        bot = YouCompareBot()
        bot.run()
        self.assertEqual(
            [c.similarity for c in CrossCommentRelationship.select().where(CrossCommentRelationship.replied == False)],
            [0.7668393782383419, 1.0, 0.993006993006993, 0.8809523809523809])
        self.assertEqual(len(RedditPost.select()),
                         len(list(bot.reddit_bot.subreddit('+'.join(DEFAULT_SUBREDDITS)).top(limit=None))))

    def test_continuous_run(self):
        bot = YouCompareBot()
        bot.reddit_bot.REDDIT_MAX_POSTS = 0
        bot.run()
        self.assertEqual(
            len(CrossCommentRelationship.select().where(CrossCommentRelationship.replied == False)),
            4)
        self.assertEqual(len(RedditPost.select()),
                         len(list(bot.reddit_bot.subreddit('+'.join(DEFAULT_SUBREDDITS)).top(limit=None))))

    def test_short_run(self):
        bot = YouCompareBot()
        bot.reddit_bot.REDDIT_MAX_POSTS = 1
        bot.run()
        self.assertEqual(
            len(CrossCommentRelationship.select().where(CrossCommentRelationship.replied == False)),
            0)
        self.assertEqual(len(RedditPost.select()), 1)
