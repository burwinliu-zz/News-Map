"""
    Need to configure username and password according to your own specs in an env file

    Should have files to configure the databases to hold countries
"""
import psycopg2
from webpage.settings import setup
from os import getenv
import decimal
from webpage.settings.setup import setup_globals
import re

setup_globals()


# used to test that postgres is in fact working and connected
def test() -> int:
    """
    Testing that connection can be established

    :return: int
    """
    try:
        connection = setup_connection()
        setup.test()
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return 1
    except OSError:
        print("settings imported incorrectly")
        return 1
    finally:
        # closing database connection.
        if 'connection' in locals():
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# noinspection PyUnresolvedReferences
def init_db(schema: str, name: str, column_data, table_rules=None, inherit=None) \
        -> tuple:
    """
    Takes params from user and inits postgreSQL database according to inputs
    Note -- column data can have a max of three parameters, see annotations for others

    :param schema: str
    :type table_rules: list()
    :rtype: None
    :param name: str
    :param column_data: list[tuple] if len(tuple) <= 3 (list[tuple(len<3)])
    :param table_rules: list[str
    :param inherit: str
    :return: db.Database
    """
    if table_rules is None:
        table_rules = []
    if table_rules is None:
        table_rules = list()
    try:
        connection = setup_connection()
        cursor = connection.cursor()

        column_compiled = str()
        names = list()
        types = list()
        for i in column_data:
            if 0 < len(i) < 4:
                names.append(i[0])
                types.append(i[1])
                column_compiled += f"{' '.join([j for j in i])}, "
            else:
                raise TypeError
        # NOTE PEOPLE DO NOT FORGET SEMI COLONS
        to_execute = f"CREATE TABLE {schema}.{name} ({column_compiled[:-2]}{' '.join(table_rules)});"
        if inherit is not None:
            to_execute += f"INHERIT {inherit}"
        if check_table_exists(name, schema):
            return tuple((schema, name, tuple(names), tuple(_process_types(types))))
        cursor.execute(to_execute)
        connection.commit()
        res = tuple((schema, name, tuple(names), tuple(_process_types(types))))
    except OSError:
        print("settings imported incorrectly", OSError)

    finally:
        # closing database connection.
        if 'connection' in locals():
            cursor.close()
            connection.close()
        if 'res' in locals():
            _add_to_system_records(*res)
            return res


def setup_connection():
    """
    Setup connection to sql server

    :return: psycopg2._connect
    """
    try:
        return psycopg2.connect(user=getenv('DATABASE_USER_SQL'),
                                password=getenv('DATABASE_PW_SQL'),
                                host=getenv('HOST_IP_ADDR_SQL'),
                                port=getenv('HOST_PORT_SQL'),
                                database=getenv('DATABASE_TYPE_SQL'))
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def retrieve(command: str) -> list:
    try:
        connection = setup_connection()
        cursor = connection.cursor()
        cursor.execute(command)
        res = cursor.fetchall()
    finally:
        # closing database connection.
        if 'connection' in locals():
            cursor.close()
            connection.close()
        if 'res' in locals():
            return res


def execute_command(command: str) -> None:
    """
    Execute a postgres cmd

    :param command: str -- the command
    :return: none
    """
    try:
        connection = setup_connection()
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()


def check_table_exists(name: str, schema: str) -> bool:
    """
    Checks if a table with given name and schema is in the sys_info table
    :param name: str -- name of table to search
    :param schema -- parameter the item is under
    :return: bool
    """
    to_execute = f"SELECT schema, name FROM system.sys_info"
    to_check = retrieve(to_execute)
    return tuple((name, schema)) in to_check


def get_data(schema: str, name: str, columns: tuple):
    return retrieve(f"SELECT {', '.join(columns)} FROM {schema}.{name}")


def exists_in_table(schema: str, name: str, column: str, table: str) -> bool:
    """
    Check if name is in schema.table's column

    :param schema: schema of the table
    :param name: name of the item searching for
    :param column: column name
    :param table: table name
    :return: bool
    """
    to_check = retrieve(f"SELECT {column} FROM {schema}.{table}")
    return name in to_check


def _process_types(rules: list) -> list:
    """
    Convert the types (in SQL str format) to their corresponding python types.

    :param rules: list
    :return: tuple
    """
    res = list()
    convert_dict = {"boolean": bool,
                    "smallint": int,
                    "SMALLINT": int,
                    "int": int,
                    "serial": int,
                    "bigint": int,
                    "oid": int,
                    "real": float,
                    "double": float,
                    "numeric": decimal.Decimal,
                    "bytea": bytes,
                    }
    for i in rules:
        if i.endswith("[]"):
            res.append(list)
            continue
        try:
            res.append(convert_dict[i])
        except KeyError:
            res.append(str)
    return res


def _types_to_str(types: tuple) -> tuple:
    """
    convert types tuple to list tuple (with basic types, to expand if needed)
    may be missing a few conversions

    :param types: tuple[types, ...]
    :return: tuple[str, ...]
    """
    converter = {
        str: "str",
        int: "int",
        float: "float",
        bool: "bool",
        list: "list",
    }
    res = list()
    for i in types:
        res.append(converter[i])
    return tuple(res)


def _add_to_system_records(schema: str, name: str, columns: tuple, types: tuple):
    """
    Add item to the sys_info database for records

    :param schema:str
    :param name:str
    :param columns:tuple of str
    :param types:tuple of types
    :return:
    """
    try:
        connection = setup_connection()
        cursor = connection.cursor()
        columns = re.sub(r"'", "", str(columns))
        types = re.sub(r"'", "", str(_types_to_str(types)))
        to_add = f"'{schema}', '{name}', '{columns}', '{types}'"
        cursor.execute(f'INSERT INTO system.sys_info (schema, name, columns, types) VALUES ({to_add})')
        connection.commit()
    finally:
        # closing database connection.
        if 'connection' in locals():
            cursor.close()
            connection.close()


class DatabaseError(Exception):
    """
    Error class
    """
    pass

