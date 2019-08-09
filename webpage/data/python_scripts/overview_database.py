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
import webpage.data.python_scripts.sql_manage as sql_manage


class OverviewDatabase(database.Database):
    def __init__(self):
        col_names = tuple(("ISO_Code", "News_list", "colour"))
        col_types = tuple((int, list, int))
        super().__init__("public", "news_overview", col_names, col_types)
        self.max_items = 0
        self.num_articles = dict()
        self._sync_db_to_obj()

    def add_input(self, data_name: tuple, data_input: tuple):
        try:
            index_iso = data_name.index("ISO_Code")
            data_name.index("News_list")
            data_name.index("colour")
        except ValueError:
            print("Passed invalid inputs -- no ISO_Code or news_list found")
            raise ValueError
        self._update_self(data_name[index_iso])
        super().add_input(data_name, data_input)

    def _update_self(self, iso_code: int):
        pass

    def _sync_db_to_obj(self):
        x = sql_manage.get_data(f"SELECT ISO_Code FROM public.news_overview")
        for i in x:
            if i not in self.num_articles:
                continue

    def _convert_num_to_colour(self):
        pass


'''
testing purposes
if __name__ == "__main__":
    odb = OverviewDatabase()
    odb.add_input(tuple(("ISO_Code", "News_list", "colour")), tuple((23, [3, 4, 2], 1)))
'''
