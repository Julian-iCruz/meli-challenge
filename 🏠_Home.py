import json
import pandas as pd
import streamlit as st
from utils.utils import *
from utils.home import *

st.set_page_config(page_title="Home", page_icon="🏠")

with open('texts.json', 'r') as archivo:
    texts = json.load(archivo)

st.title('MP Sec Tech Challenge 👋')
st.markdown(texts['Home_description'])
st.divider()

st.header('¿Que encontraras en la App?')
st.markdown(texts['Home_find'])

tab1, tab2, tab3, tab4 = st.tabs(['Informe', 'Descriptivo', 'Análisis de variables','Modelos'])

with tab1:
    ("""En esta sección encontrará todos los hallazgos realizados el explorar el dataset de igual manera podrá tener una visión más amplia de la toma de decisiones para el preprocesamiento de los datos y la definición de diferentes casos de uso que pueden ser planteados para atacar el tema principal que es la detección de anomalías.""")
with tab2:
    st.markdown("""La sección descriptiva es la que se encarga de unificar los datasets para el challenge en cuestión, pero también permite subir cualquier dataset con el fin de poder realizar su exploratorio en la sección 📊***Análisis de variables***""")
with tab3:
    showDefinitionVariables(texts)
with tab4:
    st.info('TAB 4')