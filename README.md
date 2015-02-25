# Simply Choose

SimplyChoose is yet another web based poll/agenda/planer.
It is written in Python using 
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

