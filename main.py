# https://stackoverflow.com/questions/55936200/how-to-build-a-simple-rss-reader-in-python-3-7
# https://www.jcchouinard.com/read-rss-feed-with-python/

# how to add option without any argument (--json)
# https://intellipaat.com/community/4618/argparse-module-how-to-add-option-without-any-argument

# logging:
# https://khashtamov.com/ru/python-logging/


# parse RSS

# python -m pip install bs4  !!!
# python -m pip install requests  !!!
# python - m pip install lxml    !!!  чтобы нормально парсился xml

# python -m pip install --upgrade pip setuptools wheel

from bs4 import BeautifulSoup
import requests
import argparse

import json # json

import logging
import sys
from logging import StreamHandler, Formatter


logger = logging.getLogger(__name__)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))


# def get_source(url):
#     """Return the source code for the provided URL.
#
#     Args:
#         url (string): URL of the page to scrape.
#
#     Returns:
#         response (object): HTTP response object from requests_html.
#     """
#
#     try:
#         session = HTMLSession()
#         response = session.get(url)
#         return response
#
#     except requests.exceptions.RequestException as e:
#         print(e)

def parse_rss_reader_args():
    """Creates the arguments parser, adds arguments."""

    parser = argparse.ArgumentParser(prog='rss_reader', description='This utility reads RSS feed & outputs to console')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action='store_true', help='print version info')
    parser.add_argument('--json', action='store_true', help='print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='output verbose status messages in stdout')
    parser.add_argument('--limit', type=int, help='limit news topics if this parameter provided')
    args = parser.parse_args()

    return args


def read_rss(rss_url):

    # TODO add images
    # TODO exceptions don't work

    """
    :param rss_url: RSS url for reading
    :return: feed_title - title of the rss feed, articles_dicts - list of dictionaries with article data

    Fetches the given url using requests;
    Parses the XML with BeautifulSoup;
    Creates a list of dictionaries with article data: title, image, link, date;
    Fetches feed title
    """
    try:
        logger.debug("Starting rss reader...")
        url = requests.get(rss_url)
        logger.debug(f"Loading news from {rss_url}...")
        soup = BeautifulSoup(url.content, 'xml')
    except Exception as e:
        print('Error fetching the URL: ', rss_url)
        print(e)
    try:
        articles = soup.findAll('item')
        articles_dicts = [
            {
                'title': a.title.text,
                'link': a.link.text,
                # 'image':
                'date': a.pubDate.text
            }
            for a in articles
        ]
        feed_title = soup.find('channel').title.text
        return feed_title, articles_dicts
    except Exception as e:
        print('Could not parse the xml: ', rss_url)
        print(e)


def print_articles(articles_limit=float('inf')):

    #TODO errors: not integer.

    """
    :param articles_limit: if not specified, then user gets _all_ available feed;
    if larger than feed size then user gets _all_ available news.
    :return: articles_list - list of dictionaries with articles
    Prints results of rss parsing in console
    """
    args = parse_rss_reader_args()
    feed, articles = read_rss(args.source)
    logger.debug("Processing result...")
    if articles_limit >= 1:
        print(f'Feed: {feed}\n\n')
        articles_list = []
        for article in articles:
            if articles.index(article) < articles_limit:
                articles_dict = {
                    'Title': article["title"],
                    'Date': article["date"],
                    'Link': article["link"]
                }

                articles_list.append(articles_dict)

                print(
                    f'Title: {article["title"]}\n\n'
                    f'Date: {article["date"]}\n\n'
                    f'Link: {article["link"]}\n\n------------------------\n'
                )
            else:
                break
    else:
        raise Exception("Sorry, no numbers below one")

    return articles_list


def print_json(articles_list):
    """
    :param articles_list: list of dictionaries with articles to be converted into JSON format and printed in stdout
    :return:
    In case of using `--json` argument the utility converts the news into JSON format and prints in stdout
    """

    articles_json = json.dumps(articles_list, indent=2)
    print(articles_json)


def main():

    args = parse_rss_reader_args()

    if args.source is not None:
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        if args.json:
            if args.limit is None:
                articles = print_articles()
            else:
                articles = print_articles(args.limit)
            print_json(articles)
        else:
            if args.limit is None:
                print_articles()
            else:
                print_articles(args.limit)

        logger.debug("Exiting the program.")


if __name__ == "__main__":
    main()



# test_url = 'https://news.yahoo.com/rss/'
#test_url = 'https://realpython.com/atom.xml' # Error     feed = soup.find('channel').title.text
# AttributeError: 'NoneType' object has no attribute 'title'

# test_url = 'https://practicaldatascience.co.uk/feed.xml'
#test_url = 'https://waylonwalker.com/rss.xml'
#test_url = 'https://www.jcchouinard.com/author/jean-christophe-chouinard/feed/'