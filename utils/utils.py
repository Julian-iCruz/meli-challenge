import numpy as np
import pandas as pd
import streamlit as st
from datetime import time

def joinData():
    df_firts_round_raw = pd.read_excel('Data of First_Round Experiment.xlsx', sheet_name = 'Raw Records')
    df_second_round_raw = pd.read_excel('Data of Second_Round Experiment.xlsx', sheet_name = 'Raw Records')
    df_firts_round = deleteNullRowsAndColumns(df_firts_round_raw)
    df_second_round_raw = deleteNullRowsAndColumns(df_firts_round_raw)
    df_behavior = pd.concat([df_firts_round, df_second_round_raw], axis = 0)
    return df_behavior

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

def downloadData(df):
    csv = convert_df(df)
    title = st.text_input('Nombre de descarga de su archivo', 'Data_Experiment')
    st.download_button(label="Download data as CSV", data = csv, file_name = str(title)+'.csv', mime='text/csv',)
    return

def deleteNullRowsAndColumns(df):
    df.dropna(axis = 0, how = 'all', inplace=True)
    df.dropna(axis = 1, how = 'all', inplace=True)
    return df.reset_index(drop = True)

def getInfo(df):
    describe = {}
    for column in df.columns:
        describe[column] = [str(df[column].dtype), df[column].isnull().sum()]
    return describe

def getVariableType(df):
    time_variable = []; numerical_variable = []; categorical_variable = []
    df_date = pd.DataFrame({'Date': ['2022-05-01'],'Categorica': ['Categoria'], 'Numerica': 10})
    df_date['Date'] = pd.to_datetime(df_date['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    for column in df.columns:
        if df_date['Date'].dtype == df[column].dtype:
            time_variable.append(column)
        elif df_date['Categorica'].dtype == df[column].dtype:
            categorical_variable.append(column)
        elif df_date['Numerica'].dtype == df[column].dtype:
            numerical_variable.append(column)
            
    dict_type_variables = {
        "time_variable" : time_variable,
        "categorical_variable" : categorical_variable,
        "numerical_variable" : numerical_variable,
    }
    return dict_type_variables

def generateSidebar(df, variable_type):
    st.sidebar.header('Filtros generales')
    st.sidebar.divider()
    star_date_input = ''; end_date_input = ''; time_range = ''

    with st.sidebar.expander("Rango de Tiempo"):
        st.divider()
        if len(variable_type['time_variable']) == 1:
            time_selector = variable_type['time_variable'][0]
        
        if len(variable_type['time_variable']) > 1:
            time_selector = st.sidebar.selectbox('Variables de Tiempo', df[variable_type['time_variable']].columns)
        
        if len(variable_type['time_variable']) != 0:
            start_date = df[time_selector].min().date()
            end_date = df[time_selector].max().date()

            col1, col2 = st.columns(2)

            with col1:
                start_date_input = st.date_input("Fecha de inicio", start_date)

            with col2:
                end_date_input = st.date_input("Fecha de fin", end_date)

            time_range = st.slider("Rango de hora", value=(time(00, 00), time(23, 59)))

    with st.sidebar.expander("Eliminar Columnas"):
        st.divider()
        categorical_drop = st.multiselect("Variables Categóricas", variable_type['categorical_variable'])
        numerical_drop = st.multiselect("Variables Numerica", variable_type['numerical_variable'])

    with st.sidebar.expander("Variables Categóricas"):
        st.divider()
        for column in variable_type['categorical_variable']:
            categorical_selector = st.multiselect(column, df[column].value_counts().keys(), key = column)
            if len(categorical_selector) != 0:
                df = df[df[column].isin(categorical_selector)]
    
    with st.sidebar.expander("Variables Numericas"):
        st.divider()
        numerical_selector = st.multiselect('Variables Categóricas', variable_type['numerical_variable'])

    start_date = pd.to_datetime(start_date_input)
    end_date = pd.to_datetime(end_date_input)
    df_behavior = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df_behavior = df_behavior.drop(categorical_drop, axis = 1)
    return df_behavior