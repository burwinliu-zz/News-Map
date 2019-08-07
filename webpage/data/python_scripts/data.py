"""
    Will take countries data and serve into postgresql
    Will take colours spectrum data and serve into postgresql
    Will take files from scraping and link
    Aland == Aland islands
    French
"""

import pycountry
import webpage.data.python_scripts.sql_manage as setup
import webpage.data.python_scripts.database as database
import re


# ToDo Finish writing these init functions and store articles, remember to link between overview, colour and articles
def store_bulk_articles(news_article: tuple, location: tuple) -> None:
    """
    Will add in many articles to the news article database

    :param news_article: list of strings -- news article url web addresses
    :param location: list of strings -- corresponding web adresses
    :return:
    """


def store_article(news_article: str, location: str) -> None:
    """
    To help with adding one article at a time to a news database

    :param news_article: str --  news article url web address
    :param location: str of ISO-3166-1 code (link to country database)
    :return: None
    """
    pass


def store_countries(db: database.Database) -> None:
    """
    Store country info into database

    :return:None
    """
    db.add_many_inputs(tuple(("NUMERIC", "iso3166_code", "country_name")), tuple((get_country_codes_and_names())))


def init_session() -> None:
    """
    Start of each web-page session

    :return: None
    """
    pass


def _init_countries() -> database.Database:
    """
    init the countries database
    Will store countries numeric, iso and country name

    :return: database.Database object
    """
    if setup.test() == 0:
        raise setup.DatabaseError
    param = setup.init_db("public", "countries",
                          [
                              ("NUMERIC", "SMALLINT", "PRIMARY KEY"),
                              ("iso3166_code", "VARCHAR(2)", "NOT NULL"),
                              ("country_name", "VARCHAR(75)", "NOT NULL")
                          ]
                          )
    res = database.Database(*param)

    return res


def _init_news():
    """
    init the news database
    Will store news article info

    :return: database.Database object
    """
    pass


def _init_news_overview():
    """
    init the news overview
    Will store news overview -- number of hits, corresponding colour and other info

    :return: database.Database object
    """
    pass


def get_country_codes_and_names() -> list:
    """
    for retrieving all country codes and stuff

    :return: list of tuples that contain all country info
    """
    list_of_country = pycountry.countries
    res = list()
    for country in list_of_country:
        if "'" in country.name:
            to_input = re.sub(r"'", "''", country.name)
            res.append(tuple((country.numeric, country.alpha_2, to_input)))
            continue
        res.append(tuple((country.numeric, country.alpha_2, country.name)))
    return res


if __name__ == "__main__":
    to_pass = _init_countries()
    store_countries(to_pass)
