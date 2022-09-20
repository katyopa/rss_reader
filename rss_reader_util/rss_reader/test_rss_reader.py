from unittest import TestCase
from rss_reader import rss_reader
import pickledb
import json
from unittest.mock import MagicMock
import rss_reader
import os
import PyPDF2
import unittest.mock
from unittest.mock import patch


TestCase.maxDiff = None   # чтобы difference целиком показывался


class TestGetArticles(TestCase):

    def test_get_articles_no_image(self):
        rss_reader.rss_reader.parse_rss_reader_args = MagicMock()
        rss_reader.rss_reader.create_json.return_value = True

        rss_reader.rss_reader.read_rss = MagicMock()
        rss_reader.rss_reader.read_rss.return_value = (
            'Yahoo News - Latest News & Headlines',
            [
               {
                   'title': 'title_1',
                   'link': 'link_1',
                   'date': 'date_1'
               },
               {
                   'title': 'title_2',
                   'link': 'link_2',
                   'date': 'date_2'
               },
               {
                   'title': 'title_3',
                   'link': 'link_3',
                   'date': 'date_3'
               }
            ]
                                           )

        rss_reader.add_to_db = MagicMock()
        rss_reader.add_to_db.return_value = True

        rss_reader.rss_reader.time.strftime = MagicMock()
        rss_reader.rss_reader.time.strftime.return_value = 'Tue, 06 Sep 2022 17:24:17 +0100'

        rss_reader.rss_reader.feedparser.datetimes._parse_date = MagicMock()
        rss_reader.rss_reader.feedparser.datetimes._parse_date.return_value = True

        articles_list = rss_reader.rss_reader.get_articles(articles_limit=2)
        result_list = [
               {
                   'Title': 'title_1',
                   'Date': 'Tue, 06 Sep 2022 17:24:17 +0100',
                   'Link': 'link_1'
               },
               {
                   'Title': 'title_2',
                   'Date': 'Tue, 06 Sep 2022 17:24:17 +0100',
                   'Link': 'link_2'
               }
                        ]

        self.assertEqual(articles_list, result_list)

    def test_get_articles_limit_less_than_1(self):
        rss_reader.rss_reader.parse_rss_reader_args = MagicMock()
        rss_reader.rss_reader.create_json.return_value = True

        rss_reader.rss_reader.read_rss = MagicMock()
        rss_reader.rss_reader.read_rss.return_value = (
            'Yahoo News - Latest News & Headlines',
            [
               {
                   'title': 'title_1',
                   'link': 'link_1',
                   'date': 'date_1'
               },
               {
                   'title': 'title_2',
                   'link': 'link_2',
                   'date': 'date_2'
               },
               {
                   'title': 'title_3',
                   'link': 'link_3',
                   'date': 'date_3'
               }
            ]
                                           )

        rss_reader.add_to_db = MagicMock()
        rss_reader.add_to_db.return_value = True

        rss_reader.rss_reader.time.strftime = MagicMock()
        rss_reader.rss_reader.time.strftime.return_value = 'Tue, 06 Sep 2022 17:24:17 +0100'

        rss_reader.rss_reader.feedparser.datetimes._parse_date = MagicMock()
        rss_reader.rss_reader.feedparser.datetimes._parse_date.return_value = True

        with self.assertRaises(Exception) as context:
            rss_reader.rss_reader.get_articles(articles_limit=0)

        self.assertTrue("Sorry, no numbers below one" in str(context.exception))

    def test_get_articles_add_to_db(self):
        rss_reader.rss_reader.parse_rss_reader_args = MagicMock()
        rss_reader.rss_reader.create_json.return_value = True

        rss_reader.rss_reader.read_rss = MagicMock()
        rss_reader.rss_reader.read_rss.return_value = (
            'Yahoo News - Latest News & Headlines',
            [
               {
                   'title': 'title_1',
                   'link': 'link_1',
                   'date': 'date_1'
               },
               {
                   'title': 'title_2',
                   'link': 'link_2',
                   'date': 'date_2'
               },
               {
                   'title': 'title_3',
                   'link': 'link_3',
                   'date': 'date_3'
               }
            ]
                                           )

        rss_reader.add_to_db = MagicMock()
        rss_reader.add_to_db.return_value = True

        rss_reader.rss_reader.time.strftime = MagicMock()
        rss_reader.rss_reader.time.strftime.return_value = 'Tue, 06 Sep 2022 17:24:17 +0100'

        rss_reader.rss_reader.feedparser.datetimes._parse_date = MagicMock()
        rss_reader.rss_reader.feedparser.datetimes._parse_date.return_value = True

        with open('rss_reader/test_rss.db', 'w') as f:
            f.write('{}')

        articles_list = rss_reader.rss_reader.get_articles(articles_limit=2)
        result_list = [
               {
                   'Title': 'title_1',
                   'Date': 'Tue, 06 Sep 2022 17:24:17 +0100',
                   'Link': 'link_1'
               },
               {
                   'Title': 'title_2',
                   'Date': 'Tue, 06 Sep 2022 17:24:17 +0100',
                   'Link': 'link_2'
               }
                        ]

        self.assertEqual(articles_list, result_list)


