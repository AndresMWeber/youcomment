from difflib import SequenceMatcher

import time
import praw
import youcomment.conf as conf
import youcomment.reddit as rd
import youcomment.youtube as yt


class YouCompareBot(object):
    reddit_bot = rd.RedditYoutubeBot()
    youtube_bot = yt.YoutubeVideoBot()
    reply_template = ''

    def __init__(self, subreddit=None):
        self.reddit_bot.subreddit_list = subreddit or self.reddit_bot.subreddit_list

        with open(conf.POST_TEMPLATE, 'r') as f:
            self.reply_template = f.read()

    def run(self, subreddit=None):
        """ Runs the bot and makes replies if conf.LIVE is True.
            If conf.REDDIT_NUM_REPLIES set to:
                0 - Runs indefinitely
                int - Runs until the number of posts is checked.

        :param subreddit: list or str, list of subreddit names or just a name
        :return: list(tuple(float, praw.models.reddit.comment.Comment, dict)), list of (similarity, youtube video data, reddit comment)
        """
        subreddit = subreddit if isinstance(subreddit, list) else subreddit
        similar_posts = []

        for post in self.reddit_bot.run(subreddit):
            try:
                youtube_comments = self.youtube_bot.run(post.url)

                for reddit_comment in self.reddit_bot.get_top_n_comments(post):
                    for youtube_comment in youtube_comments:
                        similarity = self.similarity(youtube_comment['textDisplay'], reddit_comment.body)

                        if similarity > conf.SIMILARITY_LIMIT:
                            similar_posts.append((similarity, reddit_comment, youtube_comment))

                self.make_replies(similar_posts)

            except AttributeError:
                continue

        return similar_posts

    def make_replies(self, similar_posts):
        """ The bot will attempt to make replies to the given similar youtube/reddit comments on reddit.

        :param similar_posts: list(tuple(float, praw.models.reddit.comment.Comment, dict))
        """
        if not conf.LIVE:
            return

        try_again = True

        for similar_post in similar_posts:
            value, reddit, youtube = similar_post
            retries = 0

            while try_again:
                try_again = False
                try:
                    reddit.reply(self.reply_template % (100 * round(value, 4), youtube['url']))
                    break
                except praw.exceptions.APIException as e:
                    retries += 1
                    time.sleep(conf.REDDIT_REPLY_INTERVAL)
                    try_again = True if retries < conf.REDDIT_NUM_RETRIES else False

    @staticmethod
    def similarity(str1, str2):
        return SequenceMatcher(None, str1, str2).ratio()


if __name__ == '__main__':
    bot = YouCompareBot()
    bot.run()
