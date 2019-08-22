"""
Subclass of database to represent the overview of the news database -- will help in sorting it out into countries

SEE data.py for use

("ISO_Code", "SMALLINT", "UNIQUE"),
("News_list", "BIGINT[]"),
("Colour", "SMALLINT")
"""
from .database import Database
from .sql_manage import execute_command, get_data
import webpage.server.data.python_scripts.database as database
import webpage.server.data.python_scripts.sql_manage as sql_manage
from typing import Tuple


class OverviewDatabase(Database):
    def __init__(self):
        """
        Init the database
        """
        col_names = tuple(("ISO_Code", "News_list"))
        col_types = tuple((int, list))
        super().__init__("public", "news_overview", col_names, col_types)

    def add_input(self, data_name: tuple, data_input: tuple):
        """
        add single input row to database

        :param data_name: tuple of names to be inputted
        :param data_input: data to be inputted
        :return: None
        """
        # test this command
        if "ISO_Code" not in data_name or "News_list" not in data_name:
            raise ValueError("Passed invalid inputs -- no ISO_Code or news_list found")
        data = get_data(self.schema, self.name, tuple("iso_code"))
        if data_input in data:
            self._update_input(data_input)
        else:
            super().add_input(data_name, data_input)

    def add_many_inputs(self, data_names: tuple, data_input: Tuple) -> None:
        """
        Add inputs to overview

        :param data_names: tuple of names to be inputted
        :param data_input: tuple of data to be inputted
        :return: none
        """
        if "ISO_Code" not in data_names or "News_list" not in data_names:
            raise ValueError("Passed invalid inputs -- no ISO_Code or news_list found")
        to_add, to_update = self._parse_commands(data_input, data_names.index("ISO_Code"))
        self._update_input(tuple(to_update))
        super().add_many_inputs(data_names, tuple(to_add))

    def _parse_commands(self, data_input: tuple, pos_iso: int) -> (list, list):
        """
        Parse the commands to see what is to be updated and what is to be added

        :param data_input: tuple of all input-ed data
        :param pos_iso: position of the iso_code (the key for this database)
        :return: (list, list) of lists to add, lists to update
        """
        to_return_data = list()
        to_unique_update = list()
        data = get_data(self.schema, self.name, tuple(("ISO_Code",)))
        data = [int(item[0]) for item in data]
        for item in data_input:
            if item[pos_iso] in data:
                to_unique_update.append(item)
            else:
                to_return_data.append(item)
        return to_return_data, to_unique_update

    def _update_input(self, data_update: tuple) -> None:
        # Todo TEST THIS FUNCTION AND MIX AND MATCH
        """
        WARNING might not play nice.
        Helper function meant to update inputs into overview database

        :param data_update: tuple to update inputs
        :return:None
        """
        if len(data_update) == 0:
            return
        values = ', '.join(f"({k[0]}, ARRAY{list(k[1])}::BIGINT[])" for k in data_update)
        execute_command(f"UPDATE {self.schema}.{self.name} AS t SET "
                                   f"iso_code = c.iso_code, "
                                   f"news_list= t.news_list||c.news_list "
                                   f"FROM(VALUES {values}) AS c(iso_code, news_list) "
                                   f"WHERE c.iso_code = t.iso_code;")


# if __name__ == "__main__":
    # testing purposes
    '''
    odb = OverviewDatabase()
    x = sql_manage.retrieve(f"SELECT ISO_Code FROM public.news_overview")
    y = sql_manage.retrieve(f"SELECT news_list FROM public.news_overview")
    print(x, y)
    for i in x:
        print(i)
        print(type(i))
    odb.add_input(tuple(("ISO_Code", "News_list")), tuple((4, [3, 4, 2])))
    '''
