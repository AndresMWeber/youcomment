import argparse
import os, time
from apscheduler.schedulers.background import BackgroundScheduler

import youcomment.bot as youbot
import youcomment.youlog as youlog
import youcomment.conf as conf


def entry():
    youlog.log.info('Running YouComment as CLI.')

    parser = argparse.ArgumentParser(description='Add some integers.')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-m', '--maxposts', type=int,
                       help='Indicate the maximum number of Reddit posts the bot will check on a discrete run.')

    group.add_argument('-c', '--continuous', action='store_const', const=0,
                       help='Run bot continuously.')

    parser.add_argument('-s', '--subreddits', type=str, nargs="+",
                        help='A space-separated list of SubReddits to run the bot on.')

    parser.add_argument('-a', '--affinity', type=float,
                        help='Specify if you want to override the default similarity limit (default: 0.75)')

    parser.add_argument('-i', '--interval', type=int, default=conf.DEFAULT_BOT_RUN_INTERVAL_MINS,
                        help='Minute delay interval for the bot to run its check.')

    namespace = parser.parse_args()
    scheduler = create_scheduler(interval=namespace.interval,
                                 subreddits=namespace.subreddits,
                                 max_posts=namespace.maxcomments or namespace.continuous,
                                 affinity=namespace.affinity)

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


def create_scheduler(**kwargs):
    minutes = kwargs.get('interval', conf.DEFAULT_BOT_RUN_INTERVAL_MINS)
    # Start the daemon
    youlog.log.info('Scheduling/Starting instance of YouComment(%s) to run every %d minutes' % (kwargs or '', minutes))

    bot_instance = youbot.YouCompareBot(subreddits=kwargs.get('subreddits', None))
    bot_instance.reddit_bot.REDDIT_MAX_POSTS = kwargs.get('max_posts', 0)
    if kwargs.get('affinity'):
        bot_instance.SIMILARITY_LIMIT = kwargs.get('affinity')

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(bot_instance.run, 'interval', minutes=minutes)
    scheduler.start()
    youlog.log.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    return scheduler


if __name__ == "__main__":
    entry()