class TestAddOrUpdateDB(TestCase):

    @patch('rss_reader.rss_reader.update_db')
    @patch('rss_reader.rss_reader.db.exists')
    def test_add_or_update_db_calls_update_db(self, mock_db_exists, mock_update_db):
        mock_db_exists.return_value = True

        rss_reader.rss_reader.add_or_update_db(
            date_in_db="20220906",
            art_to_db=[
                   {
                       "Title": "MyTitle3",
                       "Date": "MyDate3"
                   },
                   {
                       "Title": "MyTitle4",
                       "Date": "MyDate4"
                   }
               ]
               )

        mock_update_db.assert_called_once()

    @patch('rss_reader.rss_reader.add_to_db')
    @patch('rss_reader.rss_reader.db.exists')
    def test_add_or_update_calls_add_to_db(self, mock_db_exists, mock_add_to_db):
        mock_db_exists.return_value = False

        rss_reader.rss_reader.add_or_update_db(
            date_in_db="20220915",
            art_to_db=[
                {
                    "Title": "MyTitle3",
                    "Date": "MyDate3"
                }
            ]
        )

        mock_add_to_db.assert_called_once()


class TestPrintArticles(TestCase):

    def test_print_articles_no_image(self):
        articles = [{'Title': 'Woman whose rape DNA led to her arrest sues San Francisco',
                     'Date': 'Mon, 12 Sep 2022 20:58:22 +0100',
                     'Link': 'https://news.yahoo.com/woman-whose-rape-dna-led-205822755.html'}]

        with patch('builtins.print') as mock_print:
            rss_reader.rss_reader.print_articles(articles_list=articles)

            self.assertEqual(mock_print.call_count, 1)

    def test_print_articles_with_image(self):
        articles = [
            {
                "Title": "All 14 on boat in deadly crash off the Florida Keys were ejected, official report says",
                "Date": "Tue, 06 Sep 2022 20:11:58 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/KMNXXqA.7EuEBAyRi1gQxw--~"
                         "B/aD0xMTU5O3c9MTE0MDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/miami_herald_mcclatchy_975/4a6d0aae87cc4c24ada13279c70095e3",
                "Link": "https://news.yahoo.com/14-boat-deadly-crash-off-201158562.html"
            }
        ]

        with patch('builtins.print') as mock_print:
            rss_reader.rss_reader.print_articles(articles_list=articles)

            self.assertEqual(mock_print.call_count, 2)


