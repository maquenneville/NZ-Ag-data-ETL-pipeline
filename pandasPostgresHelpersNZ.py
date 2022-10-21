# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 02:11:39 2022

@author: marca
"""

import pandas as pd
import os
import shutil
import time
import psycopg2
from config import config


def move_csv_to_public(path):
    """


    Parameters
    ----------
    path : string, path of csv

    Returns
    -------
    None, moves csv file to Public for easy loading into Postgres

    """

    file = os.path.basename(path)

    shutil.copy(path, r"C:\Users\Public" + f"\{file}")

    time.sleep(2)

    print(f"{file} copied to public, ready to load")


def delete_csv_from_public(file):
    """


    Parameters
    ----------
    desPath : string, desired destination path for csv from Public

    Returns
    -------
    None, deletes csv files from Public

    """

    os.unlink(r"C:\Users\Public" + f"\{file}")

    time.sleep(2)

    print(f"{file} deleted from public")


def make_create_statement(tableName, dframe):
    """


    Parameters
    ----------
    tableName : string, name of desired table in Postgres
    dframe : Dataframe, the target pandas Dataframe

    Returns
    -------
    a SQL CREATE TABLE statement with the appropriate column names and data types.
    Note: you will need to designate PRIMARY KEYS and REFERENCE columns manually

    """

    colnames = list(dframe.columns)
    datatypes = list(dframe.dtypes)
    datatypes = [str(i) for i in datatypes]

    coldata = dict(zip(colnames, datatypes))

    sql = f"""
CREATE TABLE {tableName} (
                """

    for col, typ in coldata.items():
        snippet = ""
        snippet += col + " "
        if typ == "int64":
            snippet += "INTEGER,\n"
        elif typ == "object":
            snippet += "VARCHAR(200),\n"
        elif typ == "float64":
            snippet += "REAL,\n"

        sql += snippet
    sql = sql[:-2]
    sql += "\n);"

    return sql


def make_load_statement(tableName, dframe, fileName, folder):
    """


    Parameters
    ----------
    tableName : string, name of table being populated
    dframe : Dataframe, pandas Dataframe that was exported into the csv
    fileName : string, file name (plus .csv)
    folder: Main path to folder with CSVs, include r at beginning of string

    Returns
    -------
    a SQL COPY statement to load data from a csv file into a Postgres table

    """
    sql = f"COPY {tableName}("
    columns = list(dframe.columns)
    path = r"C:\Users\Public" + f"\{fileName}"
    for n, i in enumerate(columns):
        if n == len(columns) - 1:
            sql += i + ")\n"
        else:
            sql += i + ","
    sql += f"FROM '{path}'\n"
    sql += """DELIMITER ','
CSV HEADER;
"""
    return sql


def delete_test_tables():
    """


    Deletes AG NZ tables from the Postgres database

    """

    tables = [
        "graze_farm",
        "graze_region",
        "livestock_farm",
        "livestock_region",
        "livestock_total",
        "territorial",
    ]

    conn = None

    try:

        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        for t in tables:
            print(f"Deleting {t}")
            sql = f"DROP TABLE {t};"
            # execute the sql statements
            cur.execute(sql)

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        print("Test tables deleted")
