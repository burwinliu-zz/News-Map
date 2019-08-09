"""
Subclass of database to represent the news database -- major changes in the adding of items

SEE data.py for use

("news_number", "SERIAL", "PRIMARY KEY"),
("url", "TEXT"),
("ISO_Code", "SMALLINT")
"""
from collections import defaultdict

import webpage.data.python_scripts.database as database

from webpage.data.python_scripts import sql_manage


class NewsDatabase(database.Database):
    def __init__(self):
        col_names = tuple(("news_number", "url", "headline", "ISO_Code"))
        col_types = tuple(("int", "str", "str", "int"))
        super().__init__("public", "news", col_names, col_types)

    def add_many_inputs(self, data_names: tuple, data_input: tuple) -> dict:
        next_value = int(sql_manage.get_data("SELECT last_value FROM public.news_news_number_seq;")[0])
        iso_index = data_names.index("ISO_Code")
        res = dict()
        for item in data_names[iso_index]:
            if item in res:
                res[item].append(next_value)
                next_value += 1
            else:
                res[item] = [next_value]
                next_value += 1
        super().add_many_inputs(data_names, data_input)