class TestAddToDB(TestCase):

    def test_add_to_db(self):
        with open('rss_reader/test_rss.db', 'w') as f:
            f.write('{}')

        db_articles = [
            {
                "Title": "World's second-tallest roller coaster is permanently closing",
                "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~"
                         "B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
                "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"
            },
            {
                "Title": "All 14 on boat in deadly crash off the Florida Keys were ejected, official report says",
                "Date": "Tue, 06 Sep 2022 20:11:58 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/KMNXXqA.7EuEBAyRi1gQxw--~"
                         "B/aD0xMTU5O3c9MTE0MDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/miami_herald_mcclatchy_975/4a6d0aae87cc4c24ada13279c70095e3",
                "Link": "https://news.yahoo.com/14-boat-deadly-crash-off-201158562.html"
            },
            {
                "Title": "Botched cosmetic tattoo done on a budget leaves Thai woman with four eyebrows",
                "Date": "Tue, 06 Sep 2022 22:35:51 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/fjBt9UDDLwSxrjvLUYFerg--~"
                         "B/aD00MjU7dz04MDA7YXBwaWQ9eXRhY2h5b24-"
                         "/https://media.zenfs.com/en/nextshark_articles_509/921bf5c2a0d957892e668bcf666f7b86",
                "Link": "https://news.yahoo.com/botched-cosmetic-tattoo-done-budget-223551634.html"
            }
        ]
        test_db = pickledb.load("rss_reader/test_rss.db",
                                False)

        test_db.set("20220906", db_articles)
        test_db.dump()

        test_article = {
            'Title': 'Southern California mudslides damage homes, carry away cars',
            'Date': 'Tue, 13 Sep 2022 13:56:25 +0100',
            'Link': 'https://news.yahoo.com/rains-mudslides-prompt-southern-california-135625021.html',
            'Image': 'https://s.yimg.com/uu/api/res/1.2/o1YsUTaaZxuqKLK86t0wew--~'
                     'B/aD0yODk1O3c9NDM0MjthcHBpZD15dGFjaHlvbg--'
                     '/https://media.zenfs.com/en/ap.org/085ec5e156bb9c378928d743edae91a0'
        }

        rss_reader.rss_reader.add_to_db(
            database=test_db,

            date="20220906",
            article=test_article
        )

        test_list = test_db.get("20220906")
        self.assertIn(test_article, test_list)

        test_db.deldb()
        test_db.dump()


class TestUpdateDB(TestCase):

    def test_update_db_does_not_exist_add(self):
        with open('rss_reader/test_rss.db', 'w') as f:
            f.write('{}')

        db_articles = [
            {
                "Title": "World's second-tallest roller coaster is permanently closing",
                "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~"
                         "B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
                "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"
            },
            {
                "Title": "All 14 on boat in deadly crash off the Florida Keys were ejected, official report says",
                "Date": "Tue, 06 Sep 2022 20:11:58 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/KMNXXqA.7EuEBAyRi1gQxw--~"
                         "B/aD0xMTU5O3c9MTE0MDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/miami_herald_mcclatchy_975/4a6d0aae87cc4c24ada13279c70095e3",
                "Link": "https://news.yahoo.com/14-boat-deadly-crash-off-201158562.html"
            },
            {
                "Title": "Botched cosmetic tattoo done on a budget leaves Thai woman with four eyebrows",
                "Date": "Tue, 06 Sep 2022 22:35:51 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/fjBt9UDDLwSxrjvLUYFerg--~"
                         "B/aD00MjU7dz04MDA7YXBwaWQ9eXRhY2h5b24-"
                         "/https://media.zenfs.com/en/nextshark_articles_509/921bf5c2a0d957892e668bcf666f7b86",
                "Link": "https://news.yahoo.com/botched-cosmetic-tattoo-done-budget-223551634.html"
            }
        ]
        test_db = pickledb.load("rss_reader/test_rss.db",
                                False)  # тесты запускаются из корневого (там где setup) - добавила путь

        test_db.set("20220906", db_articles)
        test_db.dump()

        test_article = {
            'Title': 'Southern California mudslides damage homes, carry away cars',
            'Date': 'Tue, 13 Sep 2022 13:56:25 +0100',
            'Link': 'https://news.yahoo.com/rains-mudslides-prompt-southern-california-135625021.html',
            'Image': 'https://s.yimg.com/uu/api/res/1.2/o1YsUTaaZxuqKLK86t0wew--~'
                     'B/aD0yODk1O3c9NDM0MjthcHBpZD15dGFjaHlvbg--'
                     '/https://media.zenfs.com/en/ap.org/085ec5e156bb9c378928d743edae91a0'
        }

        rss_reader.rss_reader.update_db(        # вот опять вопросы с импортом (первый rss_reader раньше не нужен был)
            database=test_db,
            date="20220906",
            article=test_article
        )
        test_list = test_db.get("20220906")
        self.assertIn(test_article, test_list)

        test_db.deldb()   # удаляю, чтобы повторно запускать
        test_db.dump()

    def test_update_db_exists_not_deleted(self):
        with open('rss_reader/test_rss.db', 'w') as f:
            f.write('{}')

        db_articles = [
            {
                "Title": "World's second-tallest roller coaster is permanently closing",
                "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~"
                         "B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--"
                      "/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
                "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"},
            {
                "Title": "All 14 on boat in deadly crash off the Florida Keys were ejected, official report says",
                "Date": "Tue, 06 Sep 2022 20:11:58 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/KMNXXqA.7EuEBAyRi1gQxw--~"
                         "B/aD0xMTU5O3c9MTE0MDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/miami_herald_mcclatchy_975/4a6d0aae87cc4c24ada13279c70095e3",
                "Link": "https://news.yahoo.com/14-boat-deadly-crash-off-201158562.html"
            },
            {
                "Title": "Botched cosmetic tattoo done on a budget leaves Thai woman with four eyebrows",
                "Date": "Tue, 06 Sep 2022 22:35:51 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/fjBt9UDDLwSxrjvLUYFerg--~"
                         "B/aD00MjU7dz04MDA7YXBwaWQ9eXRhY2h5b24-"
                         "/https://media.zenfs.com/en/nextshark_articles_509/921bf5c2a0d957892e668bcf666f7b86",
                "Link": "https://news.yahoo.com/botched-cosmetic-tattoo-done-budget-223551634.html"
            }
        ]
        test_db = pickledb.load("rss_reader/test_rss.db",
                                False)

        test_db.set("20220906", db_articles)
        test_article = {
            "Title": "World's second-tallest roller coaster is permanently closing",
            "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
            "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~"
                     "B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--"
                     "/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
            "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"
        }

        rss_reader.rss_reader.update_db(
            database=test_db,
            date="20220906",
            article=test_article
        )
        test_dict = test_db.get("20220906")
        self.assertIn(test_article, test_dict)

        test_db.deldb()
        test_db.dump()


