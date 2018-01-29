# based on the work of Sebastian Raschka
# original header
# Sebastian Raschka 2014
# Prints Information of a SQLite database.

# E.g.,
#
"""
Total rows: 1

Column Info:
ID, Name, Type, NotNull, DefaultVal, PrimaryKey
(0, 'id', 'TEXT', 0, None, 1)
(1, 'date', '', 0, None, 0)
(2, 'time', '', 0, None, 0)
(3, 'date_time', '', 0, None, 0)

Number of entries per column:
date: 1
date_time: 1
id: 1
time: 1
"""

import records
from sqlalchemy import inspect

def connect(connection_stirng):
    """ Make connection to an SQLite database file """
    try:
        database = records.Database(connection_stirng)
    except Exception:
        print('Error while connecting to the database. Check your connection string')
        exit(127)
    return database


def close(database):
    """ Commit changes and close connection to the database """
    database.close()

def total_rows(database, table_name, print_out=False):
    """ Returns the total number of rows in the database table """
    count = database.query('SELECT COUNT(*) FROM {}'.format(table_name))
    if print_out:
        print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]

def database_tables(database):
    """ Returns a dict of table name """

    dbtables = database.get_table_names()
    tables = {}
    for table in dbtables:
        tables[table] = None

    return tables

def table_col_info(database, table_name, print_out=False):
    """
       Returns a list of tuples with column informations:
       (id, name, type, notnull, default_value, primary_key)
    """

    columns = inspect(database._engine).get_columns(table_name)
    info = []
    for c in columns:
        try:
            info.append((c['name'], str(c['type']), c['nullable'],
                         c['default'], c['primary_key']))
        except:
            info.append((c['name'], 'Null type', c['nullable'],
                         c['default'], c['primary_key']))

    if print_out:
        print("\n{}:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey".format(table_name))
        for col in info:
            print(col)

    return info

def get_component_from_info(column_info, component):
    """ Returns the named component from a PRAGMA TABLE_INFO
        sqlite3 query.
        where component must be one of:
        Name, Type, NotNull, DefaultVal, PrimaryKey
    """
    pragma_dict = {"Name": 0, "Type": 1, "NotNull": 2, "DefaultVal": 3, "PrimaryKey": 4}

    return column_info[pragma_dict[component]]
