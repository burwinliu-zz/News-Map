# create json folder, serve to a url, and provide to parse.js
from webpage.server.data.python_scripts.sql_manage import retrieve
import math


def get_data():
    """
    Get data and properly format for the GET http request function
    TODO Rename and make more clear that this is for COLOURS DICT
    :return:
    """
    # TODO add in a reload backend command (for data from scraping)
    overview = retrieve("SELECT * FROM public.news_overview")
    countries = retrieve("SELECT * FROM public.countries")
    news = retrieve("SELECT * FROM public.news")
    news_overview = _attach_code(overview, countries, news)
    colours_dict = _assign_colours(news_overview)
    print(colours_dict)
    return


def _assign_colours(overview: dict) -> dict:
    """
    Assign colours to each key of the overview news dict
    :param overview: dict
    :return: dict
    """
    largest = _max_item(overview)
    res = dict()
    for key, item in overview.items():
        res[key] = _on_scale(len(item)/largest)
    return res


def _on_scale(percentage: float) -> str:
    """
    find out where on the scale the percentage falls and return corresponding rgb to the scale
    :param percentage: float
    :return: str
    """
    colour = {
            1: "#006eea",   2: "#1f6ee8",  3: "#2e6ee6",  4: "#396de4",  5: "#426de1",  6: "#496cdf",
            7: "#506cdd",   8: "#566cdb",  9: "#5c6bd8", 10: "#616bd6", 11: "#666bd4", 12: "#6a6ad2", 13: "#6e6ad0",
            14: "#7369cd", 15: "#7669cb", 16: "#7a69c9", 17: "#7e68c7", 18: "#8168c5", 19: '#8468c2', 20: '#8867c0',
            21: '#8b67be', 22: '#8e66bc', 23: '#9066ba', 24: '#9366b7', 25: '#9665b5', 26: '#9965b3', 27: '#9b64b1',
            28: '#9e64af', 29: '#a064ad', 30: '#a263aa', 31: '#a563a8', 32: '#a762a6', 33: '#a962a4', 34: '#ab62a2',
            35: '#ae61a0', 36: '#b0619d', 37: '#b2609b', 38: '#b46099', 39: '#b65f97', 40: '#b85f95', 41: '#ba5e93',
            42: '#bb5e91', 43: '#bd5e8e', 44: '#bf5d8c', 45: '#c15d8a', 46: '#c35c88', 47: '#c45c86', 48: '#c65b84',
            49: '#c85b82', 50: '#c95a7f', 51: '#cb5a7d', 52: '#cd597b', 53: '#ce5979', 54: '#d05877', 55: '#d15875',
            56: '#d35773', 57: '#d45771', 58: '#d6566e', 59: '#d7566c', 60: '#d9556a', 61: '#da5568', 62: '#dc5466',
            63: '#dd5464', 64: '#df5362', 65: '#e0535f', 66: '#e1525d', 67: '#e3525b', 68: '#e45159', 69: '#e55057',
            70: '#e75055', 71: '#e84f52', 72: '#e94f50', 73: '#eb4e4e', 74: '#ec4d4c', 75: '#ed4d49', 76: '#ee4c47',
            77: '#f04c45', 78: '#f14b43', 79: '#f24a40', 80: '#f34a3e', 81: '#f4493c', 82: '#f64839', 83: '#f74837',
            84: '#f84734', 85: '#f94632', 86: '#fa452f', 87: '#fc452c', 88: '#fd442a', 89: '#fe4327', 90: '#ff4224'
    }
    return colour[math.ceil(percentage*90)]


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
        res[countries[i[0]]] = i[1]
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
    for i in d.items():
        temp = len(i)
        if temp > largest:
            largest = temp
    return largest


# For testing
get_data()
