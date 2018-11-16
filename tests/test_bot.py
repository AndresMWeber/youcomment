from tests.basetest import BaseTest
from youcomment.bot import YouCompareBot


class TestBot(BaseTest):
    def test_default_run(self):
        bot = YouCompareBot()
        bot.reddit_bot.CHECKED_POSTS = []
        self.assertEqual([p[0] for p in bot.run()], [1.0, 0.8641975308641975])
        self.assertEqual(len(bot.reddit_bot.CHECKED_POSTS), 3)

    def test_continuous_run(self):
        bot = YouCompareBot()
        bot.reddit_bot.CHECKED_POSTS = []
        bot.reddit_bot.REDDIT_MAX_POSTS = 0
        posts = bot.run()
        self.assertEqual(len(posts), 2)
        self.assertEqual(len(bot.reddit_bot.CHECKED_POSTS), 3)

    def test_short_run(self):
        bot = YouCompareBot()
        bot.reddit_bot.CHECKED_POSTS = []
        bot.reddit_bot.REDDIT_MAX_POSTS = 1
        posts = bot.run()
        self.assertEqual(len(posts), 0)
        self.assertEqual(len(bot.reddit_bot.CHECKED_POSTS), 1)