class TestPrintFromDB(TestCase):

    def test_print_from_db_less_than_max(self):
        with open('rss_reader/test_rss.db', 'w') as f:
            f.write('{}')

        db_articles = [
            {
                "Title": "World's second-tallest roller coaster is permanently closing",
                "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~"
                         "B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--"
                      "/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
                "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"},
            {
                "Title": "All 14 on boat in deadly crash off the Florida Keys were ejected, official report says",
                "Date": "Tue, 06 Sep 2022 20:11:58 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/KMNXXqA.7EuEBAyRi1gQxw--~"
                         "B/aD0xMTU5O3c9MTE0MDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/miami_herald_mcclatchy_975/4a6d0aae87cc4c24ada13279c70095e3",
                "Link": "https://news.yahoo.com/14-boat-deadly-crash-off-201158562.html"
            },
            {
                "Title": "Botched cosmetic tattoo done on a budget leaves Thai woman with four eyebrows",
                "Date": "Tue, 06 Sep 2022 22:35:51 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/fjBt9UDDLwSxrjvLUYFerg--~"
                         "B/aD00MjU7dz04MDA7YXBwaWQ9eXRhY2h5b24-"
                         "/https://media.zenfs.com/en/nextshark_articles_509/921bf5c2a0d957892e668bcf666f7b86",
                "Link": "https://news.yahoo.com/botched-cosmetic-tattoo-done-budget-223551634.html"
            }
        ]
        test_db = pickledb.load("rss_reader/test_rss.db",
                                False)  # тесты запускаются из корневого (там где setup) - добавила путь

        test_db.set("20220906", db_articles)

        test_articles_list = rss_reader.rss_reader.print_from_db(
            database=test_db,
            date="20220906",
            articles_limit=2
        )

        result_list = [
            {
                "Title": "World's second-tallest roller coaster is permanently closing",
                "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~"
                         "B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--"
                      "/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
                "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"},
            {
                "Title": "All 14 on boat in deadly crash off the Florida Keys were ejected, official report says",
                "Date": "Tue, 06 Sep 2022 20:11:58 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/KMNXXqA.7EuEBAyRi1gQxw--~"
                         "B/aD0xMTU5O3c9MTE0MDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/miami_herald_mcclatchy_975/4a6d0aae87cc4c24ada13279c70095e3",
                "Link": "https://news.yahoo.com/14-boat-deadly-crash-off-201158562.html"
            }
        ]

        self.assertEqual(test_articles_list, result_list)

        test_db.deldb()
        test_db.dump()

    def test_print_from_db_more_than_max(self):
        with open('rss_reader/test_rss.db', 'w') as f:
            f.write('{}')

        db_articles = [
            {
                "Title": "World's second-tallest roller coaster is permanently closing",
                "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~"
                         "B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
                "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"},
            {
                "Title": "All 14 on boat in deadly crash off the Florida Keys were ejected, official report says",
                "Date": "Tue, 06 Sep 2022 20:11:58 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/KMNXXqA.7EuEBAyRi1gQxw--~"
                         "B/aD0xMTU5O3c9MTE0MDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/miami_herald_mcclatchy_975/4a6d0aae87cc4c24ada13279c70095e3",
                "Link": "https://news.yahoo.com/14-boat-deadly-crash-off-201158562.html"
            },
            {
                "Title": "Botched cosmetic tattoo done on a budget leaves Thai woman with four eyebrows",
                "Date": "Tue, 06 Sep 2022 22:35:51 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/fjBt9UDDLwSxrjvLUYFerg--~"
                         "B/aD00MjU7dz04MDA7YXBwaWQ9eXRhY2h5b24-"
                         "/https://media.zenfs.com/en/nextshark_articles_509/921bf5c2a0d957892e668bcf666f7b86",
                "Link": "https://news.yahoo.com/botched-cosmetic-tattoo-done-budget-223551634.html"
            }
        ]
        test_db = pickledb.load("rss_reader/test_rss.db",
                                False)  # тесты запускаются из корневого (там где setup) - добавила путь

        test_db.set("20220906", db_articles)

        test_articles_list = rss_reader.rss_reader.print_from_db(
            database=test_db,
            date="20220906",
            articles_limit=6
        )

        result_list = [
            {
                "Title": "World's second-tallest roller coaster is permanently closing",
                "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~"
                         "B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
                "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"},
            {
                "Title": "All 14 on boat in deadly crash off the Florida Keys were ejected, official report says",
                "Date": "Tue, 06 Sep 2022 20:11:58 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/KMNXXqA.7EuEBAyRi1gQxw--~"
                         "B/aD0xMTU5O3c9MTE0MDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/miami_herald_mcclatchy_975/4a6d0aae87cc4c24ada13279c70095e3",
                "Link": "https://news.yahoo.com/14-boat-deadly-crash-off-201158562.html"
            },
            {
                "Title": "Botched cosmetic tattoo done on a budget leaves Thai woman with four eyebrows",
                "Date": "Tue, 06 Sep 2022 22:35:51 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/fjBt9UDDLwSxrjvLUYFerg--~"
                         "B/aD00MjU7dz04MDA7YXBwaWQ9eXRhY2h5b24-"
                         "/https://media.zenfs.com/en/nextshark_articles_509/921bf5c2a0d957892e668bcf666f7b86",
                "Link": "https://news.yahoo.com/botched-cosmetic-tattoo-done-budget-223551634.html"
            }
        ]

        self.assertEqual(test_articles_list, result_list)

        test_db.deldb()
        test_db.dump()

    def test_print_from_db_no_news_for_date(self):
        with open('rss_reader/test_rss.db', 'w') as f:
            f.write('{}')

        db_articles = [
            {
                "Title": "World's second-tallest roller coaster is permanently closing",
                "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~"
                         "B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
                "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"},
            {
                "Title": "All 14 on boat in deadly crash off the Florida Keys were ejected, official report says",
                "Date": "Tue, 06 Sep 2022 20:11:58 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/KMNXXqA.7EuEBAyRi1gQxw--~"
                         "B/aD0xMTU5O3c9MTE0MDthcHBpZD15dGFjaHlvbg--"
                         "/https://media.zenfs.com/en/miami_herald_mcclatchy_975/4a6d0aae87cc4c24ada13279c70095e3",
                "Link": "https://news.yahoo.com/14-boat-deadly-crash-off-201158562.html"
            },
            {
                "Title": "Botched cosmetic tattoo done on a budget leaves Thai woman with four eyebrows",
                "Date": "Tue, 06 Sep 2022 22:35:51 +0100",
                "Image": "https://s.yimg.com/uu/api/res/1.2/fjBt9UDDLwSxrjvLUYFerg--~"
                         "B/aD00MjU7dz04MDA7YXBwaWQ9eXRhY2h5b24-"
                         "/https://media.zenfs.com/en/nextshark_articles_509/921bf5c2a0d957892e668bcf666f7b86",
                "Link": "https://news.yahoo.com/botched-cosmetic-tattoo-done-budget-223551634.html"
            }
        ]
        test_db = pickledb.load("rss_reader/test_rss.db",
                                False)

        test_db.set("20220906", db_articles)

        with self.assertRaises(Exception) as context:
            rss_reader.rss_reader.print_from_db(
                database=test_db,
                date="20220912",
                articles_limit=2
            )

        self.assertTrue('Could not find the news for the requested date in the database.' in str(context.exception))

        test_db.deldb()
        test_db.dump()


