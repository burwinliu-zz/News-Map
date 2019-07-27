"""
 Beautiful Soup is made available under the MIT license: Copyright (c) 2004-2019 Leonard Richardson and is used in this
 code. It belongs to all respective owners. Its website can be found: https://www.crummy.com/software/BeautifulSoup/
"""
import six.moves.urllib as urllib
from bs4 import BeautifulSoup,SoupStrainer
import html5lib
import re
import httplib2
'''Take in url function and scrape -- using google '''


class Headlines:
    def __init__(self, url: str='https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'):
        """

        :param url:
        """
        link = url
        zelda = urllib.request.urlopen(link)
        self.information = zelda.read()
        self.soup = BeautifulSoup(self.information, 'html.parser')
        self.title = self.soup.head.title
        self.listings=self.findlinks()


    def findLinks(self):
        triforce = []

        def valid(sep):
            link = sep[2]
            deadlinks = ['google', 'gstatic', 'ggpht', 'schema', 'youtube', 'blogger', 'apple']
            for dink in deadlinks:
                if link.find(dink) >= 0:
                    return False
            if len(sep[3]) == 0:
                return False
            if sep[0].find('amp') >= 0:
                return False
            return True
        for c, gannon in enumerate(re.findall("(https://(([a-z0-9]+\.)+[a-z]+)(/([^(/\s\"<>)]+))*)", str(self.information))):
            if valid(gannon):
                triforce.append(gannon[0])
        return triforce