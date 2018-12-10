import os
from time import sleep
from flask import Flask, render_template, g, Response, stream_with_context
import atexit

from youcomment.database import db_proxy
import youcomment.conf as conf
import youcomment.youlog as youlog
from youcomment.database import RedditPost, CrossCommentRelationship, Subreddit
from youcomment.__main__ import create_scheduler

app = Flask(__name__)

youlog.log.info('Running YouComment as Web Server.')
scheduler = create_scheduler()
atexit.register(lambda: scheduler.shutdown(wait=False))


def generate():
    with open(conf.LOG_PATH, 'r') as f:
        while True:
            for line in f.readlines():
                yield line
            sleep(1)

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@app.route('/')
def status():
    return render_template('status.html',
                           state=scheduler.running,
                           blacklists=Subreddit.select().where(Subreddit.blacklisted == True),
                           posts=RedditPost.select(),
                           replies=CrossCommentRelationship.select())


@app.route('/log_stream')
def log_stream():
    return Response(generate(), mimetype='text/event-stream')


@app.route('/log')
def log():
    return Response(stream_template('log.html', state=scheduler.running, log=stream_with_context(generate())))


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
