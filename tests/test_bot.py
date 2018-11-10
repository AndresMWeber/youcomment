from tests.basetest import BaseTest
from youcomment.conf import CHECKED_FILE
from youcomment.bot import YouCompareBot


class TestBot(BaseTest):
    def test_default_run(self):
        bot = YouCompareBot()
        bot.reddit_bot.CHECKED_POSTS = []
        self.assertEqual([p[0] for p in bot.run()], [1.0, 0.8641975308641975])