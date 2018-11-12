from tests.basetest import BaseTest

from youcomment.reddit import RedditYoutubeBot


class TestRun(BaseTest):
    def test_default_run_valid(self):
        bot = RedditYoutubeBot()
        bot.CHECKED_POSTS = []
        self.assertTrue(bot.run())
