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


def store_countries() -> None:
    if setup.test() == 0:
        raise setup.DatabaseError
    param = setup.init_db("countries",
                      [
                          ("NUMERIC", "SMALLINT", "PRIMARY KEY"),
                          ("iso3166_code", "VARCHAR(2)", "NOT NULL"),
                          ("country_name", "VARCHAR(75)", "NOT NULL")
                      ]
                      )
    db = database.Database(*param)
    db.add_many_inputs(tuple(("NUMERIC", "iso3166_code", "country_name")), tuple((get_country_codes_and_names())))


def get_country_codes_and_names():
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
    store_countries()
