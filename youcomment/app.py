import os
from flask import Flask, render_template, g
import atexit

from youcomment.database import db_proxy
import youcomment.youlog as youlog
from youcomment.database import RedditPost, CrossCommentRelationship, Subreddit
from youcomment.__main__ import create_scheduler

app = Flask(__name__)

youlog.log.info('Running YouComment as Web Server.')
scheduler = create_scheduler()
atexit.register(lambda: scheduler.shutdown(wait=False))


@app.route('/')
def show_entries():
    return render_template('status.html',
                           state=scheduler.running,
                           blacklists=Subreddit.select().where(Subreddit.blacklisted == True),
                           posts=RedditPost.select(),
                           replies=CrossCommentRelationship.select())


@app.before_request
def before_request():
    g.db = db_proxy
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)
