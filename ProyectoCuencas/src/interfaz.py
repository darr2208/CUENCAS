import streamlit as st
from src.mapa import mostrar_mapa_dibujable
from src.geocodificador import obtener_coordenadas
from src.morfometria import calcular_parametros
from src.exportacion import exportar_shapefile_zip, exportar_excel
import pandas as pd

def ejecutar_interfaz():
    st.set_page_config(page_title="Delimitación de Cuencas", layout="wide", page_icon="🌎")

    st.markdown("""
        <style>
            body { background-color: #eaf2fb; }
            .stApp { background-color: #eaf2fb; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌍 Delimitación de Cuencas y Análisis Morfométrico")
    st.markdown("Ingresa coordenadas o una ciudad. Se dibujará un rombo automáticamente y se calcularán los parámetros.")

    with st.expander("🔎 Buscar ciudad"):
        ciudad = st.text_input("Ejemplo: Medellín, Colombia")

    coordenadas = None
    if ciudad:
        coordenadas = obtener_coordenadas(ciudad)
        if coordenadas:
            st.success(f"📍 Coordenadas encontradas: {coordenadas}")
        else:
            st.error("❌ No se encontraron coordenadas para esa ciudad.")

    with st.expander("📍 O ingresa coordenadas manuales"):
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input("Latitud", format="%.6f")
        with col2:
            lon = st.number_input("Longitud", format="%.6f")
        if lat != 0.0 or lon != 0.0:
            coordenadas = [lat, lon]

    if coordenadas:
        st.subheader("🗺️ Mapa con delimitación automática (rombo)")
        geojson_data = mostrar_mapa_con_rombo(coordenadas)
    else:
        st.info("Esperando coordenadas para mostrar el mapa...")
        return

    if geojson_data:
        gdf, resultados = calcular_parametros(geojson_data)
        st.subheader("📊 Parámetros morfométricos calculados")
        df = pd.DataFrame([resultados])
        st.dataframe(df.drop(columns=["Centroide X", "Centroide Y"]), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            excel = exportar_excel(resultados)
            st.download_button("📥 Descargar Excel", data=excel, file_name="resultados_cuenca.xlsx")
        with col2:
            shapefile_zip = exportar_shapefile_zip(gdf)
            st.download_button("📥 Descargar Shapefile (.zip)", data=shapefile_zip, file_name="cuenca_shapefile.zip")
    else:
        st.warning("No se generó una geometría válida para calcular.")
