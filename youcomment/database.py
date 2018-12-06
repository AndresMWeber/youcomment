import peewee
import os
import youcomment.conf as conf

db_proxy = peewee.Proxy()

if 'HEROKU' in os.environ:
    import urlparse, psycopg2

    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    db = psycopg2.PostgresqlDatabase(database=url.path[1:],
                                     user=url.username,
                                     password=url.password,
                                     host=url.hostname,
                                     port=url.port)
    db_proxy.initialize(db)
else:
    db = peewee.SqliteDatabase(conf.DB_PATH, pragmas={'journal_mode': 'wal',
                                                      'foreign_keys': 1,
                                                      'ignore_check_constraints': 0})
    db_proxy.initialize(db)


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
    subreddit = peewee.ForeignKeyField(Subreddit, backref='subreddit')
    permalink = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = db


class RedditComment(peewee.Model):
    comment_id = peewee.CharField(max_length=100, unique=True)
    post = peewee.ForeignKeyField(RedditPost, backref='post')
    replied = peewee.BooleanField(default=False)
    permalink = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = db


class YoutubeVideo(peewee.Model):
    video_id = peewee.CharField(max_length=20, unique=True)
    video_url = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = db


class YoutubeComment(peewee.Model):
    comment_id = peewee.CharField(max_length=20, unique=True)
    permalink = peewee.CharField(max_length=255, unique=True)
    video = peewee.ForeignKeyField(YoutubeVideo, backref='video')

    class Meta:
        database = db


class CrossCommentRelationship(peewee.Model):
    reddit_comment = peewee.ForeignKeyField(RedditComment, backref='reddit_comment')
    youtube_comment = peewee.ForeignKeyField(YoutubeComment, backref='youtube_comment')
    similarity = peewee.FloatField(default=0.0)
    replied = peewee.BooleanField(default=False)

    class Meta:
        database = db


models = [Subreddit, RedditPost, RedditComment, YoutubeVideo, YoutubeComment, CrossCommentRelationship]


def wipe_db():
    db.drop_tables(models)
    init_db()


def init_db():
    with db:
        db.create_tables(models)
