from difflib import SequenceMatcher

import youcomment.youlog as youlog
import youcomment.reddit as rd
import youcomment.youtube as yt
import youcomment.conf as conf
from youcomment.errors import InvalidYoutubeURL
from youcomment.youtube import VIDEO_ID, TEXT, ID
from youcomment.database import (CrossCommentRelationship,
                                 YoutubeComment,
                                 RedditPost,
                                 RedditComment,
                                 YoutubeVideo,
                                 init_db)


class YouCompareBot(object):
    with open(conf.TEMPLATE_PATH, 'r') as f:
        REPLY_TEMPLATE = f.read()
    MODE = conf.LIVE_MODE if conf.YC_LIVE_MODE else conf.DEV_MODE
    SIMILARITY_LIMIT = conf.SIMILARITY_LIMIT

    def __init__(self, subreddits=None):
        init_db()
        self.reddit_bot = rd.RedditBot()
        self.youtube_bot = yt.YoutubeBot()
        self.reddit_bot.subreddit_list = subreddits or self.reddit_bot.subreddit_list

    def run(self, subreddits=None):
        """ Runs the bot and makes replies if conf.LIVE is True.
            If conf.REDDIT_NUM_REPLIES set to:
                0 - Runs indefinitely
                int - Runs until the number of posts is checked.

        :param subreddits: list or str, list of subreddit names or just a name
        :return: list(tuple(float, praw.models.reddit.comment.Comment, dict)), list of (similarity, youtube video data, reddit comment)
        """
        youlog.log.info('Initializing get_top_comments_from_url of %s.' % self)
        similar_posts = []

        for post in self.reddit_bot.get_posts(subreddits or self.reddit_bot.subreddit_list):
            try:
                youtube_comments = self.youtube_bot.get_top_comments_from_url(post.url)
                reddit_comments = self.reddit_bot.get_top_comments(post)

                for reddit_comment in reddit_comments:
                    for youtube_comment in youtube_comments:
                        similarity = self.similarity(youtube_comment[TEXT], reddit_comment.body)
                        if similarity > self.SIMILARITY_LIMIT:
                            self.make_relationship(youtube_comment, reddit_comment, similarity)
                            break
            except InvalidYoutubeURL:
                youlog.log.warning('Post %s was not detected to have a YouTube Link...skipping' % post.id)

        self.make_replies()
        youlog.log.info('Reached end of reddit post stream...exiting.')
        return similar_posts

    def make_relationship(self, youtube_comment, reddit_comment, similarity):
        reddit_post = RedditPost.get(RedditPost.post_id == reddit_comment.submission.id)
        r_db_comment, _ = RedditComment.get_or_create(comment_id=reddit_comment.id,
                                                      permalink=rd.RedditBot.build_comment_url(reddit_comment),
                                                      post_id=reddit_post)

        y_video = YoutubeVideo.get(YoutubeVideo.video_id == youtube_comment[VIDEO_ID])
        y_comment_id = youtube_comment[ID]
        y_db_comment, _ = YoutubeComment.get_or_create(comment_id=y_comment_id,
                                                       video_id=y_video,
                                                       permalink=yt.YoutubeBot.build_comment_url(y_video.video_id,
                                                                                                 y_comment_id))

        cc_relationship, _ = CrossCommentRelationship.get_or_create(reddit_comment_id=r_db_comment,
                                                                    youtube_comment_id=y_db_comment,
                                                                    similarity=similarity)

        has_replied = any([reply for reply in reddit_comment.replies if reply.author.name == self.reddit_bot.user.me()])
        cc_relationship.replied = has_replied
        cc_relationship.save()

        youlog.log.info(u'Post:{}, {}'.format(reddit_post.id, repr(cc_relationship)))

    def make_replies(self):
        youlog.log.info('Bot status: %s, %s making replies.' % (self.MODE, 'not' if self.MODE == conf.DEV_MODE else ''))

        for cross_comment in CrossCommentRelationship.select().where(CrossCommentRelationship.replied == False):
            reddit_db_entry = cross_comment.reddit_comment_id
            youtube_db_entry = cross_comment.youtube_comment_id
            youlog.log.info('Using cross comment relationship: %r' % cross_comment)

            if self.MODE == conf.LIVE_MODE:
                reply_body = self.REPLY_TEMPLATE.format(SIM=round(100 * cross_comment.similarity, 3),
                                                        URL=youtube_db_entry.permalink,
                                                        V=conf.VERSION)
                self.reddit_bot.comment_reply(reddit_db_entry.comment_id, reply_body)
                cross_comment.replied = True
                cross_comment.save()
                youlog.log.info('Successfully made reply.')

    @staticmethod
    def similarity(str1, str2):
        return SequenceMatcher(None, str1, str2).ratio()
