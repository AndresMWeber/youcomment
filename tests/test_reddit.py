import os
from tests.basetest import BaseTest
from youcomment.reddit import RedditYoutubeBot
from youcomment.errors import EnvironmentError


class TestRun(BaseTest):
    def test_default_run_valid(self):
        bot = RedditYoutubeBot()
        bot.CHECKED_POSTS = []
        self.assertTrue(bot.run())

    def test_env_var_checking(self):
        for key in list(RedditYoutubeBot.ENV_VAR_DEPENDENCIES):
            reddit_pass = os.getenv(key)
            os.environ[key] = ''
            with self.assertRaises(EnvironmentError):
                RedditYoutubeBot()
            os.environ[key] = reddit_pass
