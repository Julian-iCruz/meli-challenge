import os 
import json
import pandas as pd
import streamlit as st
from utils.informe import *
from utils.sidebar import generateSidebar

st.set_page_config(page_title="Informe", page_icon="📰")

with open('texts.json', 'r') as archivo:
    texts = json.load(archivo)

df, columns = generateSidebar()

st.title('Análisis exploratorio de datos | EDA 📊')
st.markdown(texts['informe']['EDA'])

st.title('Procesamiento de datos | 🛠')
st.markdown(texts['informe']['Procesamiento'])
st.code(texts['informe']['Code'], language='python')
st.write('Obtenemos el siguiente dataset procesado.')

if columns != None:
    try:
        df = procesingLogin(df)
        st.dataframe(df, use_container_width = True)
    except:
        st.warning("The data set could not be processed.", icon="🚨")
else:
    st.warning("Choose the dataset to be processed with the above code", icon="🚨")

st.markdown(texts['informe']['Procesamiento_1'])
st.divider()

st.title('Preguntas Challenge | ❔')
st.markdown("""
* Indicar qué información necesitarías para mejorar/ampliar tu entregable.

Bueno, creo que con un poco más de tiempo se podrían lograr grandes cambios en la aplicación que planteo como solución, ya que sería una plataforma que minimizaría tiempo y esfuerzo a la hora de crear análisis exploratorio de datos con respecto a las formas tradicionales de hacerlo, incluso se podría llegar un nivel más alto de automatización donde se generen informes que contextualicen al usuario de la información más importante del conjunto de datos.

De igual manera, se podría crear una sección de modelos que pueda realizar pruebas y sacar métricas de estos de manera interactiva.

* ¿Cómo crees que podría mejorarse el dataset desde la creación del mismo si lo tuvieses que procesar?

Se podrían traer algunas variables clasificatorias para los usuarios que ayudarían a segmentar la población de buena manera, por ejemplo:

1. Edad
2. Genero
3. Profesion
4. Informacion demografica

Tambien se puede establecer un protocolo de calidad de datos que puede ayudar a garantizar que los datos se recopilen y procesen de manera consistente y precisa, lo que aumenta la confiabilidad y la validez del dataset.


* ¿Cuáles serían las ventajas de poseer labels en este dataset?

La ventaja principal es que podrían implementar técnicas de aprendizaje supervisado, esto también ayuda a comprender mejor la estructura y patrones de los datos. De igual manera, pueden mejorar la precisión de los resultados obtenidos en los modelos, al igual que hay un ahorro de tiempo y recursos para evitar etiquetar datos manualmente o con técnicas de aprendizaje no supervisado.

* ¿De poseer aún más datos relacionados con el consumo de dicho site, crees que podríamos identificar ataques sobre el mismo?¿De qué tipo?.

Si, en lo absoluto, a pesar de que ya se tiene una gran cantidad de datos, puede que en un caso de uso donde se busque entender el comportamiento de cada usuario estos datos se queden cortos, en un sistema de modelos escalonados donde primero se determina si un evento es anómalo entre todo el dataset o de todos los eventos generados y luego un modelo especifico por usuario el tener más datos por usuario mejora el entendimiento de la línea base de comportamiento del mismo.
""")