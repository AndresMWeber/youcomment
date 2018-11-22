import argparse
from youcomment.bot import YouCompareBot

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add some integers.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--maxcomments', type=int,
                       help='Indicate the maximum number of comments the bot will scrape on a discrete run.')
    group.add_argument('-c', '--continuous', action='store_const', const=-1,
                        help='Run bot continuously.')

    parser.add_argument('-s', '--subreddits', type=str, nargs="+",
                        help='A space-separated list of subreddits to run the bot on.')

    parser.add_argument('-i', '--similarity', type=float,
                        help='Specify if you want to override the default similarity limit (default: 0.75)')

    namespace = parser.parse_args()


    bot_instance = YouCompareBot(subreddits=namespace.subreddits)

    if namespace.maxcomments or namespace.continuous:
        bot_instance.reddit_bot.REDDIT_MAX_POSTS = namespace.maxcomments

    if namespace.similarity:
        bot_instance.SIMILARITY_LIMIT = namespace.similarity

    bot_instance.run()