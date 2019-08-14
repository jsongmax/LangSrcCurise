#!/usr/bin/env python
import os
import sys
import pymysql
import contextlib
import configparser

cfg = configparser.ConfigParser()
cfg.read('Config.ini')

host = cfg.get("Server", "host")
username = cfg.get("Server", "username")
password = cfg.get("Server", "password")
Dbname = cfg.get("Server","dbname").lower()
port = int(cfg.get("Server","port"))


@contextlib.contextmanager
def co_mysql(db='mysql'):
    conn = pymysql.connect(host=host,user=username,password=password,port=port,db=db,charset='utf8')
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

with co_mysql(db='mysql') as cursor:
   row_count = cursor.execute("show databases;")
   a = cursor.fetchall()
   b = [y for x in a for y in x]
   if Dbname.lower() in b:
       pass
   else:
       cursor.execute('create database {}'.format(Dbname))

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LangSrcCurise.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

