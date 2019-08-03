"""
    Need to configure username and password according to your own specs in an env file

    Should have files to configure the databases to hold countries
"""
import psycopg2
from webpage.settings import settings
from os import getenv


# used to test that postgres is in fact working and connected
# TODO Convert host to more permanent state to connect to
# TODO setup data file to save and store on db, and record colours, values for county map and country names
def test() -> int:
    """
    Testing that connection can be established

    :return: int
    """
    try:
        connection = psycopg2.connect(user="postgres",
                                      password=getenv('DATABASE_PW'),
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")
        settings.test()
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
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# noinspection PyUnresolvedReferences
def init_db(name: str, column_data: list[tuple[str, ...]], table_rules: list[str, ...] = list, inherit: str = None) \
        -> None:
    """
    Takes params from user and inits postgreSQL database according to inputs
    Note -- column data can have a max of three parameters, see annotations for others

    :rtype: None
    :param name: str
    :param column_data: list[tuple] if len(tuple) <= 3 (list[tuple(len<3)])
    :param table_rules: list[str
    :param inherit: str
    :return: None
    """
    if table_rules is None:
        table_rules = []
    if table_rules is None:
        table_rules = list()
    try:
        connection = psycopg2.connect(user="postgres",
                                      password=getenv('DATABASE_PW'),
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()
        column_compiled = str()

        for i in column_data:
            if 0 < len(i) < 4:
                column_compiled += f"{' '.join([j for j in i])}, "
            else:
                raise TypeError

        to_execute = f"CREATE TABLE {name} ({column_compiled}{' '.join(table_rules)})"
        if inherit is not None:
            to_execute += f"INHERIT {inherit}"
        cursor.execute(to_execute)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL in initDb", error)

    except OSError:
        print("settings imported incorrectly")

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def store_data():
    pass


class DatabaseError(Exception):
    pass

if __name__ == '__main__':
    test()
