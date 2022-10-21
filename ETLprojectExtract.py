# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 17:35:12 2022

@author: marca
"""
import requests, os, time
import pandas as pd
from zipfile import ZipFile
from openpyxl import load_workbook

import csv
import win32com.client as win32


def extract_NZ_ag_files(path):
    """
    INPUT
    -------
        path: string, path (with r in the beginning) pointing to project folder

    Returns
    -------
    df_relev : dictionary, a dictionary of Pandas DataFrames extracted from the original Excel files

    """

    home_folder = path

    os.chdir(home_folder)

    print("Retrieving Ag Production ZIP file from NZ gov stats site")

    url = "https://www.stats.govt.nz/assets/Uploads/Agricultural-production-statistics/Agricultural-Production-Statistics-key-tables-from-APS-2002-2017.zip"

    # Downloading the file by sending the request to the URL
    req = requests.get(url)

    # Split URL to get the file name
    filename = url.split("/")[-1]

    # Writing the file to the local file system
    print("Downloading zip file")

    with open(filename, "wb") as output_file:
        output_file.write(req.content)

    # unzipping file
    print("Unzipping file")

    agZip = ZipFile(
        home_folder
        + "\Agricultural-Production-Statistics-key-tables-from-APS-2002-2017.zip"
    )

    agZip.extractall(home_folder)

    agZip.close()

    # unzipping internal files
    print("Unzipping internal files")

    for file in os.listdir(home_folder):
        if os.path.splitext(file)[1] == ".zip":
            minizip = ZipFile(home_folder + f"\{file}")
            minizip.extractall(home_folder)
            minizip.close()

    

    # Convert older Excel files to newer filetypes
    print("Selecting and Updating Excel Filetypes")
    i = 0
    for file in os.listdir(home_folder):

        if os.path.splitext(file)[1] == ".xls" and "sum" in os.path.splitext(file)[
            0
        ].split("-"):

            # excel = win32.DispatchEx('Excel.Application') #uses new instance of excel
            excel = win32.gencache.EnsureDispatch(
                "Excel.Application"
            )  # uses current instance of excel

            # create new workbook
            wb_new = excel.Workbooks.Add()
            wb_new.SaveAs(home_folder + f"\{os.path.splitext(file)[0]}" + ".xlsx")
            wb_old = excel.Workbooks.Open(home_folder + f"\{file}")

            for sh in wb_old.Sheets:
                wb_old.Worksheets(sh.Name).Move(Before=wb_new.Worksheets("Sheet1"))

            wb_new.Worksheets("Sheet1").Delete()
            wb_new.Save()
            excel.Application.Quit()
            del excel  # ensure Excel process ends
            i += 1

        if i == len(os.listdir(home_folder)):
            print("Files updated")
            break

    # Deleting titles from Excel files, clean up rows, and convert to CSV files
    print("Cleaning and Converting Excel files to CSV")

    for file in os.listdir(home_folder):
        if os.path.splitext(file)[1] == ".xlsx":

            wb = load_workbook(file)
            ws = wb.worksheets[0]
            ws.delete_rows(1, 5)

            if "1" in os.path.splitext(file)[0].split("-"):
                print(f"Fixing {file}")
                ws.delete_rows(2, 1)
                ws.delete_rows(51, 3)
                ws.delete_rows(80, 12)

            if "2" in os.path.splitext(file)[0].split("-"):
                print(f"Fixing {file}")
                ws.delete_rows(3, 2)
                ws.delete_rows(33, 8)
                ws.delete_rows(1, 1)

            if "3" in os.path.splitext(file)[0].split("-"):
                print(f"Fixing {file}")
                ws.delete_rows(2, 2)
                ws.delete_rows(39, 9)

            if "4" in os.path.splitext(file)[0].split("-"):
                print(f"Fixing {file}")
                ws.delete_rows(2, 2)
                ws.delete_rows(53, 3)
                ws.delete_rows(81, 10)
                ws.delete_rows(76, 4)
                ws.delete_rows(51, 2)

            if "5" in os.path.splitext(file)[0].split("-"):
                print(f"Fixing {file}")
                ws.delete_rows(2, 1)
                ws.delete_rows(31, 8)

            if "6" in os.path.splitext(file)[0].split("-"):
                print(f"Fixing {file}")
                ws.delete_rows(2, 1)
                ws.delete_rows(12, 3)
                ws.delete_rows(23, 9)

            # writer object is created
            col = csv.writer(open(os.path.splitext(file)[0] + ".csv", "w", newline=""))

            # writing the data in csv file
            for r in ws.rows:
                col.writerow([cell.value for cell in r])

            wb.close()

    # fetching CSV files and converting into pandas DataFrames, storing them in dictionary

    df_dict = {}

    print("Fetching CSV files and converting to DataFrame dictionary")

    for file in os.listdir(home_folder):
        if os.path.splitext(file)[1] == ".csv":

            try:
                df = pd.read_csv(file)
                df_dict[os.path.splitext(file)[0]] = df
            except:
                pass

    df_relev = {}

    for file in df_dict:
        if "sum" in file.split("-"):

            df_relev[file] = df_dict[file]

    return df_relev


def delete_old_test_files(path):
    """
    INPUT: 
    ------    
        path: string, path (with r in the beginning) pointing to project folder

    Deletes Excel, zip and CSV files in the project folder

    """

    home_folder = path

    os.chdir(home_folder)
    ext_list = [".xlsx", ".xls", ".zip", ".csv"]
    for file in os.listdir(home_folder):
        if os.path.splitext(file)[1] in ext_list:
            print(f"Deleting file {file}")
            os.unlink(home_folder + f"\{file}")

    print("----All extra files deleted----")
