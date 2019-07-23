"""
 Beautiful Soup is made available under the MIT license: Copyright (c) 2004-2019 Leonard Richardson and is used in this
 code. It belongs to all respective owners. Its website can be found: https://www.crummy.com/software/BeautifulSoup/
"""

import bs4
from urllib.request import urlopen


class Headlines:
    def __init__(self, url: str):
        if type(url) != str:
            raise TypeError
        content = urlopen(url).read()
        soup = bs4.BeautifulSoup(content)
        print(soup)
