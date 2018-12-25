import peewee
import os
import youcomment.conf as conf


def load_db():
    db_proxy = peewee.Proxy()
    if 'HEROKU' in os.environ:
        from six.moves.urllib.parse import urlparse, uses_netloc
        uses_netloc.append('postgres')
        url = urlparse(os.environ["DATABASE_URL"])
        db_kwargs = {'database': url.path[1:], 'user': url.username, 'password': url.password,
                     'host': url.hostname, 'port': url.port}
        db = peewee.PostgresqlDatabase(**db_kwargs)
    else:
        default_pragmas = {'journal_mode': 'wal', 'foreign_keys': 1, 'ignore_check_constraints': 0}
        db = peewee.SqliteDatabase(conf.DB_PATH, pragmas=default_pragmas)

    db_proxy.initialize(db)
    return db, db_proxy


db, db_proxy = load_db()


class Subreddit(peewee.Model):
    name = peewee.CharField(max_length=255, unique=True)
    blacklisted = peewee.BooleanField(default=False)

    class Meta:
        database = db

    @classmethod
    def get_bans(self):
        return Subreddit.select().where(Subreddit.blacklisted)


class RedditPost(peewee.Model):
    post_id = peewee.CharField(max_length=100, unique=True)
    subreddit_id = peewee.ForeignKeyField(Subreddit, backref='posts')
    permalink = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = db


class RedditComment(peewee.Model):
    comment_id = peewee.CharField(max_length=100, unique=True)
    post_id = peewee.ForeignKeyField(RedditPost, backref='comments')
    permalink = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = db


class YoutubeVideo(peewee.Model):
    video_id = peewee.CharField(max_length=255, unique=True)
    video_url = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = db


class YoutubeComment(peewee.Model):
    comment_id = peewee.CharField(max_length=255, unique=True)
    video_id = peewee.ForeignKeyField(YoutubeVideo, backref='video')
    permalink = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = db


class CrossCommentRelationship(peewee.Model):
    reddit_comment_id = peewee.ForeignKeyField(RedditComment, backref='related_to')
    youtube_comment_id = peewee.ForeignKeyField(YoutubeComment, backref='related_to')
    similarity = peewee.FloatField(default=0.0)
    replied = peewee.BooleanField(default=False)

    class Meta:
        database = db

    def __repr__(self):
        return str(u'{}(reddit: {}, youtube: {}, similarity: {}, replied: {}'.format(self.__class__.__name__,
                                                                                     self.reddit_comment_id.permalink,
                                                                                     self.youtube_comment_id.permalink,
                                                                                     self.similarity,
                                                                                     self.replied).encode('utf-8'))


models = [Subreddit, RedditPost, RedditComment, YoutubeVideo, YoutubeComment, CrossCommentRelationship]


def wipe_db():
    db.drop_tables(models)
    init_db()


def init_db():
    with db:
        db.create_tables(models)
