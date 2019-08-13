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
from typing import Tuple


class OverviewDatabase(database.Database):
    def __init__(self):
        col_names = tuple(("ISO_Code", "News_list"))
        col_types = tuple((int, list, int))
        super().__init__("public", "news_overview", col_names, col_types)

    def add_input(self, data_name: tuple, data_input: tuple):
        # Todo involve parse commands.
        if "ISO_Code" not in data_name or "News_list" not in data_name:
            raise ValueError("Passed invalid inputs -- no ISO_Code or news_list found")

        super().add_input(data_name, data_input)

    def add_many_inputs(self, data_names: tuple, data_input: Tuple[Tuple]) -> None:
        if "ISO_Code" not in data_names or "News_list" not in data_names:
            raise ValueError("Passed invalid inputs -- no ISO_Code or news_list found")
        super().add_many_inputs(data_names, data_input)

    def _parse_commands(self, data_input):
        # Todo parse commands that exist and that do not exist in the news_overview database
        to_return_name = list()
        to_return_data = list()
        to_unique_update = dict()
        '''
        for i in range(len(data_input)):
            try:
                if self.rules[data_name[i]] == 1:
                    to_unique_update[data_name[i]] = data_input[i]
            except KeyError:
                to_return_name.append(data_name[i])
                to_return_data.append(data_input[i])
        self._unique_update(to_unique_update)
        '''
        return to_return_name, to_return_data

    def _update_input(self):
        # Todo, update tuples if the value already exists
        pass


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
