# NZ-Ag-data-ETL-pipeline

Built for Windows

This project extracts Ag data from the stats.govt.nz site (https://www.stats.govt.nz/assets/Uploads/Agricultural-production-statistics/Agricultural-Production-Statistics-key-tables-from-APS-2002-2017.zip), cleans the livestock totals Excel files and loads them into a PostgreSQL database.

This pipeline uses openpyxl to clean up the parser-hostile source Excel files, which only works on .xlsx files, therefore the old .xls files had to be updated using win32com.  The tables then had to be individually cleaned, as they each had different formatting styles, and accounting for all styles functionally would have been unnecessarily complex.  From there, the tables (as DataFrames) were converted back to CSV files,  the files were copied to public (to get around permissions requirements), CREATE and COPY SQL statements were autocreated and stored in dictionaries linked to file names, and each CSV file was loaded into Postgres in turn.  The CSVs in public are then deleted for housekeeping, and I include functions for deleting excess files from your folder while testing, as well as deleting test tables from the chosen database.

Going forward, I'd like to find a way to multithread the win32com-driven update process, I've been struggling to find methods that don't involve messing with the BIOS.

This is my first project on GitHub, and likely has numerous sections that could be more efficiently implemented.  It's part of my ongoing attempt to optimize and streamline the creation of custom ETL strategies for custom tasks.

How to use:
-requires modules psycopg2, os, csv, pandas, requests, time, openpyxl, zipfile, win32com (downloaded using pip install pywin32)
-download all .py files to a single folder
-include in that folder a database.ini file with format:

[postgresql]
host=#####
database=#####
user=#####
password=#####

- using ETLprojectMain, run it manually on your IDE or call it on the command line with the chosen project folder path as the one arguement
- you should now have a bunch of zip, excel and csv files in your project folder, as well as 6 new AG data tables in your database


Notes: 

- use deleteTest as second command line argument after path to delete old test files from project folder.
- I installed all of my packages through Anaconda prompt, and ran them through it.  Results may differ if using the main Windows command line.
