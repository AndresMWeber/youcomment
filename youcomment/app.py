import os
from flask import Flask, render_template
import atexit

import youcomment.youlog as youlog
from youcomment.database import RedditPost, CrossCommentRelationship, Subreddit
from youcomment.__main__ import create_scheduler

app = Flask(__name__)

youlog.log.info('Running YouComment as Web Server.')
scheduler = create_scheduler()
atexit.register(lambda: scheduler.shutdown(wait=False))


@app.route('/')
def show_entries():
    return render_template('index.html',
                           blacklists=Subreddit.select().where(Subreddit.blacklisted == True),
                           posts=RedditPost.select(),
                           replies=CrossCommentRelationship.select().where(CrossCommentRelationship.replied == True))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)
