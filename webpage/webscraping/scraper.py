"""
 Beautiful Soup is made available under the MIT license: Copyright (c) 2004-2019 Leonard Richardson and is used in this
 code. It belongs to all respective owners. Its website can be found: https://www.crummy.com/software/BeautifulSoup/
"""
import six.moves.urllib as urllib
from bs4 import BeautifulSoup, SoupStrainer
import html5lib
import re
import httplib2
from typing import List
from six.moves import cPickle as pkl
import datetime

'''Take in url function and scrape -- using google '''


class Headlines:
    def __init__(self,
                 url: str = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'):
        """

        :param url: this is the place in google news that we will use to check from
        """
        link = url
        zelda = urllib.request.urlopen(link)
        self.information = zelda.read()
        self.soup = BeautifulSoup(self.information, 'html.parser')
        self.title = self.soup.head.title
        self.listings = self.trim(self.findlinks())
        self.time = datetime.datetime.now()

    def findLinks(self) -> List[str]:
        '''
        this is a helper method for the main
        :return:
        '''
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

        for c, gannon in enumerate(
                re.findall("(https://(([a-z0-9]+\.)+[a-z]+)(/([^(/\s\"<>)]+))*)", str(self.information))):
            if valid(gannon):
                triforce.append(gannon[0])

        return triforce

    def trim(self,tf):
        rehold = []

        def check(site):
            target = site['information']
            return target.find('.jpg') >= 0 or target.find('jpeg') >= 0 or target.find('.mp4') >= 0 or target.find(
                '/image') >= 0 or target.find('.JPG') >= 0 or site['full'].find('images.wsj') >= 0

        last = None
        for dol in tf:

            if last is None:

                last = dol
            else:
                if check(dol):
                    last['pic'] = dol['full']
                elif dol['site'] == 'reutersmedia':
                    continue  # do nothing, ive got no idea why there is a 1x1 image here.
                elif last['full'] == dol['full']:
                    continue  # this is if it is a repeater
                else:
                    rehold.append(dol)
                    last = dol
        return rehold

    def save(self, filename=None):
        with open(self.time if filename is None else filename, 'wb') as fp:
            pkl.dump(self, fp)

    def __str__(self):
        return self.title + '\ncreated on' + self.time + '\nwith :' + len(self.listings) + 'links'
