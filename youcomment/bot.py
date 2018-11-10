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

    def run(self, subreddit=None, reply=False):
        subreddit = subreddit if isinstance(subreddit, list) else subreddit
        posts = self.reddit_bot.run(subreddit)
        similar_posts = []
        for post in posts:
            youtube_comments = self.youtube_bot.run(post.url)
            reddit_comments = self.reddit_bot.get_top_25_comments(post)
            
            for youtube_comment in youtube_comments:
                for reddit_comment in reddit_comments:
                    similarity = self.similarity(youtube_comment['textDisplay'], reddit_comment.body)
                    if similarity > conf.SIMILARITY_LIMIT:
                        similar_posts.append((similarity, reddit_comment, youtube_comment))
    
        if reply:
            self.make_replies(similar_posts)
    
        return similar_posts
        
    def make_replies(self, similar_posts):
        try_again = True
        for similar_post in similar_posts:
            value, reddit, youtube = similar_post
            while try_again:
                try_again = False
                try:
                    reddit.reply(self.reply_template % (100 * round(value, 4), youtube['url']))
                    break
                except praw.exceptions.APIException:
                    time.sleep(600)
                    try_again = True
                


    @staticmethod
    def similarity(str1, str2):
        return SequenceMatcher(None, str1, str2).ratio()
