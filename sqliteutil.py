# based on the work of Sebastian Raschka
# 
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

import sqlite3
import os.path

def connect(sqlite_file):
    """ Make connection to an SQLite database file """
    if os.path.isfile(sqlite_file):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        return conn, c
    else:
        raise FileNotFoundError("{} not found".format(sqlite_file))

def close(conn):
    """ Commit changes and close connection to the database """
    conn.close()

def total_rows(cursor, table_name, print_out=False):
    """ Returns the total number of rows in the database """
    cursor.execute('SELECT COUNT(*) FROM {}'.format(table_name))
    count = cursor.fetchall()
    if print_out:
        print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]

def database_tables(cursor):
    """ Returns a dict of table name """
    cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\'');
    tables = {};
    for table in cursor.fetchall():
        tables[table[0]] = None

    return tables

def table_col_info(cursor, table_name, print_out=False):
    """ 
       Returns a list of tuples with column informations:
       (id, name, type, notnull, default_value, primary_key)
    
    """
    cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = cursor.fetchall()
    
    if print_out:
        print("\n{}:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey".format(table_name))
        for col in info:
            print(col)
    return info

def get_component_from_pragma(pragma, component):
    """ Returns the named component from a PRAGMA TABLE_INFO
        sqlite3 query.
        where component must be one of:
        ID, Name, Type, NotNull, DefaultVal, PrimaryKey
    """
    pragma_dict = {
        "ID": 0,
        "Name": 1,
        "Type": 2,
        "NotNull": 3,
        "DefaultVal": 4,
        "PrimaryKey": 5
    }

    return pragma[pragma_dict[component]]

def values_in_col(cursor, table_name, print_out=False):
    """ Returns a dictionary with columns as keys and the number of not-null 
        entries as associated values.
    """
    cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = cursor.fetchall()
    col_dict = dict()
    for col in info:
        col_dict[col[1]] = 0
    for col in col_dict:
        cursor.execute('SELECT ({0}) FROM {1} WHERE {0} IS NOT NULL'.format(col, table_name))
        # In my case this approach resulted in a better performance than using COUNT
        number_rows = len(cursor.fetchall())
        col_dict[col] = number_rows
    if print_out:
        print("\nNumber of entries per column:")
        for i in col_dict.items():
            print('{}: {}'.format(i[0], i[1]))
    return col_dict
