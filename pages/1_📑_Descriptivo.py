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
    st.divider()

    ## ---------------------------------- Descripcion del dataset ----------------------------------
    st.header('Exploratorio de variables 👋')
    st.markdown(texts['Description_exploratorio'])
    df_describe = df.describe(include=['O'])
    df_dtype_null =  pd.DataFrame(data = getInfo(df), index = ['Type', 'Nulls'])
    df_describe =  pd.concat([df_describe, df_dtype_null.drop(['Date'], axis = 1)], axis = 0)
    st.dataframe(df_describe, use_container_width = True)
else:
    st.info('Upload a Dataset file for analysis', icon="⚠️")