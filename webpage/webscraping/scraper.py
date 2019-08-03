"""
 Beautiful Soup is made available under the MIT license: Copyright (c) 2004-2019 Leonard Richardson and is used in this
 code. It belongs to all respective owners. Its website can be found: https://www.crummy.com/software/BeautifulSoup/
"""
import six.moves.urllib as urllib
from bs4 import BeautifulSoup, SoupStrainer
import html5lib
import re
import httplib2
from typing import List, Tuple, Dict
from six.moves import cPickle as pkl
import datetime
from tqdm import tqdm

'''Take in url function and scrape -- using google '''


def _trim(tf: List[str]) -> List[str]:
    '''

    :param tf: this takes in a list
    :return: and attempts to return a cut down list
    '''
    rehold = []

    def check(site):
        target = site['information']
        return target.find('.jpg') >= 0 or target.find('jpeg') >= 0 or target.find('.mp4') >= 0 or target.find(
            '/image') >= 0 or target.find('.JPG') >= 0 or site['full'].find('images.wsj') >= 0 or site['full'].find(
            'cbsnews1.cbsistatic') >= 0

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


def make_readable(sp: BeautifulSoup) -> Dict:
    '''
    this makes a single soup readable
    :param sp:
    :return:
    '''
    for script in sp(['script', 'style', 'header', 'footer']):
        script.extract()
    text = sp.get_text()
    lines = [line.strip() for line in text.splitlines()]
    chunks = [phrase.strip() for line in lines for phrase in line.split('  ')]
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return {'text': text, 'title': sp.title}


def soups_to_strs(soups: List[BeautifulSoup]) -> List[Dict]:
    return [make_readable(soup) for soup in soups]


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
        self.listings = self.find_links()
        self.listings = _trim(self.listings)
        self.time = datetime.datetime.now()

    def find_links(self) -> List[str]:
        '''
        this is a helper method for the init
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

    def get_all_articles(self) -> List[BeautifulSoup]:
        '''
        i don't think using this would be the best method, probably the generator would be a better choice
        :return:
        '''
        loaded_sites = list()
        for i in tqdm(self.listings, desc='loading ALL sites'):
            try:
                brought = urllib.request.urlopen(i['full']).read()
                sp = BeautifulSoup(brought, 'html.parser')
                loaded_sites.append(sp)
            except urllib.error.HTTPError:
                print("failed on " + str(i))
            except Exception as e:
                print('failed on ' + str(i) + 'with exception' + str(e))
        return loaded_sites

    def get_sample(self, batch_size: int = 10) -> List[BeautifulSoup]:
        '''
        this might be the better way
        :param batch_size: how much you want to read at a time
        :return:
        '''
        loaded_sites = list()
        for i in self.listings:
            try:
                brought = urllib.request.urlopen(i['full']).read()
                sp = BeautifulSoup(brought, 'html.parser')
                loaded_sites.append(sp)
                if len(loaded_sites) >= batch_size:
                    yield loaded_sites
                    loaded_sites = list()
            except urllib.error.HTTPError:
                print("failed on " + str(i))
            except Exception as e:
                print('failed on ' + str(i) + 'with exception' + str(e))
        return loaded_sites

    def save(self, filename=None) -> list:
        '''
        @todo actually complete this, will not actually work
        :param filename:
        :return:
        '''
        with open(str(self.time) + '.pkl' if filename is None else filename, 'wb') as fp:
            pkl.dump(self.listings, fp)

    def __str__(self):
        return self.title + '\ncreated on' + self.time + '\nwith :' + len(self.listings) + 'links'
