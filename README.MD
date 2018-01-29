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
	{proc} [-h | --help]
	{proc} [-v] [-t] [-o <format>] <database> <regex>

	Options:
	-h, --help    Shows this help
	-v            Raise verbosity level
	-t            Show tables info
	-o format     Save to export.format (csv, yaml, txt, json)

	Arguments:
	<database>    database dns
	<regex>       regex to match

## License

`sqlii` is released under the GPL 3.0 license and it's copyleft of Mauro Pizzamiglio