"""
Subclass of database to represent the news database -- major changes in the adding of items

SEE data.py for use

("news_number", "SERIAL", "PRIMARY KEY"),
("url", "TEXT"),
("ISO_Code", "SMALLINT")
"""

import database
from config import retrieve

Database = database.Database


class NewsDatabase(Database):
    def __init__(self):
        """
        Init the database
        """
        col_names = tuple(("news_number", "url", "headline", "ISO_Code"))
        col_types = tuple((int, str, str, int))
        super().__init__("public", "news", col_names, col_types)

    def add_many_inputs(self, data_names: tuple, data_input: tuple) -> dict:
        """
        Function that will take in data_names and data_inputs, and add the data_input (stored as a tuple of
        tuples which each have a corresponding value to their respective data_name

        :param data_names: tuple of names to be inputted
        :param data_input: tuple of data to be inputted
        :return: None
        """
        # Ensuring that function caller will be giving proper inputs=
        if "url" not in data_names or "headline" not in data_names:
            raise Exception(f'URL or Headline not in inputs')

        next_value = int(retrieve("SELECT last_value FROM public.news_news_number_seq;")[0][0])
        iso_index = data_names.index("ISO_Code")
        res = dict()
        for item in data_input:
            # Ensuring all items have proper length
            if len(item) != len(data_names):
                raise Exception(f"Your input tuple are not correct in {item}")

            if type(item[iso_index]) != int:
                item[iso_index] = int(item[iso_index])
            if item in res:
                res[item[iso_index]].append(next_value)
                next_value += 1
            else:
                res[item[iso_index]] = [next_value]
                next_value += 1
        super().add_many_inputs(data_names, data_input)
        return res
