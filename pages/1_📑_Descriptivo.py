import json
import pandas as pd
import streamlit as st
from utils.utils import *

st.set_page_config(page_title="Descriptivo", page_icon="📑")

with open('texts.json', 'r') as archivo:
    texts = json.load(archivo)

st.title('Descriptivo 👋')
st.markdown("""
En esta sección podrá tener un primer acercamiento al set de datos que cargue en la sección inferior, este es afectado por los filtros que se despliegan a mano derecha, con el fin de segmentar los datos y poder analizar poblaciones específicas.
""")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.info('Asigne un nombre y de click en  ***Download data as CSV*** para obtener el dataset de los experimentos de primera y segunda ronda unidos.')
    downloadData(joinData())

with col2:
    st.info('Suba cualquier dataset de datos que desee explorar, para el caso puntual se hará uso del archivo descargado en la seccion de la izquierda.')
    uploaded_file = st.file_uploader("Escoja un archivo:")
    
st.divider()

if uploaded_file is not None:
    with open("dataset.json", "w") as file:
        json.dump({"Dataset_name" : uploaded_file.name}, file, indent=4)

    df_behavior = pd.read_csv(uploaded_file)
    df_behavior.to_csv(uploaded_file.name, index = False)
    ## ---------------------------------- Set de Datos ----------------------------------
    st.header('Vista Set de Datos 👋')
    st.markdown(texts['description'])
    variable_type = getVariableType(df_behavior)

## ---------------------------------- Sidebar ----------------------------------
    df_behavior = generateSidebar(df_behavior, variable_type)

    shape = df_behavior.shape
    st.write('Filas: ',shape[0], 'Columnas: ', shape[1])
    st.dataframe(df_behavior, use_container_width = True) 
    st.divider()

## ---------------------------------- Descripcion del dataset ----------------------------------
    st.header('Exploratorio de variables 👋')
    st.markdown(texts['Description_exploratorio'])

    df_describe = df_behavior.describe(include=['O'])
    df_dtype_null =  pd.DataFrame(data = getInfo(df_behavior), index = ['Type', 'Nulls'])
    df_describe =  pd.concat([df_describe, df_dtype_null.drop(['Date'], axis = 1)], axis = 0)
    st.dataframe(df_describe, use_container_width = True)
else:
    st.info('Escoja un archivo CSV para analizar', icon="⚠️")