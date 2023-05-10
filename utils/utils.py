import os
import json
import numpy as np
import pandas as pd
import streamlit as st
from datetime import time

def joinData():
    df_firts_round_raw = pd.read_excel("Data of First_Round Experiment.xlsx", sheet_name = "Raw Records")
    df_second_round_raw = pd.read_excel("Data of Second_Round Experiment.xlsx", sheet_name = "Raw Records")
    df_firts_round = deleteNullRowsAndColumns(df_firts_round_raw)
    df_second_round_raw = deleteNullRowsAndColumns(df_firts_round_raw)
    df_behavior = pd.concat([df_firts_round, df_second_round_raw], axis = 0)
    return df_behavior

@st.cache_data
def convertDf(df):
    return df.to_csv(index=False).encode("utf-8")

def downloadData(df, df_name):
    csv = convertDf(df)
    st.download_button(label="Download data as CSV", data = csv, file_name = str(df_name)+".csv", mime="text/csv",)
    return

def deleteNullRowsAndColumns(df):
    df.dropna(axis = 0, how = "all", inplace=True)
    df.dropna(axis = 1, how = "all", inplace=True)
    return df.reset_index(drop = True)

def getInfo(df):
    describe = {}
    for column in df.columns:
        describe[column] = [str(df[column].dtype), df[column].isnull().sum()]
    return describe