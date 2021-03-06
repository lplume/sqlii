#!/usr/bin/env python3
"""
                     _|  _|  _|  
   _|_|_|    _|_|_|  _|          
 _|_|      _|    _|  _|  _|  _|  
     _|_|  _|    _|  _|  _|  _|  
 _|_|_|      _|_|_|  _|  _|  _|  
                 _|              
                 _| petergrimes

Match a regex against a sqlite3 database content

inspired by
* http://www.automatingosint.com/blog/2016/05/expanding-skype-forensics-with-osint-email-accounts/

Usage:
   {proc} [-h | --help]
   {proc} [-v] [-t] [-o <filename>] <database> <regex>

Options:
   -h, --help    Shows this help
   -v            Raise verbosity level
   -t            Show tables info
   -o <filename> Save to file prefixed filename (csv)

Arguments:
   <database>    sqlite3 database you wish to analyze
   <regex>       regex to match

"""
__version__ = "1.0.0"
__author__ = "petergrimes"

from docopt import docopt
import logging
from logging.config import dictConfig
from os.path import basename
import sys
import sqliteutil
import re
import csv

#: The dictionary, used by :class:`logging.config.dictConfig`
#: use it to setup your logging formatters, handlers, and loggers
#: For details, see https://docs.python.org/3.4/library/logging.config.html#configuration-dictionary-schema
DEFAULT_LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '[%(levelname)s] %(name)s: %(message)s'},
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        __name__: {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

#: Map verbosity level (int) to log level
LOGLEVELS = {None: logging.WARNING,  # 0
             0: logging.WARNING,
             1: logging.INFO,
             2: logging.DEBUG,
             }

#: Instantiate our logger
log = logging.getLogger(__name__)


def parsecli(cliargs=None):
    """Parse CLI arguments with docopt

    :param list cliargs: List of commandline arguments or None (=use sys.argv)
    :type clicargs: list | None
    :return: dictionary from docopt
    :rtype: dict
    """
    version = "%s %s" % (__name__, __version__)
    args = docopt(__doc__.format(proc=basename(sys.argv[0])),
                  argv=cliargs,
                  version=version)
    # Setup logging and the log level according to the "-v" option
    dictConfig(DEFAULT_LOGGING_DICT)
    log.setLevel(LOGLEVELS.get(args['-v'], logging.DEBUG))

    log.debug("CLI result: %s", args)
    return args

def match_regex_in_table(cursor, table_name, table_info, regex, print_out=True):
    """ Returns a dictionary with columns as keys and the
        match as associated values
    """
    match_list = []
    regex = re.compile(regex)

    cursor.execute("SELECT * FROM %s" % table_name)
    rows = cursor.fetchall()

    for row in rows:
        current_pk_value = None
        current_pk_name = False
        for idx, column in enumerate(row):
            pragma = table_info[idx]
            pk = sqliteutil.get_component_from_pragma(pragma, 'PrimaryKey')

            if pk == 1:
                current_pk_name = sqliteutil.get_component_from_pragma(pragma, 'Name')
                current_pk_value = row[idx]

            try:
                matches = regex.findall(column)
            except:
                continue

            for match in matches:                
                query = "SELECT * FROM %s WHERE %s = %s" % (table_name, current_pk_name, current_pk_value)
                match_list.append((cursor.description[idx][0], row[idx], query))

    return match_list

def toCSVFile(rowlist, filename, tableName, header):
    with open(filename,'a') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(header)
        for row in rowlist:
            currentrow = list(row)
            current = [tableName] + currentrow
            csv_out.writerow(current)

def toStdOut(rowlist, tableName, header):
    print(header)
    for row in rowlist:
        currentrow = list(row)
        current = [tableName] + currentrow
        print(",".join(map(str, current)))


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :type clicargs: list | None
    :return: error codes
    :rtype: int
    """
    try:
        args = parsecli(cliargs)
        conn, c = sqliteutil.connect(args['<database>'])
        tables = sqliteutil.database_tables(c)
        matches = {}
        for table in tables:
            tables[table] = sqliteutil.table_col_info(c, table)
            if args['-t'] and args['-o']:
                toCSVFile(tables[table], args['-o'] + '_tables.csv', table, ["TABLE", "ID", "Name", "Type", "NotNull", "DefaultVal", "PrimaryKey"])
            if args['-t']:
                toStdOut(tables[table], table, "TABLE, ID, Name, Type, NotNull, DefaultVal, PrimaryKey")

            current_match = match_regex_in_table(c, table, tables[table], args['<regex>'])

            if current_match:
                toStdOut(current_match, table, "TABLE, COLUMN, RAW MATCH, QUERY")
                if args['-o']:
                    toCSVFile(current_match, args['-o'] + '_matches.csv', table, ["TABLE", "COLUMN", "RAW" "MATCH", "QUERY"])
            matches[table] = current_match


        sqliteutil.close(conn)

        return 0
    
    # List possible exceptions here and turn exceptions into return codes
    except Exception as error:  # this should be a more specific exception
        log.exception(error)
        log.fatal(error)
        # Use whatever return code is appropriate for your specific exception
        return 10


if __name__ == "__main__":
    sys.exit(main())
