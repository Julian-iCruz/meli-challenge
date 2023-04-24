import pandas as pd
import streamlit as st

def procesingLogin(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df["Action"]=="click(Btn_Login)"]
    df['Day'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Flag_day'] = df['Day'].isin(['Saturday','Sunday'])
    df['Flag_hour'] = (df['Hour'] >=8) & (df['Hour'] <=18)
    user_list = df['Login ID'].value_counts().keys()
    df['regular_hour'] = df.apply(compareTime, axis = 1, regular_hour_user = obtainRegularHours(df, user_list))
    return df.drop(['Action','Date', 'Page', 'Next Page', 'Content','Goal'], axis = 1)

def obtainRegularHours(df_in, user_list):
    regular_hours_dict = {}
    for user in user_list:
        df_user = df_in[df_in["Login ID"] == user]
        conteo = df_user["Hour"].value_counts()
        regular_hours_dict[user] = conteo[conteo > 2].index.to_list()
    return regular_hours_dict

def compareTime(row, regular_hour_user):
    return row["Login ID"] in regular_hour_user.keys() and row["Hour"] in regular_hour_user[row["Login ID"]]