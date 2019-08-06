"""
    Database representation object
"""
import webpage.data.python_scripts.sql_manage as sql_manage
import re


class Database:
    def __init__(self, name: str, column_names: tuple, column_types: tuple):
        """
        Init a database object representation

        :param name: str
        :param column_names: tuple
        :param column_types: tuple
        """
        self.name = name
        self.types = column_types
        self.columns = column_names
        self.numColumns = len(column_types)

    def add_many_inputs(self, data_names: tuple, data_input: tuple) -> None:
        """
        Add many inputs to the database, providing all inputs are consistent with the database
        NOTE: Will finish up to the point of failure, and add all prior datapoints into the database
        TODO test this function

        :param data_names: tuple
        :param data_input: tuple[tuple, ...]
        :return: None
        """
        try:
            if len(data_names) <= self.numColumns:
                connection = sql_manage.setup_connection()
                cursor = connection.cursor()
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
                cursor.execute(f"INSERT INTO {self.name}({', '.join(data_names)})"
                               f"SELECT * FROM  unnest({data_to_add});")
                connection.commit()
            else:
                raise self.InvalidInput
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()

    class InvalidInput:
        pass
