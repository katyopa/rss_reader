from unittest import TestCase
from rss_reader import rss_reader
import pickledb
from json import loads

# class TestPrintArticles(TestCase):
#
#     def test_print_articles(self):
#         articles_list = [{'Title': 'Woman whose rape DNA led to her arrest sues San Francisco',
#           'Date': 'Mon, 12 Sep 2022 20:58:22 +0100',
#           'Link': 'https://news.yahoo.com/woman-whose-rape-dna-led-205822755.html'},
#          {'Title': "Donald Trump potentially snubbed for the Queen's funeral after the Bidens receive two invites",
#           'Date': 'Mon, 12 Sep 2022 10:08:45 +0100',
#           'Link': 'https://news.yahoo.com/donald - trump - potentially - snubbed - queens - 100845927.html'},
#          {'Title': 'Video shows Russian fighter jet crashing immediately after sharp turn in take - off, Ukraine says',
#           'Date': 'Tue, 13 Sep 2022 12: 38:02 + 0100',
#           'Link': 'https: // news.yahoo.com / video - shows - russian - fighter - jet - 123802054.html'}]
#
#         self.assertEqual(
#             rss_reader.print_articles(articles_list),
#     """"
#     Link': 'https://news.yahoo.com/video-shows-russian-fighter-jet-123802054.html'}]
#     Title: Woman's rape cries go unheard in unmonitored drug sting
#     Date: Tue, 13 Sep 2022 14:27:08 +0100
#     Link: https://news.yahoo.com/womans-rape-cries-unheard-unmonitored-142708098.html
#     ------------------------
#
#     Title: Donald Trump potentially snubbed for the Queen's funeral after the Bidens receive two invites
#     Date: Mon, 12 Sep 2022 10:08:45 +0100
#     Link: https://news.yahoo.com/donald-trump-potentially-snubbed-queens-100845927.html
#     ------------------------
#
#     Title: Video shows Russian fighter jet crashing immediately after sharp turn in take-off, Ukraine says
#     Date: Tue, 13 Sep 2022 12:38:02 +0100
#     Link: https://news.yahoo.com/video-shows-russian-fighter-jet-123802054.html
#     ------------------------
#     """
#                             )
#

class TestUpdateDB(TestCase):

    def test_update_db_positive(self):
        test_db = pickledb.load("rss_reader/test_rss.db", False)  # тесты запускаются из корневого (там где setup) - добавила путь
        test_article = {
            'Title': 'Southern California mudslides damage homes, carry away cars',
            'Date': 'Tue, 13 Sep 2022 13:56:25 +0100',
            'Link': 'https://news.yahoo.com/rains-mudslides-prompt-southern-california-135625021.html',
            'Image': 'https://s.yimg.com/uu/api/res/1.2/o1YsUTaaZxuqKLK86t0wew--~B/aD0yODk1O3c9NDM0MjthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/085ec5e156bb9c378928d743edae91a0'
        }

        rss_reader.update_db(
            database=test_db,
            date="20220906",
            article=test_article
        )
        test_list = test_db.get("20220906")
        self.assertIn(test_article, test_list)
#
#
#     def test_update_db_negative(self):
#         test_db = pickledb.load("rss_reader/test_rss.db", False)
#         print(type(test_db))
#         test_article = {
#             "Title": "World's second-tallest roller coaster is permanently closing",
#             "Date": "Tue, 06 Sep 2022 15:50:32 +0100",
#             "Image": "https://s.yimg.com/uu/api/res/1.2/A8E8MEz.vcMmMiyYuA73Vw--~B/aD0xNTk0O3c9MTgwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/a85232b31cf044b7d8d0567733aef771",
#             "Link": "https://news.yahoo.com/worlds-second-tallest-roller-coaster-155032974.html"
#         }
#
#         rss_reader.update_db(
#             database=test_db,
#             date="20220906",
#             article=test_article
#         )
#         test_dict = test_db.get("20220906")
#         self.assertIn(test_article, test_dict)

#
class CreateJson(TestCase):

     def test_create_json_positive(self):
        # articles_list = [
        #     {
        #          'Title': "Woman's rape cries go unheard in unmonitored drug sting",
        #          'Date': 'Tue, 13 Sep 2022 14:27:08 +0100',
        #          'Link': 'https://news.yahoo.com/womans-rape-cries-unheard-unmonitored-142708098.html',
        #          'Image': 'https: // s.yimg.com / uu / api / res / 1.2 / R5j0twnGjY3dFUsENIcKcA - -~B / aD00MDAwO3c9NjAwMDthcHBpZD15dGFjaHlvbg - - / https: // media.zenfs.com / en / ap.org / cf6457b451fe2161f930f26932654a0b'
        #      },
        #      {
        #          'Title': "Abcarian: The queen is dead, a country mourns, yet poor Meghan Markle still can'tcatchabreak",
        #          'Date': 'Wed, 14 Sep 2022 10:05:21 +0100',
        #          'Link': 'https://news.yahoo.com / abcarian - queen - dead - country - mourns - 100521724.html',
        #          'Image': 'https: // s.yimg.com / uu / api / res / 1.2 / 5p_SnRxcJYK.Z6LkNJzIFQ - -~B / aD01NjA7dz04NDA7YXBwaWQ9eXRhY2h5b24 - / https: // media.zenfs.com / en / los_angeles_times_opinion_902 / fe424b0602b7bab5b91349aacae8d523'""
        #      }
        #                   ]

        articles_list = [{"Title": "MyTitle1", "Date": "MyDate1"}, {"Title": "MyTitle2", "Date": "MyDate2"}]

        # result_json = [
        #    {
        #      "Title": "Woman's rape cries go unheard in unmonitored drug sting",
        #      "Date": "Tue, 13 Sep 2022 14:27:08 +0100",
        #      "Link": "https://news.yahoo.com/womans-rape-cries-unheard-unmonitored-142708098.html",
        #      "Image": "https://s.yimg.com/uu/api/res/1.2/R5j0twnGjY3dFUsENIcKcA--~B/aD00MDAwO3c9NjAwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/cf6457b451fe2161f930f26932654a0b"
        #    },
        #    {
        #      "Title": "Abcarian: The queen is dead, a country mourns, yet poor Meghan Markle still can't catch a break",
        #      "Date": "Wed, 14 Sep 2022 10:05:21 +0100",
        #      "Link": "https://news.yahoo.com/abcarian-queen-dead-country-mourns-100521724.html",
        #      "Image": "https://s.yimg.com/uu/api/res/1.2/5p_SnRxcJYK.Z6LkNJzIFQ--~B/aD01NjA7dz04NDA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/los_angeles_times_opinion_902/fe424b0602b7bab5b91349aacae8d523"
        #   }
        #  ]

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
        articles_json.loads()

        self.assertEqual(articles_json, result_json)


    # class ConvertToHtml(TestCase):
    #
    #     def test_convert_to_html(self):
    #
    #     def convert_to_html(articles):
    #         """
    #         In case of using `--to_html` argument the utility converts the news into HTML format
    #         :param articles: JSON string with articles to be converted into HTML format
    #         :return html_output: HTML Table representation
    #         """
    #         json_articles = create_json(articles)
    #         logger.debug(f"Converting the news to HTML format...")
    #         html_output = json2html.convert(json=json_articles)
    #         return html_output
    #


if __name__ == "__main__":
     unittest.main()



