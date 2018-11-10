from .basetest import BaseTest

from youcomment.reddit import RedditYoutubeBot
from youcomment.config import CHECKED_FILE

class TestRun(BaseTest):
    def test_default_run_valid(self):
        bot = RedditYoutubeBot()
        bot.CHECKED_POSTS = []
        bot.run()
