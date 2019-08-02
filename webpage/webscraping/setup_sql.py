"""
    Need to configure username and password according to your own specs in an env file

    Should have files to configure the databases to hold countries
"""
import psycopg2
import webpage.settings as settings
from os import getenv
from iso3166 import countries


# used to test that postgres is in fact working and connected
def test():
    """
    Testing that connection can be established

    :return: None
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
    except OSError:
        print("settings imported incorrectly")
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def print_countries() -> None:
    """
    print out countries  from iso3166, from pylib. Will use this list to generate a database containing all coutnries databases

    :return: None
    """
    print(type(countries))
    for key in countries:
        print(key)
        print(key.name, key.alpha2)


if __name__ == '__main__':
    print_countries()
