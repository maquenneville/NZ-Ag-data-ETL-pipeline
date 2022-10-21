# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 19:39:34 2022

@author: marca
"""

import pandas as pd
import numpy as np


def transform_data(df_relev):
    """


    Parameters
    ----------
    df_relev : dictonary, a dictionary of DataFrames extracted for the AG NZ data zip folder

    Returns
    -------
    df_final : dictionary, a dictionary of cleaned DataFrames, with updated filetypes,
                column names, and null values replaced with means

    """

    df_final = {}

    ####Clean first dataframe

    print("-----Cleaning first dataframe-----")

    # seperate dataframe
    livestock = df_relev["1-sum-livestock"]

    # remove empty columns
    for col in list(livestock.columns):
        if "Unnamed" in col:
            del livestock[col]

    ##fix column names to fit convention
    name_dict = {}
    for col in list(livestock.columns):
        new_name = "".join([word.title() for word in col.split(" ")])

        name_dict[col] = new_name

    livestock.rename(columns=name_dict, inplace=True)
    livestock.rename(
        columns={
            "Ewes(2ToothAndOver)PutToRam": "EwesPutToRam",
            "DairyCows&Heifers(Over1YearOld)InMilkOrCalf": "DairyCowsAndHeifers",
            "BeefCowsAndHeifersInCalf": "BeefCowsAndHeifers",
        },
        inplace=True,
    )

    # remove errant letters, to be replaced with means (as they are simply "no response" records)
    livestock = livestock.replace(to_replace=["..C", "..S", "R"], value=None)

    # remove errant '-' values, convert columns to numeric, fill null value with means of their columns
    # then round
    ta = livestock.TerritorialAuthority.tolist()

    del livestock["TerritorialAuthority"]

    fillna_dict = {}
    round_dict = {}
    for col in livestock.columns:
        for val in livestock[col].tolist():
            if val == "-":
                livestock[livestock[col] == "-"] = None

        livestock[col] = pd.to_numeric(livestock[col])

        fillna_dict[col] = livestock[col].mean()

        round_dict[col] = 0

    livestock.fillna(value=fillna_dict, inplace=True)

    livestock = livestock.round(round_dict)

    livestock.insert(0, "TerritorialAuthority", ta)

    df_final["livestock_total"] = livestock

    ###Clean second dataframe
    print("-----Cleaning second dataframe-----")

    graze_farm = df_relev["2-sum-graze-farm"]

    for col in list(graze_farm.columns):
        if "Unnamed" in col:
            del graze_farm[col]

    ##fix column names to fit convention
    name_dict = {}
    for col in list(graze_farm.columns):
        new_name = "".join([word.title() for word in col.split(" ")])

        name_dict[col] = new_name

    graze_farm.rename(columns=name_dict, inplace=True)
    graze_farm.rename(columns={"FarmType(Anzsic)": "FarmTypeAnzsic"}, inplace=True)

    # remove errant letters, to be replaced with means (as they are simply "no response" records)
    graze_farm = graze_farm.replace(to_replace=["..C", "..S", "R"], value=None)

    # remove errant '-' values, convert columns to numeric then round
    ta = graze_farm.FarmTypeAnzsic.tolist()

    del graze_farm["FarmTypeAnzsic"]

    fillna_dict = {}
    round_dict = {}
    for col in graze_farm.columns:
        for val in graze_farm[col].tolist():
            if val == "-":
                graze_farm[graze_farm[col] == "-"] = None

        graze_farm[col] = pd.to_numeric(graze_farm[col])

        fillna_dict[col] = graze_farm[col].mean()

        round_dict[col] = 0

    graze_farm.fillna(value=fillna_dict, inplace=True)

    graze_farm = graze_farm.round(round_dict)

    graze_farm.insert(0, "FarmTypeAnzsic", ta)

    df_final["graze_farm"] = graze_farm

    ###Clean third dataframe
    print("-----Cleaning third dataframe-----")

    graze_region = df_relev["3-sum-graze-region"]

    for col in list(graze_region.columns):
        if "Unnamed" in col:
            del graze_region[col]

    ##fix column names to fit convention
    name_dict = {}
    for col in list(graze_region.columns):
        new_name = "".join([word.title() for word in col.split(" ")])

        name_dict[col] = new_name

    graze_region.rename(columns=name_dict, inplace=True)

    # remove errant letters, to be replaced with means (as they are simply "no response" records)
    graze_region = graze_region.replace(to_replace=["..C", "..S", "R"], value=None)

    # remove errant '-' values, convert columns to numeric then round
    ta = graze_region.Region.tolist()

    del graze_region["Region"]

    fillna_dict = {}
    round_dict = {}
    for col in graze_region.columns:
        for val in graze_region[col].tolist():
            if val == "-":
                graze_region[graze_region[col] == "-"] = None

        graze_region[col] = pd.to_numeric(graze_region[col])

        fillna_dict[col] = graze_region[col].mean()

        round_dict[col] = 0

    graze_region.fillna(value=fillna_dict, inplace=True)

    graze_region = graze_region.round(round_dict)

    graze_region.insert(0, "Region", ta)

    df_final["graze_region"] = graze_region

    ###Clean fourth dataframe
    print("-----Cleaning fourth dataframe-----")

    territorial = df_relev["4-sum-graze-territorial"]

    for col in list(territorial.columns):
        if "Unnamed" in col:
            del territorial[col]

    territorial = territorial[territorial["Territorial Authority"] != "NaN"]

    ##fix column names to fit convention
    name_dict = {}
    for col in list(territorial.columns):
        new_name = "".join([word.title() for word in col.split(" ")])

        name_dict[col] = new_name

    territorial.rename(columns=name_dict, inplace=True)

    # remove errant letters, to be replaced with means (as they are simply "no response" records)
    territorial = territorial.replace(to_replace=["..C", "..S", "R"], value=None)

    # remove errant '-' values, convert columns to numeric then round
    ta = territorial.TerritorialAuthority.tolist()

    del territorial["TerritorialAuthority"]

    fillna_dict = {}
    round_dict = {}
    for col in territorial.columns:
        for val in territorial[col].tolist():
            if val == "-":
                territorial[territorial[col] == "-"] = None

        territorial[col] = pd.to_numeric(territorial[col])

        fillna_dict[col] = territorial[col].mean()

        round_dict[col] = 0

    territorial.fillna(value=fillna_dict, inplace=True)

    territorial = territorial.round(round_dict)

    territorial.insert(0, "TerritorialAuthority", ta)

    df_final["territorial"] = territorial

    ###Clean fifth dataframe
    print("-----Cleaning fifth dataframe-----")

    livestock_farm = df_relev["5-sum-livestock-farm"]

    for col in list(livestock_farm.columns):
        if "Unnamed" in col:
            del livestock_farm[col]

    # fix column names to fit convention
    name_dict = {}
    for col in list(livestock_farm.columns):
        new_name = "".join([word.title() for word in col.split(" ")])

        name_dict[col] = new_name

    livestock_farm.rename(columns=name_dict, inplace=True)
    livestock_farm.rename(
        columns={
            "FarmType(Anzsic)": "FarmTypeAnzsic",
            "DairyCows&Heifers(Over1YearOld)InMilkOrCalf": "DairyCowsAndHeifers",
            "BeefCowsAndHeifers(InCalf)": "BeefCowsAndHeifers",
            "Ewes(2ToothAndOver)PutToRam": "EwesPutToRam",
        },
        inplace=True,
    )

    # remove errant letters, to be replaced with means (as they are simply "no response" records)
    livestock_farm = livestock_farm.replace(to_replace=["..C", "..S", "R"], value=None)

    # remove errant '-' values, convert columns to numeric then round
    ta = livestock_farm.FarmTypeAnzsic.tolist()

    del livestock_farm["FarmTypeAnzsic"]

    fillna_dict = {}
    round_dict = {}
    for col in livestock_farm.columns:
        for val in livestock_farm[col].tolist():
            if val == "-":
                livestock_farm[livestock_farm[col] == "-"] = None

        livestock_farm[col] = pd.to_numeric(livestock_farm[col])

        fillna_dict[col] = livestock_farm[col].mean()

        round_dict[col] = 0

    livestock_farm.fillna(value=fillna_dict, inplace=True)

    livestock_farm = livestock_farm.round(round_dict)

    livestock_farm.insert(0, "FarmTypeAnzsic", ta)

    df_final["livestock_farm"] = livestock_farm

    # Clean sixth dataframe
    print("-----Cleaning sixth dataframe-----")

    livestock_region = df_relev["6-sum-livestock-region"]

    for col in list(livestock_region.columns):
        if "Unnamed" in col:
            del livestock_region[col]

    # fix column names to fit convention
    name_dict = {}
    for col in list(livestock_region.columns):
        new_name = "".join([word.title() for word in col.split(" ")])

        name_dict[col] = new_name

    livestock_region.rename(columns=name_dict, inplace=True)

    livestock_region.rename(
        columns={
            "DairyCows&Heifers(Over1YearOld)InMilkOrCalf": "DairyCowsAndHeifers",
            "BeefCowsAndHeifersInCalf": "BeefCowsAndHeifers",
            "Ewes(2ToothAndOver)PutToRam": "EwesPutToRam",
        },
        inplace=True,
    )

    # remove errant letters, to be replaced with means (as they are simply "no response" records)
    livestock_region = livestock_region.replace(
        to_replace=["..C", "..S", "R"], value=None
    )

    # remove errant '-' values, convert columns to numeric then round
    ta = livestock_region.Region.tolist()

    del livestock_region["Region"]

    fillna_dict = {}
    round_dict = {}
    for col in livestock_region.columns:
        for val in livestock_region[col].tolist():
            if val == "-":
                livestock_region[livestock_region[col] == "-"] = None

        livestock_region[col] = pd.to_numeric(livestock_region[col])

        fillna_dict[col] = livestock_region[col].mean()

        round_dict[col] = 0

    livestock_region.fillna(value=fillna_dict, inplace=True)

    livestock_region = livestock_region.round(round_dict)

    livestock_region.insert(0, "Region", ta)

    df_final["livestock_region"] = livestock_region

    return df_final
