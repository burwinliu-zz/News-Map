"""
 Beautiful Soup is made available under the MIT license: Copyright (c) 2004-2019 Leonard Richardson and is used in this
 code. It belongs to all respective owners. Its website can be found: https://www.crummy.com/software/BeautifulSoup/
"""
import datetime
import re
import warnings
from timeit import default_timer as timer
from typing import List, Dict

import six.moves.urllib as urllib
from bs4 import BeautifulSoup
from six.moves import cPickle as pkl

from .data import *

'''Take in url function and scrape -- using google '''


def _trim(tf: List[str]) -> List[str]:
    """

    :param tf: this takes in a list
    :return: and attempts to return a cut down list
    """
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
    """
    this makes a single soup readable
    :param sp:
    :return:
    """
    for script in sp(['script', 'style', 'header', 'footer', 'title', 'meta', '[document]', 'head']):
        print(str(script.extract()))
    text = sp.get_text()
    lines = [line.strip() for line in text.splitlines()]
    chunks = [phrase.strip() for line in lines for phrase in line.split('  ')]
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return {'text': text, 'title': sp.title}


def soups_to_strs(soups: List[BeautifulSoup]) -> List[Dict]:
    return [make_readable(soup) for soup in soups]


def headline_change(headline: str) -> str:
    '''
    :param headline:
    :return:
    '''
    headline = headline.strip()
    headline = headline.replace('\'', '\"')
    return headline


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
        self.nameBase = CountryNames()
        self.amount_loaded = 0

    def find_links(self) -> List[str]:
        """
        this is a helper method for the init
        :return:
        """
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

        for c, gannon in enumerate(re.findall("(https://(([a-z0-9]+\.)+[a-z]+)((/[^(/\s\"<>)]+)*))", str(
                self.information))):  # need to change indecies around for an optional (www)
            if valid(gannon):
                triforce.append({'full': gannon[0], 'site': gannon[2][:-1], 'information': gannon[3]})
        return triforce

    def get_all_articles(self, predict_country=False) -> dict:
        """

        :param predict_country:
        :return: sample of everything
        """
        return self.get_sample(batch_size=float("inf"), predict_country=predict_country)

    def gen_samples(self, batch_size: int = 10, predict_country=False, early_trim=False) -> dict:
        """
        This is a generator that you can use to get samples or something
        :param early_trim:
        :param predict_country:
        :param batch_size: how much you want to read at a time
        predict_country: if you want it to try to attempt to predict countries
        :return:
        """
        start = timer()
        loaded_sites = list()
        for i in self.listings:
            print(i)
            try:
                if i['full'][-3:] == 'the':
                    i['full'] = i['full'][:-3]
                    print("hit")
                brought = urllib.request.urlopen(i['full']).read()
                sp = BeautifulSoup(brought, 'html.parser')
                self.amount_loaded += 1
                loaded_sites.append(i)
                i['request'] = brought
                i['soup'] = sp
                if early_trim:
                    i['text'] = make_readable(sp)
                if predict_country:
                    i['country'] = self.predict_country(i)
                if len(loaded_sites) >= batch_size:
                    end = timer()
                    print("Time elapsed:" + str(end - start))
                    yield loaded_sites
                    start = timer()
                    loaded_sites = list()
            except urllib.error.HTTPError:
                print("failed on " + str(i['full']) + 'the HTTP or something bad')
            except Exception as e:
                print('failed on ' + str(i['full']) + 'with exception' + str(e))
        yield loaded_sites

    def save(self, filename=None) -> list:
        """
        @todo actually complete this, will not actually work
        :param filename:
        :return:
        """
        warnings.warn('Not fully implemented yet, plz dont use this')
        with open(str(self.time) + '.pkl' if filename is None else filename, 'wb') as fp:
            pkl.dump(self, fp)

    def predict_country(self, listing: dict) -> Prediction:
        '''

        :param listing:
        :return: a prediction
        '''
        target = listing['soup'].head.title
        return self.nameBase.predict(str(target))

    def __str__(self):
        return str(self.title) + '\ncreated on' + str(self.time) + '\nwith :' + str(len(self.listings)) + 'links'
