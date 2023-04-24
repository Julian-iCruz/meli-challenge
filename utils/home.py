import json
import pandas as pd
import streamlit as st

def showDefinitionVariables(texts):
    st.write(texts['Home_analysis'])
    st.divider()
    tab1, tab2, tab3, tab4 = st.tabs(["Variables Categóricas", "Variables Numéricas", "Variables Combinadas", "Comportamiento de usuario"])

    with tab1:
        st.header("Variables Categóricas")
        st.markdown(texts['Definition_categorical'])
        st.header("Un poco de teoría")
        showCategoricalTheory(texts)

    with tab2:
        st.header("Variables Numéricas")
        st.info('Variables Categóricas')

    with tab3:
        st.header("Variables Combinadas")
        st.info('Variables Categóricas')

    with tab4:
        st.header("Comportamiento de usuario")
        st.info('Variables Categóricas')
    return

def showCategoricalTheory(texts):
    st.write(texts['Home_analysis_categorical'])
    st.divider()

    st.subheader("Clasificación")
    col1, col2 = st.columns(2)

    with col1:
        with st.expander('Categóricas Nominales'):
            st.write(texts['Nominal_definition'])
            nominal = { "genero": ["Femenino","Masculino", "Otro", ""],
                    "estado civil": ["Soltero", "Casado", "Divoricado", "Viudo"]}
            df = pd.DataFrame(nominal) 
            st.dataframe(df, use_container_width = True)

    with col2:
        with st.expander('Categóricas Ordinales'):
            st.write(texts['Definition_ordinals'])
            ordinal = { "Calificación": ["Malo","Regular", "Bueno", "Excelente"],
                    "estado civil": ["Bachiller", "Pregrado", "Maestría", "Doctorado"]}
            df = pd.DataFrame(ordinal) 
            st.dataframe(df, use_container_width = True)
    
    st.subheader("Métricas y Gráficas")
    col1, col2 = st.columns(2)

    with col1:
        with st.expander('Métricas'):
            st.write(texts['Definition_metrics'])

    with col2:
        with st.expander('Gráficas'):
            st.info('Seccion en desarrollo')
    
    st.subheader("Tipos de análisis")
    with st.expander('Análisis univariado'):
            st.info('Seccion en desarrollo')
    with st.expander('Análisis bivariado'):
            st.info('Seccion en desarrollo')
    with st.expander('Análisis multivariados'):
            st.info('Seccion en desarrollo')
    return