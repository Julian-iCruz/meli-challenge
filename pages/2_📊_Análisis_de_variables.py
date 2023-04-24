import json
import numpy as np
import pandas as pd
import streamlit as st
from datetime import time
from utils.utils import *
import plotly.express as px
from utils.categorical_variables import *

st.set_page_config(page_title="Análisis de variables", page_icon="📊")

with open('texts.json', 'r') as archivo:
    texts = json.load(archivo)

with open('dataset.json', 'r') as archivo:
    dataset = json.load(archivo)

df_behavior = pd.read_csv(dataset['Dataset_name'])
df_behavior['Date'] = pd.to_datetime(df_behavior['Date'])
variable_type = getVariableType(df_behavior)

time_columns = variable_type['time_variable']
categorical_columns = variable_type['categorical_variable']
numerical_columns = variable_type['numerical_variable']

## ---------------------------------- Sidebar ----------------------------------
df_behavior = generateSidebar(df_behavior, variable_type)

## ---------------------------------- Análisis de variables ----------------------------------
st.title('Análisis de variables 👋')
with st.expander('Importancia del análisis de variables:'):
    st.markdown(texts['analysis_variables'])

tab1, tab2, tab3, tab4 = st.tabs(["Variables Categóricas", "Variables Numéricas", "Variables Combinadas", "Comportamiento de usuario"])

## ---------------------------------- Variables Categóricas ----------------------------------

with tab1:
    if len(categorical_columns) != 0:
        st.header("Variables Categóricas")
        with st.expander('Que encontrara en este tablero:'):
            st.markdown(texts['categorical_variables'])
        st.divider()

        tab1_cat, tab2_cat, tab3_cat= st.tabs(["Análisis univariado", "Análisis bivariado", "Análisis multivariado"])

        with tab1_cat:
            univariateAnalysis(df_behavior, categorical_columns)

        with tab2_cat:
            bivariateAnalysis(df_behavior, categorical_columns)
        
        with tab3_cat:
            multivariateAnalysis(df_behavior, categorical_columns)
    else:
        st.info('Su dataset no cuenta con variables Categóricas', icon="❕")
## ---------------------------------- Variables Numéricas ----------------------------------
with tab2:
    if len(numerical_columns) != 0:
        st.header("Variables Numéricas")
    else:
        st.info('Su dataset no cuenta con variables Numericas', icon="❕")

## ---------------------------------- Variables Combinadas ----------------------------------
with tab3:
    if len(numerical_columns) != 0 and len(categorical_columns) != 0:
        st.header("Variables Combinadas")
    else:
        st.info('Su dataset no cuenta con variables Numericas o Categóricas', icon="❕")

## ---------------------------------- Comportamiento de usuario ----------------------------------
with tab4:
    st.header("Comportamiento de usuario")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)