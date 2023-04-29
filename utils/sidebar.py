import os
import pandas as pd
import streamlit as st
from datetime import time

def generateSidebar():
    folder_path = "datasets"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with st.sidebar.expander("File upload", expanded=True):
        uploadFiles(folder_path)
    selected_dataset = selectFile(folder_path)
    
    if selected_dataset != None:
        df = pd.read_csv(os.path.join(folder_path, selected_dataset))
        st.sidebar.header("Filtros generales")

        with st.sidebar.expander("Time range"):
            columns_type = getColumnsType(df)
            df[columns_type["categorical_columns"]] = df[columns_type["categorical_columns"]].astype(str)
            df = selectTimeRange(df, columns_type["datetime_columns"])
        st.write(df.shape)
        st.write(df)

def uploadFiles(folder_path):
    uploaded_file = st.file_uploader(label="Load dataset to be explored", type=["csv"], help="")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        file_path = os.path.join(folder_path, uploaded_file.name)
        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False)
            st.success("Successfully saved")
        else:
            st.warning("Already existing file", icon="🚨")
    return

def selectFile(folder_path):
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
    files.sort(key=os.path.getctime, reverse=True)
    files = [file.split("/")[1] for file in files]
    return st.sidebar.selectbox("Select the dataset to analyze", files, index=0, help="")

def getColumnsType(df):
    numerical_columns = df.select_dtypes(include=["int", "float"]).columns.tolist()
    datetime_columns = getDateTypeColumns(df.drop(columns=numerical_columns, axis=1))
    categorical_columns = df.drop(columns=numerical_columns + datetime_columns, axis=1).columns

    return {
        "datetime_columns" : datetime_columns,
        "categorical_columns" : categorical_columns,
        "numerical_columns" : numerical_columns,
    }

def getDateTypeColumns(df):
    list_date_type_columns = []
    for column in df.columns:
        try:
            pd.to_datetime(df[column])
            list_date_type_columns.append(column)
        except:
            pass
    return list_date_type_columns

def selectTimeRange(df, columns):
    datetime_columns = []
    if len(columns) != 0:
        datetime_columns = columns
    time_selector = st.selectbox("Select the datetime variables", datetime_columns, index=0)

    if time_selector != None:
        df[time_selector] = pd.to_datetime(df[time_selector])
        start_date = df[time_selector].min().date()
        end_date = df[time_selector].max().date()

        col1, col2 = st.columns(2)
        with col1:
            start_date_input = st.date_input("Start date", start_date)
            st.write(start_date)
        with col2:
            end_date_input = st.date_input("End date", end_date)
            st.write(end_date)
        df = df[(df[time_selector]>=pd.to_datetime(start_date_input)) & (df[time_selector]<=pd.to_datetime(end_date_input))]
        time_range = st.slider("Range of hours", value=(time(00, 00), time(23, 59)))
        df = df[(df[time_selector].apply(lambda x: x.time())>=time_range[0]) & (df[time_selector].apply(lambda x: x.time())<=time_range[1])]
    return df