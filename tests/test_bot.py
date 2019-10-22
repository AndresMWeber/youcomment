from tests.basetest import BaseTest
from youcomment.bot import YouCompareBot
from youcomment.database import RedditPost, CrossCommentRelationship

TEST_SUBREDDIT = 'test123456123456'


class TestBot(BaseTest):
    def test_default_run(self):
        bot = YouCompareBot(subreddits=TEST_SUBREDDIT)
        bot.run()
        self.assertEqual(sorted([round(n, 1) for n in [c.similarity for c in CrossCommentRelationship.select()]]),
                         sorted([round(n, 1) for n in [0.7668, 0.880952]]))
        self.assertEqual(len(RedditPost.select()),
                         len(list(bot.reddit_bot.subreddit('+'.join([TEST_SUBREDDIT])).top(limit=None))))

    def test_continuous_run(self):
        bot = YouCompareBot(subreddits='test123456123456')
        bot.reddit_bot.REDDIT_MAX_POSTS = 0
        bot.run()
        self.assertEqual(len(CrossCommentRelationship.select()), 2)
        self.assertEqual(len(RedditPost.select()),
                         len(list(bot.reddit_bot.subreddit('+'.join([TEST_SUBREDDIT])).top(limit=None))))

    def test_short_run(self):
        bot = YouCompareBot(subreddits='test123456123456')
        bot.reddit_bot.REDDIT_MAX_POSTS = 1
        bot.run()
        self.assertEqual(len(CrossCommentRelationship.select()), 0)
        self.assertEqual(len(RedditPost.select()), 1)