class TestCreateJson(TestCase):

    def test_create_json_positive(self):
        articles_list = [
            {
                "Title": "MyTitle1",
                "Date": "MyDate1"
            },
            {
                "Title": "MyTitle2",
                "Date": "MyDate2"
            }
        ]

        result_json = [
            {
                "Title": "MyTitle1",
                "Date": "MyDate1"
            },
            {
                "Title": "MyTitle2",
                "Date": "MyDate2"
            }
        ]

        articles_json = rss_reader.create_json(articles_list)
        articles_json_str = json.loads(articles_json)

        self.assertEqual(articles_json_str, result_json)


class PrintJson(TestCase):

    def test_print_json(self):
        with patch('builtins.print') as print_mock:
            test_articles = "We are articles in json format"
            rss_reader.rss_reader.print_json(json_articles=test_articles)
            print_mock.assert_called_with(test_articles)


class TestConvertToHtml(TestCase):
    def test_convert_to_html(self):
        rss_reader.create_json = MagicMock()
        rss_reader.create_json.return_value = \
            '[{"Title": "MyTitle1", "Date": "MyDate1"}, {"Title": "MyTitle2", "Date": "MyDate2"}]'
        articles_list = [
            {"Title": "MyTitle1", "Date": "MyDate1"},
            {"Title": "MyTitle2", "Date": "MyDate2"}
        ]
        html_output = rss_reader.rss_reader.convert_to_html(articles=articles_list)

        result = \
            '<table border="1">' \
            '<thead><tr><th>Title</th><th>Date</th></tr></thead>' \
            '<tbody><tr><td>MyTitle1</td><td>MyDate1</td></tr><tr><td>MyTitle2</td><td>MyDate2</td></tr></tbody>' \
            '</table>'

        self.assertEqual(html_output, result)


