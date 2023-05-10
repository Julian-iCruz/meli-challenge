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
downloadData(joinData(), "data_experiment")
st.markdown(intro['description'])
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

st.title('Procesamiento de datos | 🛠')
processing = texts['informe']['processing']
st.markdown(processing['target_1'])
st.code(processing['code_1'], language='python')
st.write('Obtenemos el siguiente dataset procesado.')

try:
    df_procesingLogin = procesingLogin(df)
    shape = df_procesingLogin.shape
    st.write('Filas: ',shape[0], 'Columnas: ', shape[1])
    st.dataframe(df_procesingLogin, use_container_width = True)
    downloadData(df_procesingLogin, "data_login")
except:
    st.warning("The data set could not be processed.", icon="🚨")
st.markdown(processing['posprocessing_1'])

st.markdown(processing['target_2'])
st.code(processing['code_2'], language='python')
st.write('Obtenemos el siguiente dataset procesado.')

try:
    df_procesingActionContent = procesingActionContent(df)
    st.dataframe(df_procesingActionContent, use_container_width = True)
    shape = df_procesingActionContent.shape
    st.write('Filas: ',shape[0], 'Columnas: ', shape[1])
    downloadData(df_procesingActionContent, "data_action_content")
except:
    st.warning("The data set could not be processed.", icon="🚨")
st.markdown(processing['posprocessing_2'])
st.divider()

st.title('Ataques y Vulnerabilidades |🧑🏻‍💻')
attacks_vulnerabilities = texts['informe']['attacks_vulnerabilities']

st.markdown(attacks_vulnerabilities["intro"])

st.markdown(attacks_vulnerabilities["risk"])
st.image(Image.open('img/1_riesgos_de_privacidad.jpg'))
st.markdown(attacks_vulnerabilities["risk_1"])
st.image(Image.open('img/2_riesgos_de_privacidad.jpg'))
st.markdown(attacks_vulnerabilities["risk_2"])

st.markdown(attacks_vulnerabilities["xss"])
st.image(Image.open('img/3_xss.jpg'))
st.markdown(attacks_vulnerabilities["xss_1"])
st.image(Image.open('img/4_xss.jpg'))
st.markdown(attacks_vulnerabilities["xss_2"])

st.markdown(attacks_vulnerabilities["sql"])
st.image(Image.open('img/5_sql.jpg'))
st.image(Image.open('img/6_sql.jpg'))
st.markdown(attacks_vulnerabilities["sql_1"])
st.image(Image.open('img/7_sql.png'))
st.markdown(attacks_vulnerabilities["sql_2"])

st.markdown(attacks_vulnerabilities["files"])
st.image(Image.open('img/8_files.jpg'))
st.markdown(attacks_vulnerabilities["files_1"])
st.image(Image.open('img/9_files.jpg'))
st.markdown(attacks_vulnerabilities["files_2"])

st.markdown(attacks_vulnerabilities["csrf"])
st.image(Image.open('img/10_csrf.png'))
st.image(Image.open('img/10_csrf.png'))
st.image(Image.open('img/12_csrf.png'))
st.markdown(attacks_vulnerabilities["csrf_1"])
st.image(Image.open('img/13_csrf.jpg'))
st.markdown(attacks_vulnerabilities["csrf_2"])

st.markdown(attacks_vulnerabilities["user"])
st.image(Image.open('img/14_user.png'))
st.markdown(attacks_vulnerabilities["user_1"])
st.image(Image.open('img/15_user.png'))
st.markdown(attacks_vulnerabilities["user_2"])
st.image(Image.open('img/16_user.png'))
st.markdown(attacks_vulnerabilities["user_3"])
st.image(Image.open('img/17_user.jpg'))
st.markdown(attacks_vulnerabilities["user_4"])
st.image(Image.open('img/18_user.png'))
st.markdown(attacks_vulnerabilities["user_5"])

st.divider()
st.title('Preguntas Challenge |❔')
st.markdown(texts['informe']['questions'])