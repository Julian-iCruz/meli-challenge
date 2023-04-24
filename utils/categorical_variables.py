import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from collections import Counter

def univariateAnalysis(df, categorical_columns):
    st.subheader("Análisis Univariado")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        generateUnivariateCategoricalGraph(df, categorical_columns, 'Key_variate_1', 'Subkey_variate_1', 2)

    with col2:
        generateUnivariateCategoricalGraph(df, categorical_columns, 'Key_variate_2', 'Subkey_variate_2', 3)
    return

def bivariateAnalysis(df, categorical_columns):
    st.subheader("Análisis Bivariado")
    st.divider()
    
    filters, subfilters = createFilterColumns(df, categorical_columns, 2)
    counter = Counter(filters)
    if not any(count > 1 for count in counter.values()):
        df, df_categorical_count, maximo, minimo = obtainMultivariateCount(df, filters)
        range_count = generateSliderFilter(minimo, maximo, 'slider_bi')
        df, df_categorical_count = filterSubcategories(df, df_categorical_count, filters, subfilters)
        conditional = (df_categorical_count['Count'] >= range_count[0]) & (df_categorical_count['Count'] <= range_count[1])
        df_categorical_count = df_categorical_count[conditional]
        col1, col2 = st.columns(2)
        
        with col1:
            checkbox_count_percentage = st.checkbox('Porcentaje')
        with col2:
            checkbox_group_stack = st.checkbox('Grupo')

        group_stack = 'stack'
        count_percentage = 'Count'
        if checkbox_group_stack:
            group_stack = 'group'
        if checkbox_count_percentage:
            count_percentage = 'Porcentaje'

        st.subheader('Grafico de barras')
        fig = px.bar(df_categorical_count, x = filters[0], y = count_percentage, color = filters[1], barmode = group_stack, height = 650)
        st.plotly_chart(fig, use_container_width = True)

        st.subheader('Conteos | Porcentajes')
        st.dataframe(df_categorical_count, use_container_width = True)
        showDescribe(df_categorical_count)
        
        st.subheader('Correlación')
        df_table = pd.crosstab(df[filters[0]], df[filters[1]])
        fig = px.imshow(df_table,x = df_table.columns,y = df_table.index, width = 800)
        st.plotly_chart(fig)

        showBoxPlot(df_categorical_count)
    else:
        st.warning('Escoja variables diferentes', icon="⚠️")
    return

def multivariateAnalysis(df, categorical_columns):
    st.subheader("Análisis Multivariado")
    st.divider()

    number_filters = st.slider('Cantidad de filtros', 1, 5, 4)
    filters, subfilters = createFilterColumns(df, categorical_columns, number_filters)
    counter = Counter(filters)
    if not any(count > 1 for count in counter.values()):
        df, df_categorical_count, maximo, minimo = obtainMultivariateCount(df, filters)
        range_count = generateSliderFilter(minimo, maximo, 'slider_multi')
        df, df_categorical_count = filterSubcategories(df, df_categorical_count, filters, subfilters)
        conditional = (df_categorical_count['Count'] >= range_count[0]) & (df_categorical_count['Count'] <= range_count[1])
        df_categorical_count = df_categorical_count[conditional]
        st.dataframe(df_categorical_count, use_container_width = True)
        showDescribe(df_categorical_count)
        showBoxPlot(df_categorical_count)
    else:
        st.warning('Escoja variables diferentes', icon="⚠️")
    return

def createFilterColumns(df, categorical_columns, number_columns):
    columns = st.columns(number_columns)
    filter_list = []; subfilter_list = []
    for column in range(len(columns)):
        with columns[column]:
            filter = (generateCategoricalFilter(categorical_columns, str(number_columns) + '_key_' + str(column), column + 1))
            filter_list.append(filter)
            subfilter = generateSubcategoricalFilter(df, filter, str(number_columns) + '_subkey_' + str(column))
            subfilter_list.append(subfilter)
    return filter_list, subfilter_list

def generateUnivariateCategoricalGraph(df, categorical_columns, key, subkey, index):
    filter = generateCategoricalFilter(categorical_columns, key, index)
    subfilter = generateSubcategoricalFilter(df, filter, subkey)
    df_categorical_count, maximo, minimo = obtainUnivariateCount(df, filter)
    range_count = generateSliderFilter(minimo, maximo, key)

    if len(subfilter) != 0:
        df_categorical_count = df_categorical_count.loc[subfilter]
    conditional = (df_categorical_count['Count'] >= range_count[0]) & (df_categorical_count['Count'] <= range_count[1])
    df_categorical_count = df_categorical_count[conditional]

    checkbox_count_percentage = st.checkbox('Porcentaje', key = 'checkbox_' + key)
    count_percentage = 'Count'
    if not checkbox_count_percentage:
        count_percentage = 'Porcentaje'

    st.subheader('Grafico de barras')
    st.bar_chart(df_categorical_count.drop([count_percentage], axis = 1), use_container_width = True)

    st.subheader('Conteos | Porcentajes')
    st.dataframe(df_categorical_count, use_container_width = True)
    
    st.subheader('Descriptivo de conteos')
    df_describe = df_categorical_count['Count'].describe().reset_index().T
    df_describe.columns = df_describe.loc['index']
    df_describe.drop(['index'], axis = 0, inplace = True)
    st.dataframe(df_describe)
    
    st.subheader('Gráfico de cajas')
    fig = px.box(df_categorical_count, y = ['Count'])
    st.plotly_chart(fig, use_container_width = True)

    return

def generateCategoricalFilter(categorical_columns, key, index):
    return st.selectbox('Categorica', categorical_columns, key = key, index = index)

def generateSubcategoricalFilter(df, categorical_selector, key):
    return st.multiselect(categorical_selector, df[categorical_selector].value_counts().keys(), key = key)

def generateSliderFilter(minimo, maximo, key):
    return st.slider('Rango de conteo', minimo, maximo, (minimo, maximo), key = key + '_slider')

def obtainUnivariateCount(df, column):
    categorical_count = df[column].value_counts().reset_index().set_index('index')
    categorical_count.rename(columns = {column : 'Count'}, inplace = True)
    total_counts = categorical_count['Count'].sum()
    categorical_count['Porcentaje'] = categorical_count['Count'] / total_counts * 100
    maximo = int(categorical_count['Count'].max())
    minimo = int(categorical_count['Count'].min())
    return categorical_count, maximo, minimo

def obtainMultivariateCount(df, columns):
    df_counts = df.groupby(columns).size().reset_index(name = 'Count')
    total_counts = df_counts['Count'].sum()
    df_counts['Porcentaje'] = df_counts['Count'] / total_counts * 100
    maximo = int(df_counts['Count'].max())
    minimo = int(df_counts['Count'].min())
    return df, df_counts, maximo, minimo

def filterSubcategories(df, df_counts, filters, subfilters):
    for filter, subfilter in zip(filters, subfilters):
        if len(subfilter) != 0:
            df_counts = df_counts[df_counts[filter].isin(subfilter)]
            df = df[df[filter].isin(subfilter)]
    return df, df_counts

def showDescribe(df):
    st.subheader('Descriptivo de conteos')
    df_describe = df['Count'].describe().reset_index().T
    df_describe.columns = df_describe.loc['index']
    df_describe.drop(['index'], axis = 0, inplace = True)
    st.dataframe(df_describe, use_container_width = True)
    return

def showBoxPlot(df):
    st.subheader('Gráfico de cajas')
    fig = px.box(df, x = ['Count'], orientation = 'h')
    st.plotly_chart(fig, use_container_width = True)
    return