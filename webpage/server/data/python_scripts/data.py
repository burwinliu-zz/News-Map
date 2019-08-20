"""
    Will take countries data and serve into postgresql
    Will take colours spectrum data and serve into postgresql
    Will take files from scraping and link

    HERE IS MAIN FILE, try not to touch other files
"""

import pycountry
import webpage.server.data.python_scripts.sql_manage as setup
import webpage.server.data.python_scripts.database as database
import webpage.server.data.python_scripts.overview_database as overview_db
import webpage.server.data.python_scripts.news_database as news_db
import re


def store_countries(db: database.Database) -> None:
    """
    Store country info into database

    :return:None
    """
    db.add_many_inputs(tuple(("NUMERIC", "iso3166_code", "country_name")), tuple((get_country_codes_and_names())))


def store_articles(urls: tuple, headlines: tuple, iso_codes: tuple):
    """
    store amount of articles, given in tuples to databases

    :param urls: tuple
    :param headlines: tuple
    :param iso_codes: tuple
    :return: None
    """
    # Variable setup
    to_exe = list()
    ndb = news_db.NewsDatabase()
    odb = overview_db.OverviewDatabase()
    # Double checking your inputs are good, else we crash
    if not (len(urls) == len(headlines) == len(iso_codes)):
        raise Exception(f"Your urls, headlines and iso_codes do not have same lengths")
    for i in range(len(urls)):
        # Double checking your inputs are good, else we crash
        if type(urls[i]) != str or type(headlines[i]) != str or type(iso_codes[i]) != int:
            raise Exception(f"Input {urls[i]}, {headlines[i]} and {iso_codes[i]} are improper at position {i}")

        to_exe.append(tuple((urls[i], headlines[i], iso_codes[i])))

    param = ndb.add_many_inputs(tuple(("url", "headline", "ISO_Code")), tuple(to_exe))
    odb.add_many_inputs(tuple(("ISO_Code", "News_list")), tuple(((k, v) for k, v in param.items())))


def _init_sys_info() -> database.Database:
    """
    init sys info db
    :return: database.Database
    """
    if setup.test() == 0:
        raise setup.DatabaseError
    param = setup.init_db("system", "sys_info",
                          [
                              ("schema", "TEXT"),
                              ("name", "TEXT", "UNIQUE"),
                              ("columns", "TEXT"),
                              ("types", "TEXT")
                          ],
                          sys_table=True
                          )
    res = database.Database(*param)
    return res


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
                          ],
                          sys_table=False
                          )
    res = database.Database(*param)
    return res


def init_news() -> news_db.NewsDatabase:
    """
    init the news database
    Will store news article info

    :return: database.Database object
    """
    if setup.test() == 0:
        raise setup.DatabaseError
    setup.init_db("public", "news",
                  [
                      ("news_number", "SERIAL", "PRIMARY KEY"),
                      ("url", "TEXT", "NOT NULL"),
                      ("headline", "VARCHAR(75)", "NOT NULL"),
                      ("ISO_Code", "SMALLINT",),
                  ]
                  )
    res = news_db.NewsDatabase()
    return res


def init_news_overview() -> overview_db.OverviewDatabase:
    """
    init the news overview
    Will store news overview -- number of hits, corresponding colour and other info

    :return: database.Database object
    """
    if setup.test() == 0:
        raise setup.DatabaseError
    res = overview_db.OverviewDatabase()
    setup.init_db("public", "news_overview",
                  [
                      ("ISO_Code", "SMALLINT", "PRIMARY KEY"),
                      ("News_list", "BIGINT[]"),
                  ]
                  )
    return res


def reset_news():
    setup.execute_command("DELETE FROM public.news")
    setup.execute_command("ALTER SEQUENCE public.news_news_number_seq RESTART WITH 1")


def reset_overview():
    setup.execute_command("DELETE FROM public.news_overview")


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
    # For reset of database

    '''
    reset_news()
    reset_overview()
    '''

    # For setup of databases
    '''
    _init_sys_info()
    countries = _init_countries()
    store_countries(countries)
    init_news()
    init_news_overview()
    '''

