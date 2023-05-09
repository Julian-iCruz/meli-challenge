import os 
import json
import pandas as pd
from PIL import Image
import streamlit as st
from utils.informe import *
from utils.sidebar import generateSidebar
from utils.utils import downloadData, joinData

st.set_page_config(page_title="Informe", page_icon="📰")

with open('texts.json', 'r') as archivo:
    texts = json.load(archivo)

df, columns = generateSidebar()

intro = texts['informe']['intro']
st.title('Análisis exploratorio de datos | EDA 📊')
st.markdown(intro['join'])
st.code(intro['code_join'], language='python')
st.markdown(intro['after_join'])
downloadData(joinData())
st.divider()

st.subheader('Análisis descriptivo 📊')
st.markdown(texts['informe']['descriptivo']['observations'])
try:
    len(df)
    st.dataframe(df)
except:
    st.warning("Proceed to load the dataset you downloaded earlier.", icon="🚨")
st.divider()

st.subheader('Análisis categorico 📊')
categorical = texts['informe']['categorical']
st.markdown(categorical['univariate'])
st.markdown(categorical['bivariate'])
st.markdown(categorical['multivariate'])
st.divider()

#image = Image.open('img/newplot.png')
#st.image(image, caption='Sunrise by the mountains')
st.title('Procesamiento de datos | 🛠')
processing = texts['informe']['processing']
st.markdown(processing['target_1'])
st.code(processing['code_1'], language='python')
st.write('Obtenemos el siguiente dataset procesado.')

if columns != None:
    try:
        df = procesingLogin(df)
        st.dataframe(df, use_container_width = True)
    except:
        st.warning("The data set could not be processed.", icon="🚨")
else:
    st.warning("Choose the dataset to be processed with the above code", icon="🚨")

st.markdown(processing['posprocessing_1'])
st.divider()

st.title('Preguntas Challenge |❔')
st.markdown(texts['informe']['questions'])