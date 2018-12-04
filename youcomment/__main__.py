import argparse
import os, time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import youcomment.bot as youbot
import youcomment.youlog as youlog


def entry():
    if __name__ == '__main__':

        parser = argparse.ArgumentParser(description='Add some integers.')

        group = parser.add_mutually_exclusive_group()

        group.add_argument('-m', '--maxcomments', type=int,
                           help='Indicate the maximum number of comments the bot will scrape on a discrete run.')

        group.add_argument('-c', '--continuous', action='store_const', const=-1,
                           help='Run bot continuously.')

        parser.add_argument('-s', '--subreddits', type=str, nargs="+",
                            help='A space-separated list of subreddits to run the bot on.')

        parser.add_argument('-a', '--affinity', type=float,
                            help='Specify if you want to override the default similarity limit (default: 0.75)')

        parser.add_argument('-i', '--interval', type=int, default=5,
                            help='Minute delay interval for the bot to run its check.')

        namespace = parser.parse_args()

        # Start the daemon
        youlog.log.info('Starting instance of YouComment with arguments: %s' % namespace)

        bot_instance = youbot.YouCompareBot(subreddits=namespace.subreddits)

        if namespace.maxcomments or namespace.continuous:
            bot_instance.reddit_bot.REDDIT_MAX_POSTS = namespace.maxcomments

        if namespace.affinity:
            bot_instance.SIMILARITY_LIMIT = namespace.affinity

        scheduler = BackgroundScheduler()
        scheduler.add_job(bot_instance.run,
                          'date',
                          run_date=datetime.now() + timedelta(minutes=namespace.interval))

        scheduler.start()
        youlog.log.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            scheduler.shutdown()


if __name__ == "__main__":
    entry()
