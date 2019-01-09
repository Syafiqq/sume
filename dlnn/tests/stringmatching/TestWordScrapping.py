import requests
from bs4 import BeautifulSoup

from dlnn.tests.ml.testcase import TestCase


class TestWordScrapping(TestCase):
    def test_word_scrapping1(self):
        url = 'http://j-ptiik.ub.ac.id/index.php/j-ptiik/article/view/7'
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, "html5lib")
        type(soup)
        print(soup.find("div", {'class': 'article-abstract'}))
        pass
