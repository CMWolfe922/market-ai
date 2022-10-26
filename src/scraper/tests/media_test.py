import unittest
from ..media.media.newspaper import NewsSpider


class MediaTestCase(unittest.TestCase):
    def test_url_extraction(self):
        spider = NewsSpider()
        urls = spider.parse()
        print(urls)
        self.assertEqual(list(), urls)


if __name__ == '__main__':
    unittest.main()
