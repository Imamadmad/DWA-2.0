import psycopg2 as sql
import psycopg2.extras as extras

import configparser
import os
import sys
import traceback

## Get db information from config file
## Config file is in parent directory
Config = configparser.ConfigParser()
Config.read('config.txt' )

## Replace with call to config file so password isn't stored in this file
conn_string = "host='{host}' dbname='{dbname}' user='{user}' password='{password}'".format(
        host    = Config.get("DatabaseConnection", "host"),
        dbname  = Config.get("DatabaseConnection", "dbname"),
        user    = Config.get("DatabaseConnection", "user"),
        password= Config.get("DatabaseConnection", "password")
    )


######################
##### Decorators #####
######################

''' A decorator which handles the openning and closing of
    database connections, so each function doesn't have to
    do so itself.
    Each wrapped function needs its first parameter to be
    c (cursor) when declared, but this parameter is not then
    used when calling he function.
'''
def connect(some_function) :
    def wrapper(*args, **kwargs) :
        conn = sql.connect(conn_string)
        c = conn.cursor(cursor_factory=extras.DictCursor)

        try :
            result = some_function(c, *args, **kwargs)
            conn.commit()
        except :
            # traceback.print_exc()
            sys.stderr.write('Rolling back {}\n'.format(some_function.__name__))
            conn.rollback()
            raise
        finally :
            # sys.stderr.write('Closing connection\n')
            conn.close()

        return result
    return wrapper


## To query the DB from the prompt while testing
## NOT TO BE USED IN THE ACTUAL APP
@connect
def test_db(c, stmnt) :
    c.execute(stmnt)

    if "select" in stmnt.lower() :
        result = c.fetchall()

        if len(result) < 1 :
            print("No result")
            return

        # print(result)
        print([col.name for col in c.description])

        for row in result :
            print(row)

        # return result