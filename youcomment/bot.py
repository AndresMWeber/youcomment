from difflib import SequenceMatcher
import time
import praw

import youcomment.youlog as youlog
import youcomment.reddit as rd
import youcomment.youtube as yt
import youcomment.conf as conf
from youcomment.database import (CrossCommentRelationship,
                                 YoutubeComment,
                                 RedditPost,
                                 RedditComment,
                                 YoutubeVideo,
                                 init_db)


class YouCompareBot(object):
    post_template_file = conf.POST_TEMPLATE
    reply_template = ''

    LIVE = conf.YC_LIVE_MODE
    SIMILARITY_LIMIT = conf.SIMILARITY_LIMIT
    REDDIT_REPLY_INTERVAL = conf.REDDIT_REPLY_INTERVAL
    REDDIT_NUM_RETRIES = conf.REDDIT_NUM_RETRIES

    def __init__(self, subreddits=None):
        init_db()
        self.reddit_bot = rd.RedditYoutubeBot()
        self.youtube_bot = yt.YoutubeVideoBot()
        self.reddit_bot.subreddit_list = subreddits or self.reddit_bot.subreddit_list

        with open(self.post_template_file, 'r') as f:
            self.reply_template = f.read()

    def run(self, subreddits=None):
        """ Runs the bot and makes replies if conf.LIVE is True.
            If conf.REDDIT_NUM_REPLIES set to:
                0 - Runs indefinitely
                int - Runs until the number of posts is checked.

        :param subreddits: list or str, list of subreddit names or just a name
        :return: list(tuple(float, praw.models.reddit.comment.Comment, dict)), list of (similarity, youtube video data, reddit comment)
        """
        youlog.log.info('Initializing run of %s.' % self)

        subreddits = rd.RedditYoutubeBot.resolve_subreddit_list(subreddits or self.reddit_bot.subreddit_list)
        similar_posts = []

        for post in self.reddit_bot.run(subreddits):
            youtube_comments = self.youtube_bot.run(post.url)
            reddit_comments = self.reddit_bot.get_top_n_comments(post)

            for reddit_comment in reddit_comments:
                r_comment, _ = RedditComment.get_or_create(comment_id=reddit_comment.id,
                                                           permalink='http://reddit.com' + reddit_comment.permalink,
                                                           post=RedditPost.get(
                                                               RedditPost.post_id == reddit_comment.submission.id))

                for youtube_comment in youtube_comments:
                    yt_body = youtube_comment['textDisplay']
                    similarity = self.similarity(yt_body, reddit_comment.body)

                    if similarity > self.SIMILARITY_LIMIT:
                        similar_posts.append((similarity, reddit_comment, youtube_comment))

                        video = YoutubeVideo.get(YoutubeVideo.video_id == youtube_comment['videoId'])
                        comment_id = youtube_comment['id']

                        y_comment = YoutubeComment.create(comment_id=comment_id,
                                                          video=video,
                                                          permalink=yt.YoutubeVideoBot.build_url(video.video_id,
                                                                                                 comment_id))

                        CrossCommentRelationship.create(reddit_comment=r_comment,
                                                        youtube_comment=y_comment,
                                                        similarity=similarity)
                        youlog.log.info(u'Post:%s, Comment:%s - Reddit(%s)<-%f->Youtube(%s).' % (
                            post.id, reddit_comment.id, reddit_comment.body, similarity, yt_body))
                        break

        self.make_replies()
        youlog.log.info('Reached end of reddit post stream...exiting.')

        return similar_posts

    def make_replies(self):
        """ The bot will attempt to make replies to the given similar youtube/reddit comments on reddit.

        """
        youlog.log.info('Bot is making replies if live.  Live status: %s' % self.LIVE)

        try_again = True

        for cross_comment in CrossCommentRelationship.select().where(CrossCommentRelationship.replied == False):
            reddit_db_entry = cross_comment.reddit_comment
            youtube_db_entry = cross_comment.youtube_comment
            youlog.log.info('Replying to comment %s because of youtube comment %s' % (reddit_db_entry.permalink,
                                                                                      youtube_db_entry.permalink))

            retries = 0

            if not self.LIVE:
                break

            while try_again:
                try_again = False

                try:
                    reply_body = self.reply_template % (100 * round(cross_comment.similarity, 4),
                                                        youtube_db_entry.permalink)
                    self.reddit_bot.comment(reddit_db_entry.comment_id).reply(reply_body)
                    break

                except praw.exceptions.APIException:
                    youlog.log.warning('Bot reply failed...retrying %d times...' % self.REDDIT_NUM_RETRIES)
                    retries += 1
                    time.sleep(self.REDDIT_REPLY_INTERVAL)
                    try_again = True if retries < self.REDDIT_NUM_RETRIES else False

    @staticmethod
    def similarity(str1, str2):
        return SequenceMatcher(None, str1, str2).ratio()
