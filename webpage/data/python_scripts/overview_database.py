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
        col_names = tuple(("ISO_Code", "News_list"))
        col_types = tuple((int, list, int))
        super().__init__("public", "news_overview", col_names, col_types)

    def add_input(self, data_name: tuple, data_input: tuple):
        try:
            assert "ISO_Code" in data_name
            assert "News_list" in data_name
        except AssertionError:
            print("Passed invalid inputs -- no ISO_Code or news_list found")
            raise ValueError
        super().add_input(data_name, data_input)


if __name__ == "__main__":
    # testing purposes
    odb = OverviewDatabase()
    x = sql_manage.get_data(f"SELECT ISO_Code FROM public.news_overview")
    y = sql_manage.get_data(f"SELECT news_list FROM public.news_overview")
    print(x, y)
    for i in x:
        print(i)
        print(type(i))
    odb.add_input(tuple(("ISO_Code", "News_list")), tuple((4, [3, 4, 2])))
