from unittest import TestCase
import warnings
import youcomment.youtube as yt

parse = yt.YoutubeVideoBot.parse_url


class TestRun(TestCase):
    def test_default_run_valid(self):
        with warnings.catch_warnings():
            self.assertTrue(yt.YoutubeVideoBot('https://www.youtube.com/watch?v=Es44QTJmuZ0').run())


class TestYoutubeURLParse(TestCase):
    def test_default_link_type(self):
        self.assertEqual(parse("https://www.youtube.com/watch?v=zivTvd0Sd9A"),
                         'zivTvd0Sd9A')

    def test_watch_query(self):
        self.assertEqual(
            parse("https://www.youtube.com/watch?v=c-bT6tZSgVY&feature=youtu.be"),
            'c-bT6tZSgVY')

    def test_feature(self):
        self.assertEqual(parse(
            "https://www.youtube.com/watch?feature=player_detailpage&v=biVLGTAMC_U#t=31s"),
            'biVLGTAMC_U')

    def test_normal_leading_underscore(self):
        self.assertEqual(
            parse("https://www.youtube.com?v=_reJWBQs0Qo"), '_reJWBQs0Qo')

    def test_embedded(self):
        self.assertEqual(
            parse("https://www.youtube.com/embed/M7lc1UVf-VE"), 'M7lc1UVf-VE')

    def test_short(self):
        self.assertEqual(parse("https://youtu.be/awF0vWgCVrs"), 'awF0vWgCVrs')

    def test_short_with_time(self):
        self.assertEqual(
            parse("https://youtu.be/9RdlYD8TyoQ?t=23"), '9RdlYD8TyoQ')

    def test_no_https(self):
        self.assertEqual(parse("youtu.be/9RdlYD8TyoQ?"), '9RdlYD8TyoQ')

    def test_leading_underscore(self):
        self.assertEqual(
            parse("https://www.youtube.com/v/_reJWBQs0Qo"), '_reJWBQs0Qo')

    def test_queries(self):
        self.assertEqual(
            parse("http://www.youtube.com/v/-wtIMTCHWuI?version=3&autohide=1"), '-wtIMTCHWuI')

    def test_attribution_link(self):
        self.assertEqual(parse(
            "http://www.youtube.com/attribution_link?a=JdfC0C9V6ZI&u=%2Fwatch%3Fv%3DEhxJLojIE_o%26feature%3Dshare"),
            'EhxJLojIE_o')

    def test_json(self):
        self.assertEqual(parse(
            "http://www.youtube.com/oembed?url=http%3A//www.youtube.com/watch?v%3D-wtIMTCHWuI&format=json"),
            '-wtIMTCHWuI')

    def test_email_link(self):
        self.assertEqual(parse(
            "https://www.youtube.com/attribution_link?a=8g8kPrPIi-ecwIsS&u=/watch%3Fv%3DyZv2daTWRZU%26feature%3Dem-uploademail"),
            'yZv2daTWRZU')
