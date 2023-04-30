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
    
    if selected_dataset == None:
        return
    
    df = pd.read_csv(os.path.join(folder_path, selected_dataset))
    columns_type = getColumnsType(df)
    df[columns_type["categorical_columns"]] = df[columns_type["categorical_columns"]].astype(str)
    
    df, columns = filterDataset(df, columns_type)
    return df, columns

def uploadFiles(folder_path):
    uploaded_file = st.file_uploader(label="Load dataset to be explored", type=["csv"], help="")
    if not uploaded_file:
        return
    
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
    categorical_columns = df.drop(columns=numerical_columns + datetime_columns, axis=1).columns.to_list()

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

def filterDataset(df, columns_type):
    st.sidebar.header("Filtros generales")
    with st.sidebar.expander("Delete columns"):
        df, columns_drop = deleterColumns(df, columns_type)
    
    columns = {
        "datetime": set(columns_type["datetime_columns"]) - set(columns_drop["datetime_drop"]),
        "categorical": set(columns_type["categorical_columns"]) - set (columns_drop["categorical_drop"]),
        "numerical": set(columns_type["numerical_columns"]) - set(columns_drop["numerical_drop"]),
    }

    with st.sidebar.expander("Time range"):
        df = selectTimeRange(df, columns["datetime"])
    
    with st.sidebar.expander("Categorical columns"):
        df = filterCategoricalColumns(df, columns["categorical"])
    
    with st.sidebar.expander("Numerical columns"):
        df = filterNumericalColumns(df, columns["numerical"])
    return df, columns

def selectTimeRange(df, columns_datetime):
    datetime_columns = []
    if len(columns_datetime) != 0:
        datetime_columns = columns_datetime
    time_selector = st.selectbox("Select the datetime variables", datetime_columns, index=0)

    if time_selector == None:
        return df
    
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

def deleterColumns(df, columns_type):
    datetime_drop = st.multiselect("Datetime columns", columns_type["datetime_columns"])
    categorical_drop = st.multiselect("Categorical columns", columns_type["categorical_columns"])
    numerical_drop = st.multiselect("Numeric columns", columns_type["numerical_columns"])
    df.drop(columns=categorical_drop + numerical_drop + datetime_drop, axis=1, inplace=True)
    return df, {
        "datetime_drop": datetime_drop,
        "categorical_drop": categorical_drop,
        "numerical_drop": numerical_drop,
    }

def filterCategoricalColumns(df, columns_categorical):
    for column in columns_categorical:
        categorical_selector = st.multiselect(column, df[column].value_counts().keys(), key = column)
        if len(categorical_selector) != 0:
            df = df[df[column].isin(categorical_selector)]
    return df

def filterNumericalColumns(df, columns_numerical):
    for column in columns_numerical:
        max, min = [df[column].max(), df[column].min()]
        st.write(column)
        col1, col2 = st.columns(2)
        with col1:
            max_value = st.number_input('Maximum value', max_value=max, value=max, key=column+"_max")
        with col2:
            min_value = st.number_input('Minimum value', min_value=min, value=min, key=column+"_min")
        st.divider()
        df = df[(df[column]>=min_value) & (df[column]<=max_value)]
    return df

def deleteFile(file, folder_path):
    if st.sidebar.button("Delete file") and file:
        os.remove(os.path.join(folder_path, file))
        st.sidebar.success("Dataset deleted")