class TestConvertToPdf(TestCase):

    def test_convert_to_pdf(self):

        rss_reader.rss_reader.create_file_name = MagicMock()
        rss_reader.rss_reader.create_file_name.return_value = 'my_file.pdf'

        rss_reader.convert_to_html = MagicMock()
        rss_reader.convert_to_html.return_value = \
            '<table border="1">' \
            '<thead><tr><th>Title</th><th>Date</th></tr></thead>' \
            '<tbody><tr><td>MyTitle1</td><td>MyDate1</td></tr><tr><td>MyTitle2</td><td>MyDate2</td></tr></tbody>' \
            '</table>'

        articles_list = [
            {"Title": "MyTitle1", "Date": "MyDate1"},
            {"Title": "MyTitle2", "Date": "MyDate2"}
        ]
        pdf_path = os.getcwd()

        rss_reader.rss_reader.convert_to_pdf(
            articles=articles_list,
            path=pdf_path)

        with open(os.path.join(f'{pdf_path}', 'my_file.pdf'), 'rb') as pdf_file:
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            page = read_pdf.getPage(0)
            page_content = page.extractText()
            content = page_content.encode('utf-8')

        self.assertEqual(content, b'Title\nDate\nMyTitle1\nMyDate1\nMyTitle2\nMyDate2')

        os.remove(os.path.join(f'{pdf_path}', 'my_file.pdf'))


if __name__ == "__main__":
    unittest.main()
