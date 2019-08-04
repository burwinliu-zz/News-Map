"""
    Will take countries data and serve into postgresql
    Will take colours spectrum data and serve into postgresql
    Will take files from scraping and link
    Aland == Aland islands
    French
"""

import pycountry
import webpage.data.python_scripts.sql_manage as setup


def store_countries() -> None:
    if setup.test() == 0:
        raise setup.DatabaseError
    db = setup.init_db("countries",
                  [
                      ("NUMERIC", "SMALLINT", "PRIMARY KEY"),
                      ("iso3166_code", "VARCHAR(2)", "NOT NULL"),
                      ("country_name", "VARCHAR(75)", "NOT NULL")
                  ]
                  )
    db.add_many_inputs()
