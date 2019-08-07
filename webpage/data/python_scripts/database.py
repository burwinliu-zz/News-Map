"""
    Database representation object
"""
import webpage.data.python_scripts.sql_manage as sql_manage
import re


class Database:
    def __init__(self, schema: str, name: str, column_names: tuple, column_types: tuple):
        """
        Init a database object representation

        :param name: str
        :param column_names: tuple
        :param column_types: tuple
        """
        self.schema = schema
        self.name = name
        self.types = column_types
        self.columns = column_names
        self.numColumns = len(column_types)
        self._check_sys_records()

    def add_many_inputs(self, data_names: tuple, data_input: tuple) -> None:
        """
        Add many inputs to the database, providing all inputs are consistent with the database

        :param data_names: tuple[str]
        :param data_input: tuple[tuple[type, ...], ...]
        :return: None
        """
        if len(data_names) <= self.numColumns:
            to_execute = list()
            for i in data_names:
                if i not in self.columns:
                    raise self.InvalidInput
                to_execute.append(list())
            for i in data_input:
                for j in range(len(i)):
                    if type(i[j]) != self.types[j]:
                        type(i[j])(self.types[j])
                    to_execute[j].append(self.types[j](i[j]))
            data_to_add = ','.join((' ARRAY' + str(ls)) for ls in to_execute)
            data_to_add = re.sub(r'"', "'", data_to_add)
            sql_manage.execute_command(f"INSERT INTO {self.schema}.{self.name}({', '.join(data_names)})"
                                       f"SELECT * FROM  unnest({data_to_add});")
        else:
            raise self.InvalidInput

    def add_input(self, data_name: tuple, data_input: tuple):
        """
        Add one line of input to the database, providing all inputs are consistent with the database

        :param data_name: tuple[str]
        :param data_input: tuple[type]
        :return: None
        """
        if len(data_name) <= self.numColumns:
            for i in data_name:
                if i not in self.columns:
                    raise self.InvalidInput
            data_to_add = ','.join(str(x) for x in data_input)
            data_to_add = re.sub(r'"', "'", data_to_add)
            sql_manage.execute_command(f"INSERT INTO {self.schema}.{self.name}({', '.join(data_name)})"
                                       f"({data_to_add});")
        else:
            raise self.InvalidInput

    def _check_sys_records(self):
        pass

    class InvalidInput:
        pass
