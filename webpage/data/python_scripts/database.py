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
        :param data_input: tuple[tuple[obj, ...], ...]
        :return: None
        """
        # Catching Exceptions
        if len(data_names) > self.numColumns:
            raise Exception(f"Invalid inputs {data_names}, {data_input}")
        if len(data_input) == 0:
            return
        to_execute = list()
        name_types = list()
        for i in data_names:
            try:
                name_types.append(self.types[self.columns.index(i)])
            except ValueError:
                raise ValueError("Name not in list of database")
        for i in range(len(data_input)):
            current_data_list = data_input[i]
            for j in range(len(current_data_list)):
                if type(current_data_list[j]) == list:
                    continue
                if type(current_data_list[j]) != name_types[j]:
                    name_types[j](current_data_list[j])
            to_execute.append(tuple(data_input[i]))
        data_to_add = ','.join(str(ls) for ls in to_execute)
        data_to_add = re.sub(r'"', "'", data_to_add)
        data_to_add = re.sub(r'\[', "ARRAY[", data_to_add)
        sql_manage.execute_command(f"INSERT INTO {self.schema}.{self.name}({', '.join(data_names)})"
                                   f"VALUES {data_to_add};")

    def add_input(self, data_name: tuple, data_input: tuple):
        """
        Add one line of input to the database, providing all inputs are consistent with the database
        :param data_name: tuple[str]
        :param data_input: tuple[type]
        :return: None
        """
        if len(data_name) > self.numColumns:
            raise Exception(f"Invalid Inputs {data_input}, {data_name}")
        for i in data_name:
            if i not in self.columns:
                raise Exception(f'Invalid input {i}')
        data_to_add = ','.join(str(x) for x in data_input)
        data_to_add = re.sub(r'"', "'", data_to_add)
        data_to_add = re.sub(r'\[', "'{", data_to_add)
        data_to_add = re.sub(r'\]', "}'", data_to_add)
        sql_manage.execute_command(f"INSERT INTO {self.schema}.{self.name}({', '.join(data_name)}) VALUES"
                                   f"({data_to_add});")

    def _check_sys_records(self):
        pass
