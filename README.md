# Simply Choose

SimplyChoose is yet another web based poll/agenda/planer.
It is written in Python2 using 
[Tornado](http://www.tornadoweb.org/en/stable/) framework
with the help of good old [Bootstrap](http://getbootstrap.com/).


## Use case scenario

If you're asking yourself why yet another I (we) had a use case
scenario like this: there was a need to allow students to choose
between a bunch of dates for their final exam. Since I had 
student info in ods/xlsx/csv files the easiest way for me would
just be to copy these csv files to an app and simply run it.
Voilà, using students can log in (info in a csv) and choose
a date (info in another csv).

## Requirements

- MySQL-python>=1.2.5
- tornado>=4.0.2
- torndb>=0.3

## Install/Run

A database in MySQL is need together with a *username* and a *pass*.
If you don't have it already you can create it as follows:
```
mysql> create database db_name;
mysql> grant all on db_name.* to 'username'@'db_host' identified by 'pass'
```
where *db_host* is the name of the machine running MySQL server (usually
*localhost*).

Appropriate database structure can be achieved now as follows:
```bash
$ mysql -uusername -p < db_schema/db_table.txt
```

Copy csv files to data directory. One for username/pass combination
and one for questions/dates/... Take a look at `data/datumi.csv`
and `data/k1.csv` for an example.

Final step is to properly adjust variables in *vars.ini* file and
run the application with
```bash
$ python app.py
```

### Running through VirtualENV

The app can also be run through a tool to create isolated Python
environment called [virtualenv](https://virtualenv.pypa.io/en/latest/).
This can be achieved as follows:

```bash
# create virtaulenv dir and activate it
$ virtualenv simplychoose_venv
$ cd simplychoose_venv && source bin/activate

# git pull/copy/... app to the appropriate directory
$ git clone https://github.com/iugrina/simplychoose.git
$ cd simplychoose

# install dependencies
$ pip install -r requirements.txt
```

You can now adjust everything like in the previous section
and run the application.

## Imporant

Don't forget to open the port for the application in your firewall.
