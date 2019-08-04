"""
    Database representation object
"""
import psycopg2
from os import getenv
import webpage.data.python_scripts.sql_manage as sql_manage


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

    def add_many_inputs(self, data_names: tuple, data_input: tuple[tuple, ...]) -> None:
        """
        Add many inputs to the database, providing all inputs are consistent with the database
        NOTE: Will finish up to the point of failure, and add all prior datapoints into the database
        TODO test this function

        :param data_names: tuple
        :param data_input: tuple[tuple, ...]
        :return: None
        """
        try:
            if data_names == self.columns and len(data_names) == self.numColumns:
                connection = sql_manage.setup_connection()
                cursor = connection.cursor()
                for i in data_input:
                    for j in range(len(i)):
                        if type(data_input[j]) != self.types[j]:
                            raise TypeError
                    # Check this 12 pm code Maybe move to sql_manage And figure out how to insert multi items
                cursor.execute(f"INSERT INTO {self.name}({', '.join(data_names)})"
                               f"")
            else:
                raise Database.InvalidInput
        finally:
            if connection:
                cursor.close()
                connection.close()

    class InvalidInput:
        pass
