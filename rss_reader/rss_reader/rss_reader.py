# https://stackoverflow.com/questions/55936200/how-to-build-a-simple-rss-reader-in-python-3-7
# https://www.jcchouinard.com/read-rss-feed-with-python/

# how to add option without any argument (--json)
# https://intellipaat.com/community/4618/argparse-module-how-to-add-option-without-any-argument

# logging:
# https://khashtamov.com/ru/python-logging/

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attrs

# format pubDate of rss feed:
# https://stackoverflow.com/questions/12270531/how-to-format-pubdate-with-python
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior


# parse RSS

# python -m pip install bs4  !!!
# python -m pip install requests  !!!
# python - m pip install lxml    !!!  чтобы нормально парсился xml
# python install pickledb

# python -m pip install --upgrade pip setuptools wheel

from bs4 import BeautifulSoup
import requests
import argparse

import json # json

import logging
import sys
from logging import StreamHandler, Formatter
from version import __version__
import pickledb
import datetime
import time
import feedparser
import os

logger = logging.getLogger(__name__)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))


def init_db():
    if not os.path.exists('rss.db'):
        with open('rss.db', 'w') as f:
            f.write('{}')

    rss_db = pickledb.load('rss.db', False)
    return rss_db


db = init_db()


def parse_rss_reader_args():
    """Creates the arguments parser, adds arguments."""

    parser = argparse.ArgumentParser(prog='rss_reader', description='This utility reads RSS feed & outputs to console')
    parser.add_argument('source', nargs='?', type=str, help='RSS URL')
    parser.add_argument('--version', action='store_true', help='print version info')
    parser.add_argument('--json', action='store_true', help='print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='output verbose status messages in stdout')
    parser.add_argument('--limit', type=int, help='limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, help='print out the news from the specified day')
    args = parser.parse_args()

    return args


def read_rss(rss_url):
    """
    Fetches the given url using requests;
    Parses the XML with BeautifulSoup;
    Creates a list of dictionaries with article data: title, image, link, date;
    Fetches feed title

    :param rss_url: RSS url for reading
    :return: feed_title - title of the rss feed, articles_dicts - list of dictionaries with article data
    """
    try:
        logger.debug("Starting rss reader...")
        url = requests.get(rss_url)
        logger.debug(f"Loading news from {rss_url}...")

        soup = BeautifulSoup(url.content, 'xml')
    except Exception as e:
        raise Exception('Error fetching the URL: ', rss_url)

    try:
        articles = soup.findAll('item')

        articles_dicts = [
            {
                'title': a.find('title').text,  # 'title': a.title.text, # alternative syntax
                'link': a.find('link').text,
                'image': a.find('media:content'),
                'date': a.find('pubDate').text
            }
            for a in articles
        ]
        feed_title = soup.find('channel').title.text
        return feed_title, articles_dicts
    except Exception as e:
        raise Exception('Could not parse the xml: %s' % rss_url)  # %s - placeholder для строки для еррора


def get_articles(articles_limit=float('inf')):

    #TODO errors: not integer.
    """
    Gets results of rss parsing

    :param articles_limit: if not specified, then user gets _all_ available feed;
    if larger than feed size then user gets _all_ available news.
    :return: articles_list - list of dictionaries with articles
    """

    args = parse_rss_reader_args()
    feed, articles = read_rss(args.source)
    logger.debug("Processing result...\n")
    if articles_limit >= 1:
        print(f'\nFeed: {feed}\n')
        articles_list = []
        for article in articles:
            if articles.index(article) < articles_limit:
                articles_dict = {
                    'Title': article["title"],
                    'Date': time.strftime('%a, %d %b %Y %X %z', feedparser.datetimes._parse_date(article["date"])),
                    'Image': article["image"]["url"],
                    'Link': article["link"]
                }
                articles_list.append(articles_dict)

                date_in_db = time.strftime('%Y%m%d', feedparser.datetimes._parse_date(article["date"]))
                if not db.exists(date_in_db):
                    add_to_db(db, date_in_db, articles_dict)
                else:
                    update_db(db, date_in_db, articles_dict)
            else:
                break
    else:
        raise Exception("Sorry, no numbers below one")

    return articles_list


def print_articles(articles_list):
    """
    Prints requested articles in console
    :param articles_list: list of dictionaries with articles to be printed
    """
    for article in articles_list:
        print(
            f'Title: {article["Title"]}\n'
            f'Date: {article["Date"]}\n'
            f'Image: {article["Image"]}\n'
            f'Link: {article["Link"]}\n------------------------\n'
            )


def add_to_db(database, date, article):
    """
    Adds article for the specific date to the local database

    :param database: local database where the articles for the specific dates are being stored
    :param date: a date in `%Y%m%d` format - actual publishing date
    :param article: dictionary with article data to be added
    """
    database.set(date, [article])
    database.dump()


def update_db(database, date, article):
    """
    Updates the list with articles for the specific date in the local database

    :param database: local database where the articles for the specific dates are being stored
    :param date: a date in `%Y%m%d` format - actual publishing date
    :param article: dictionary with article data
    """
    new_value = database.get(date)
    if article not in new_value:
        new_value.append(article)
    database.set(date, new_value)
    database.dump()


def print_from_db(database, date, articles_limit=float('inf')):
    """
    In case of using `--date` argument prints the news from the database for the specific date in console

    :param database: local database where the articles for the specific dates are being stored
    :param date: a date in `%Y%m%d` format - actual publishing date
    :param articles_limit: if not specified, then user gets _all_ available articles from database for the specific date;
    if larger than number of articles in database, then user gets _all_ available articles.
    :return specific_date_articles: the list of dictionaries with articles for the specific date
    """
    try:
        logger.debug(f"Printing the news from {date}...\n")
        specific_date_articles = database.get(date)
        limited_articles_list = []
        if articles_limit >= 1:
            for article in specific_date_articles:
                if specific_date_articles.index(article) < articles_limit:
                    limited_articles_list.append(article)
                else:
                    break
        else:
            logger.error("Sorry, no numbers below one")
        return limited_articles_list

    except Exception as e:
        raise Exception('Could not find the news for the requested date in the database.')


def print_json(articles_list):
    """
    In case of using `--json` argument the utility converts the news into JSON format and prints in stdout
    :param articles_list: list of dictionaries with articles to be converted into JSON format and printed in stdout
    """
    logger.debug("Printing news in JSON format...\n")
    articles_json = json.dumps(articles_list, indent=2)
    print(articles_json)


def print_version():
    """
    Prints version
    """
    print(__version__)


def main():

    args = parse_rss_reader_args()
    #try:
    if args.source:
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        if args.limit:
            articles = get_articles(args.limit)
        else:
            articles = get_articles()
        print_articles(articles)

        if args.json:
            print_json(articles)

    else:
        if args.date:
            if args.limit:
                specific_date_articles = print_from_db(db, args.date, args.limit)
            else:
                specific_date_articles = print_from_db(db, args.date)
            print_articles(specific_date_articles)

            if args.json:
                print_json(specific_date_articles)

        elif args.version:
            print_version()
        else:
            raise Exception("Enter some URL.")
    # except Exception as e:
    #     logger.error(e)
    #
    logger.debug("Exiting the program.")


if __name__ == "__main__":
    main()


# TODO ERROR] 'NoneType' object is not subscriptable- -  python rss_reader.py 'https://news.yahoo.com/rss/' --limit 35 --json --verbose
# 'image': None,
# <item>
# <title>Russia `alarmed' at no US visas to attend UN leaders meeting</title>
# <link>https://news.yahoo.com/russia-alarmed-no-us-visas-033903929.html</link>
# <pubDate>2022-09-03T03:39:03Z</pubDate>
# <source url="http://www.ap.org/">Associated Press</source>
# <guid isPermaLink="false">russia-alarmed-no-us-visas-033903929.html</guid>
# <media:credit role="publishing company"/>
# </item>

# test_url = 'https://news.yahoo.com/rss/'
# test_url = 'https://realpython.com/atom.xml' # Error     feed = soup.find('channel').title.text
# AttributeError: 'NoneType' object has no attribute 'title'

# test_url = 'https://practicaldatascience.co.uk/feed.xml'
# test_url = 'https://waylonwalker.com/rss.xml'
# test_url = 'https://www.jcchouinard.com/author/jean-christophe-chouinard/feed/'