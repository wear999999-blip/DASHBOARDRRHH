# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 19:52:01 2026

@author: wear_
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Análisis de Nómina y Desempeño", layout="wide")

# 2. CARGA DE DATOS (Ruta específica solicitada)
@st.cache_data
def load_data():
    ruta = r"C:\Users\wear_\OneDrive\Desktop\dashboard_rrhh\employees.csv"
    df = pd.read_csv(ruta)
    # Limpieza: Asegurar que las columnas estén en mayúsculas para evitar errores
    df.columns = [c.upper() for c in df.columns]
    return df

try:
    df = load_data()

    # Título Principal
    st.title("🏛️ Dashboard Ejecutivo de Talento Humano")
    st.markdown("---")

    # 3. BARRA LATERAL CON FILTROS (Segmentación)
    st.sidebar.header("Filtros de Análisis")
    deptos = st.sidebar.multiselect("Departamento:", options=df["DEPARTMENT"].unique(), default=df["DEPARTMENT"].unique())
    generos = st.sidebar.multiselect("Género:", options=df["GENDER"].unique(), default=df["GENDER"].unique())

    # Aplicar Filtros
    df_f = df[(df["DEPARTMENT"].isin(deptos)) & (df["GENDER"].isin(generos))]

    # 4. CUADROS DE SUMATORIA Y MÉTRICAS (KPIs)
    # Pediste: Sumatoria Salary, Promedio Salary y Conteo Empleados
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        total_nomina = df_f["SALARY"].sum()
        st.metric("Total Nómina (Sumatoria)", f"${total_nomina:,.2f}")
    
    with kpi2:
        promedio_sal = df_f["SALARY"].mean()
        st.metric("Salario Promedio", f"${promedio_sal:,.2f}")
        
    with kpi3:
        conteo_emp = len(df_f)
        st.metric("Total Empleados", f"{conteo_emp} personas")

    st.markdown("---")

    # 5. ANÁLISIS DE DESEMPEÑO Y ANTIGÜEDAD (Gráficos)
    col_a, col_b = st.columns(2)

    with col_a:
        # Relación Edad vs Salario por Género
        st.subheader("Distribución por Edad y Género")
        fig_age = px.histogram(df_f, x="AGE", color="GENDER", nbins=15,
                               title="Pirámide de Edad del Personal",
                               color_discrete_map={'Female': '#e07a5f', 'Male': '#3d5a80'})
        st.plotly_chart(fig_age, use_container_width=True)

    with col_b:
        # PerformanceScore por Departamento
        st.subheader("Puntaje de Desempeño por Unidad")
        # Corrección de sintaxis para conteo de categorías
        perf_data = df_f.groupby(["DEPARTMENT", "PERFORMANCESCORE"]).size().reset_index(name="CANTIDAD")
        fig_perf = px.bar(perf_data, x="DEPARTMENT", y="CANTIDAD", color="PERFORMANCESCORE",
                          title="Evaluación de Desempeño (PerformanceScore)",
                          barmode="group")
        st.plotly_chart(fig_perf, use_container_width=True)

    # 6. ANÁLISIS DE ANTIGÜEDAD (YearsAtCompany)
    st.subheader("Análisis de Retención y Antigüedad")
    fig_years = px.scatter(df_f, x="YEARSATCOMPANY", y="SALARY", 
                           color="DEPARTMENT", size="AGE",
                           hover_data=["PERFORMANCESCORE"],
                           title="Relación: Años en Compañía vs Salario")
    st.plotly_chart(fig_years, use_container_width=True)

    # 7. TABLA DETALLADA
    with st.expander("Ver base de datos filtrada"):
        st.write(df_f)

except Exception as e:
    st.error(f"Error detectado: {e}")
    st.info("Revisa que el archivo 'employees.csv' esté en la carpeta Dashboard_RRHH del escritorio.")