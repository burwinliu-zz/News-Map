"""
Subclass of database to represent the overview of the news database -- will help in sorting it out into countries

SEE data.py for use

("ISO_Code", "SMALLINT", "UNIQUE"),
("News_list", "BIGINT[]"),
("Colour", "SMALLINT")
ToDo remember to link between colour and num of articles
TODO decide on how colours are going to be assigned for this as well
"""
import webpage.data.python_scripts.database as database


class OverviewDatabase(database.Database):
    def __init__(self):
        col_names = tuple(("ISO_Code", "News_list", "Colour"))
        col_types = tuple((int, list, int))
        super().__init__("public", "news_overview", col_names, col_types)

    def add_input(self, iso_code, news_items):
        pass
