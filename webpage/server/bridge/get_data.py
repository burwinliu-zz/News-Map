import warnings
from typing import List

from ..data.python_scripts.data import store_articles


def refresh_data(data: List[dict]) -> None:
    """
    Get data from refreshed object in backend scraping and input to database

    :param data: List[dict] with keys "country", "headline" and "full"
    :return: None
    """
    to_add_urls = list()
    to_add_headlines = list()
    to_add_iso_codes = list()
    for i in data:
        try:
            to_add_iso_codes.append(i['country'].get_country)
            to_add_urls.append(i['full'])
            to_add_headlines.append(i['headline'])
        except KeyError:
            warnings.warn(f"Item {i} not given proper formatting with proper items")
    store_articles(tuple(to_add_urls), tuple(to_add_headlines), tuple(to_add_iso_codes))

