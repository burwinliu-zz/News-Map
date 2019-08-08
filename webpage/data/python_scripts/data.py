"""
    Will take countries data and serve into postgresql
    Will take colours spectrum data and serve into postgresql
    Will take files from scraping and link

    HERE IS MAIN FILE, try not to touch other files
"""

import pycountry
import webpage.data.python_scripts.sql_manage as setup
import webpage.data.python_scripts.database as database
import webpage.data.python_scripts.overview_database as overview_database
import webpage.data.python_scripts.news_database as news_database
import re


def store_countries(db: database.Database) -> None:
    """
    Store country info into database

    :return:None
    """
    db.add_many_inputs(tuple(("NUMERIC", "iso3166_code", "country_name")), tuple((get_country_codes_and_names())))


def store_articles(ndb: news_database.NewsDatabase, odb: overview_database, urls: tuple, iso_codes: tuple):
    to_store = ndb.add_many_inputs(urls, iso_codes)
    for iso in to_store:
        odb.add_input(iso, to_store[iso])


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


def init_news():
    """
    init the news database
    Will store news article info

    :return: database.Database object
    """
    if setup.test() == 0:
        raise setup.DatabaseError
    param = setup.init_db("public", "news",
                          [
                              ("news_number", "SERIAL", "PRIMARY KEY"),
                              ("url", "TEXT"),
                              ("ISO_Code", "SMALLINT")
                          ]
                          )
    res = database.Database(*param)
    return res


def init_news_overview():
    """
    init the news overview
    Will store news overview -- number of hits, corresponding colour and other info

    :return: database.Database object
    """
    if setup.test() == 0:
        raise setup.DatabaseError
    param = setup.init_db("public", "news_overview",
                          [
                              ("ISO_Code", "SMALLINT", "UNIQUE"),
                              ("News_list", "BIGINT[]"),
                              ("Colour", "SMALLINT")
                          ]
                          )
    res = database.Database(*param)

    return res


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
