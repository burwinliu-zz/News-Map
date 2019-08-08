"""
Subclass of database to represent the news database -- major changes in the adding of items

SEE data.py for use

("news_number", "SERIAL", "PRIMARY KEY"),
("url", "TEXT"),
("ISO_Code", "SMALLINT")
"""
import webpage.data.python_scripts.database as database


class NewsDatabase(database.Database):
    def __init__(self):
        col_names = tuple(("news_number", "url", "ISO_Code"))
        col_types = tuple(("int", "str", "int"))
        super().__init__("public", "news", col_names, col_types)

    def add_many_inputs(self, urls: tuple, iso_codes: tuple) -> dict:
        """
        Each url matches corresponding iso code -- must have same length of both
        :param urls: tuple
        :param iso_codes: tuple
        :return: dict of ints of all the newly added inputs to their corresponding iso codes (iso codes as the key)
        """
        if len(urls) != len(iso_codes):
            raise Exception("Lengths were incorrect and not matching")
        res = dict()
        return res
