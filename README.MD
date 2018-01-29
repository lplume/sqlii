# sqlii 

Match a regex against a SQL database content.

This script is inspired by
* http://www.automatingosint.com/blog/2016/05/expanding-skype-forensics-with-osint-email-accounts/

## How to Install

Simply clone `sqlii`:

    git clone https://github.com/lplume/sqlii.git

## Usage

From the `-h` help menu:

	Usage:
	   sqlii.py [-h | --help]
	   sqlii.py [-v] [-t] [-o <filename>] <database> <regex>

	Options:
	   -h, --help    Shows this help
	   -v            Raise verbosity level
	   -t            Show tables info
	   -o <filename> Save to file prefixed filename (csv)

	Arguments:
	   <database>    sqlite3 database you wish to analyze
	   <regex>       regex to match

## License

`sqlii` is released under the GPL 3.0 license and it's copyleft of Mauro Pizzamiglio