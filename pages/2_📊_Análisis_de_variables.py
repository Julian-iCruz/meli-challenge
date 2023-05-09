import json
import numpy as np
import pandas as pd
import streamlit as st
from datetime import time
from utils.utils import *
import plotly.express as px
from utils.categorical_variables import *
from utils.sidebar import generateSidebar
from utils.user_behavior import *

st.set_page_config(page_title="Análisis de variables", page_icon="📊")

with open('texts.json', 'r') as archivo:
    texts = json.load(archivo)

## ---------------------------------- Sidebar ----------------------------------
df, columns = generateSidebar()

## ---------------------------------- Análisis de variables ----------------------------------
st.title('Análisis de variables 👋')
with st.expander('Importancia del análisis de variables:'):
    st.markdown(texts['analysis_variables'])

if columns != None:
    tab1, tab2, tab3, tab4 = st.tabs(["Variables Categóricas", "Variables Numéricas", "Variables Combinadas", "Comportamiento de usuario"])

    ## ---------------------------------- Variables Categóricas ----------------------------------

    with tab1:
        if len(columns["categorical"]) != 0:
            st.header("Variables Categóricas")
            with st.expander('Que encontrara en este tablero:'):
                st.markdown(texts['categorical_variables'])
            st.divider()

            tab1_cat, tab2_cat, tab3_cat= st.tabs(["Análisis univariado", "Análisis bivariado", "Análisis multivariado"])

            with tab1_cat:
                univariateAnalysis(df, columns["categorical"])

            with tab2_cat:
                if len(columns["categorical"])>=2:
                    bivariateAnalysis(df, columns["categorical"])
                else:
                    st.info("Your dataset must have more than 2 categorical columns to make use of this section.", icon="⚠️")
            with tab3_cat:
                if len(columns["categorical"])>=3:
                    multivariateAnalysis(df, columns["categorical"])
                else:
                    st.info("Your dataset must have more than 3 categorical columns to make use of this section.", icon="⚠️")

        else:
            st.info('Su dataset no cuenta con variables Categóricas', icon="❕")
    ## ---------------------------------- Variables Numéricas ----------------------------------
    with tab2:
        if len(columns["numerical"]) != 0:
            st.header("Variables Numéricas")
        else:
            st.info('Su dataset no cuenta con variables Numericas', icon="❕")

    ## ---------------------------------- Variables Combinadas ----------------------------------
    with tab3:
        if len(columns["numerical"]) != 0 and len(columns["categorical"]) != 0:
            st.header("Variables Combinadas")
        else:
            st.info('Su dataset no cuenta con variables Numericas o Categóricas', icon="❕")

    ## ---------------------------------- Comportamiento de usuario ----------------------------------
    with tab4:
        st.header("Comportamiento de usuario")
        create_user_beahavior(df, columns)

else:
    st.info('Upload a Dataset file for analysis', icon="⚠️")