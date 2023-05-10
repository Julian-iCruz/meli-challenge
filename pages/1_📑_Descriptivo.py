import json
import pandas as pd
import streamlit as st
from utils.utils import *
from utils.sidebar import generateSidebar

st.set_page_config(page_title="Descriptivo", page_icon="📑")

with open('texts.json', 'r') as archivo:
    texts = json.load(archivo)

df, columns = generateSidebar()

st.title('Descriptivo 👋')
st.markdown("""
En esta sección podrá tener un primer acercamiento al set de datos que cargue en la sección inferior, este es afectado por los filtros que se despliegan a mano derecha, con el fin de segmentar los datos y poder analizar poblaciones específicas.
""")
st.divider()

if columns != None:
    shape = df.shape
    st.write('Filas: ',shape[0], 'Columnas: ', shape[1])
    st.dataframe(df, use_container_width = True)
    downloadData(df, "data")
    st.divider()

    ## ---------------------------------- Descripcion del dataset ----------------------------------
    st.header('Exploratorio de variables 👋')
    descriptive = texts['descriptive']
    df_dtype_null =  pd.DataFrame(data = getInfo(df), index = ['Type', 'Nulls'])
    if len(columns["categorical"])!=0:
        st.markdown(descriptive["categorical_descriptive"])
        df_describe = df[columns["categorical"]].describe(include=['O'])
        df_describe =  pd.concat([df_describe, df_dtype_null.drop(columns["numerical"] + columns["datetime"], axis = 1)], axis = 0)
        st.dataframe(df_describe, use_container_width = True)
        shape = df_describe.shape
        st.write('Filas: ',shape[0], 'Columnas: ', shape[1])
    if len(columns["numerical"])!=0:
        st.markdown(descriptive["numerical_descriptive"])
        df_describe = df[columns["numerical"]].describe()
        df_describe =  pd.concat([df_describe, df_dtype_null.drop(columns["categorical"] + columns["datetime"], axis = 1)], axis = 0)
        st.dataframe(df_describe, use_container_width = True)
        shape = df_describe.shape
        st.write('Filas: ',shape[0], 'Columnas: ', shape[1])

else:
    st.info('Upload a Dataset file for analysis', icon="⚠️")