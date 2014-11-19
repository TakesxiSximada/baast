baast

baast

install
===========

Next, execute command.::

    $ pip install baast


How to use
===========



initialize database::

    mysql> CREATE DATABASE `baast` DEFAULT CHARSET utf8;
    Query OK, 1 row affected (0.00 sec)

    mysql> use baast;
    Database changed
    mysql> GRANT ALL ON `baast.*` TO `baast@`@'127.0.0.1' IDENTIFIED BY 'baast';
    Query OK, 0 rows affected (0.04 sec)

    mysql>

create tables::

    $ alembic upgrade head
