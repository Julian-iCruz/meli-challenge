import pandas as pd
import streamlit as st
import plotly.express as px
from utils.categorical_variables import generateSubcategoricalFilter

def create_user_beahavior(df, columns):
    date_column, grouping_column, graph_frequency = generateFilters(columns)
    try:
        df_group = df.groupby([pd.Grouper(key=date_column, freq=graph_frequency)] + grouping_column).size().reset_index()
    except:
        st.info("Change the date column or your dataset has no date columnl", icon="⚠️")
        return
    
    df_group = df_group.rename(columns={0: "count"})
    
    if len(grouping_column)==0:
        st.info("Choose grouping variables", icon="⚠️")
        return
    
    subfilter_list = []
    columns_user = st.columns(len(grouping_column))
    for column in range(len(grouping_column)):
        with columns_user[column]:
            subfilter = generateSubcategoricalFilter(df_group, grouping_column[column], str(column) + '_subkey_' + str(grouping_column[column]) + "_user_behavior")
            subfilter_list.append(subfilter)
    
    df_filtered = filterSubcategories(df_group, grouping_column, subfilter_list)
    df_graph = df_filtered

    col1, col2 = st.columns(2)
    with col1:
        color_filter = st.selectbox("Color", [""] + grouping_column, index=0)
    with col2:    
        symbol_filter = st.selectbox("Symbol", [""] + grouping_column, index=0)
    
    if color_filter=="" and symbol_filter=="":
        st.info("Select Color or Symbol", icon="⚠️")
        return
    
    if color_filter!="" and symbol_filter=="":
        fig = px.line(df_graph, x=date_column, y="count", color=color_filter)
    elif color_filter=="" and symbol_filter!="":
        fig = px.line(df_graph, x=date_column, y="count", symbol=symbol_filter)
    elif color_filter!="" and symbol_filter!="":
        fig = px.line(df_graph, x=date_column, y="count", color=color_filter, symbol=symbol_filter)
    st.plotly_chart(fig, use_container_width = True)
    return

def generateFilters(columns):
    frecuency = {
        "Año": "Y",
        "Mes": "M",
        "Semana": "W",
        "Dia": "D",
        "Hora": "H",
        "Minuto": "min",
        "Segundo": "S",
    }
    col1, col2, col3 = st.columns(3)

    with col1:
        date_column = st.selectbox("Date column", columns["datetime"])
    with col2:
        number_periodicity = st.number_input("", step=1, min_value=1, value=1)
    with col3:
        periodicity = st.selectbox("Periodicity", frecuency.keys(), index=5)
    graph_frequency = str(int(number_periodicity)) + frecuency[periodicity]
    grouping_column = st.multiselect("Grouping variables", columns["categorical"])
    return date_column, grouping_column, graph_frequency

def filterSubcategories(df, filters, subfilters):
    for filter, subfilter in zip(filters, subfilters):
        if len(subfilter) != 0:
            df = df[df[filter].isin(subfilter)]
    return df

