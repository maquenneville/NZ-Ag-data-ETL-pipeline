# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:53:07 2022

@author: marca
"""

import psycopg2
from config import config
from pandasPostgresHelpersNZ import (
    make_create_statement,
    make_load_statement,
    move_csv_to_public,
    delete_csv_from_public,
)
from ETLprojectTransform import transform_data
import os, csv
import pandas as pd
from ETLprojectExtract import delete_old_test_files


def load_data(df_final, path):
    """


    Parameters
    ----------
    df_final : dictionary, a dictionary of cleaned DataFrames, originated from the AG NZ data zipfile
    path: string, path (with r in the beginning) pointing to project folder

    Function converts the DataFrames to CSVs, creates SQL statements to create each table
    and populate it with the CSV file associated with it, copies the CSVs to public (in order for Postgres
    to have access), loads each CSV into the database using the generated SQL statements, then deletes
    the copied CSVs from Public (for housekeeping)

    """

    os.chdir(path)
    #
    home_folder = path

    # Convert to CSVs
    print("Converting DataFrames back to CSVs")

    for df in df_final:
        df_final[df].to_csv(home_folder + f"\{df}.csv", index=False)
        move_csv_to_public(home_folder + f"\{df}.csv")

    # Create dicts of SQL statements
    create_dict = {}
    load_dict = {}

    for df in df_final:
        create_dict[df] = make_create_statement(df, df_final[df])
        load_dict[df] = make_load_statement(df, df_final[df], f"{df}.csv", home_folder)

    # Load CSVs into database
    print("Loading CSVs into Postgres database")
    conn = None

    try:

        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        for df in df_final:
            print(f"Loading {df}")
            sqlcreate = create_dict[df]
            sqlload = load_dict[df]
            # execute the sql statements
            cur.execute(sqlcreate)
            cur.execute(sqlload)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    for df in df_final:
        delete_csv_from_public(f"\{df}.csv")

    print("------------------")
    print("All tables loaded!")
