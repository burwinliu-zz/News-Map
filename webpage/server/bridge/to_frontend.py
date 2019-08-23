# create json folder, serve to a url, and provide to parse.js
from ..webscraping import scraper
from ..data.python_scripts.sql_manage import retrieve
from .get_data import refresh_data
import math


def reload_data():
    worker = scraper.Headlines()
    sample = worker.gen_samples(predict_country=True)
    bite = sample.__next__()
    refresh_data(bite)


def get_colour_data() -> dict:
    """
    Get data and properly format for the GET http request function
    TODO Rename and make more clear that this is for COLOURS DICT
    :return: dict
    """
    # Create new scraper.headlines object to refresh
    overview = retrieve("SELECT * FROM public.news_overview")
    countries = retrieve("SELECT * FROM public.countries")
    news = retrieve("SELECT * FROM public.news")
    news_overview = _attach_code(overview, countries, news)
    colours_dict = _assign_colours(news_overview)
    return colours_dict


def get_colour():
    return {
        1: '#00429d',
        2: '#07449e',
        3: '#0d469f',
        4: '#1248a0',
        5: '#164aa1',
        6: '#1a4ba2',
        7: '#1d4da2',
        8: '#204fa3',
        9: '#2351a4',
        10: '#2653a5',
        11: '#2855a6',
        12: '#2b57a7',
        13: '#2d59a8',
        14: '#2f5ba9',
        15: '#315daa',
        16: '#335faa',
        17: '#3561ab',
        18: '#3763ac',
        19: '#3965ad',
        20: '#3b67ae',
        21: '#3d69af',
        22: '#3e6bb0',
        23: '#406db1',
        24: '#426fb2',
        25: '#4471b2',
        26: '#4573b3',
        27: '#4775b4',
        28: '#4877b5',
        29: '#4a79b6',
        30: '#4c7bb7',
        31: '#4d7db8',
        32: '#4f7fb9',
        33: '#5081b9',
        34: '#5283ba',
        35: '#5385bb',
        36: '#5488bc',
        37: '#568abd',
        38: '#578cbe',
        39: '#598ebf',
        40: '#5a90c0',
        41: '#5b92c0',
        42: '#5d94c1',
        43: '#5e96c2',
        44: '#6098c3',
        45: '#619ac4',
        46: '#629dc5',
        47: '#649fc6',
        48: '#65a1c7',
        49: '#66a3c7',
        50: '#67a5c8',
        51: '#69a7c9',
        52: '#6aaaca',
        53: '#6baccb',
        54: '#6caecc',
        55: '#6eb0cd',
        56: '#6fb2cd',
        57: '#70b4ce',
        58: '#71b7cf',
        59: '#73b9d0',
        60: '#74bbd1',
        61: '#75bdd2',
        62: '#76bfd3',
        63: '#77c2d3',
        64: '#79c4d4',
        65: '#7ac6d5',
        66: '#7bc8d6',
        67: '#7ccbd7',
        68: '#7dcdd8',
        69: '#7fcfd8',
        70: '#80d1d9',
        71: '#81d4da',
        72: '#82d6db',
        73: '#83d8dc',
        74: '#84dadd',
        75: '#85ddde',
        76: '#87dfde',
        77: '#88e1df',
        78: '#89e3e0',
        79: '#8ae6e1',
        80: '#8be8e2',
        81: '#8ceae3',
        82: '#8dede3',
        83: '#8eefe4',
        84: '#8ff1e5',
        85: '#91f3e6',
        86: '#92f6e7',
        87: '#93f8e8',
        88: '#94fae8',
        89: '#95fde9',
        90: '#96ffea'
    }


def _assign_colours(overview: dict) -> dict:
    """
    Assign colours to each key of the overview news dict
    :param overview: dict
    :return: dict
    """
    largest = _max_item(overview)
    res = dict()
    for key, item in overview.items():
        res[key] = _on_scale(len(item) / largest)
    return res


def _on_scale(percentage: float) -> str:
    """
    find out where on the scale the percentage falls and return corresponding rgb to the scale
    :param percentage: float
    :return: str
    """
    return get_colour()[math.ceil(percentage * 90)]


def _attach_code(overview: list, countries: list, news: list) -> dict:
    """
    Attach the correct code to each of the news_list (in iso 2char format)
    :param overview: list of overview db
    :param countries: list of countries db
    :param news: list of news db
    :return: dict with attached keys
    """
    countries = _countries_to_dict(countries)
    res = dict()
    for i in overview:
        try:
            res[countries[i[0]]] = i[1]
        except KeyError:
            if i[0] == 0:
                res["NO_COUNTRY"] = i[1]
            else:
                raise KeyError
    return res


def _countries_to_dict(ls: list) -> dict:
    """
    convert countries db in the form of a list to a dict
    :param ls: list
    :return: dict
    """
    res = dict()
    for i in ls:
        res[i[0]] = i[1]
    return res


def _max_item(d: dict) -> int:
    """
    find largest len item of a dict
    :param d: dict[key: list]
    :return: int
    """
    largest = 0
    for i in d.values():
        temp = len(i)
        if temp > largest:
            largest = temp
    return largest
