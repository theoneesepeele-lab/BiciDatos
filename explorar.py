import streamlit as st
import pandas as pd

st.title("Explorar los datos")

archivo = st.file_uploader("Selecciona bicicletas_listas.csv", type=["csv"])

if st.button("Cargar datos"):
    if archivo is not None:
        df_leido = pd.read_csv(archivo, parse_dates=["fecha"], encoding="utf-8-sig")
        st.session_state["df"] = df_leido
    else:
        st.warning("Por favor selecciona el archivo CSV antes de pulsar Cargar datos.")

if st.session_state["df"] is None:
    st.info("Para comenzar, selecciona el archivo bicicletas_listas.csv y haz clic en 'Cargar datos'.")
    st.stop()

df = st.session_state["df"].copy()
st.success(f"{len(df):,} registros cargados.")

tipo_usuario = st.session_state["tipo_usuario"]
tipo_dia = st.session_state["tipo_dia"]
hora_ini, hora_fin = st.session_state["horas"]

mapa_columnas = {
    "Todos": "alquileres_total",
    "Ocasionales": "alquileres_ocasionales",
    "Registrados": "alquileres_registrados"
}
col_activa = mapa_columnas[tipo_usuario]

df_filtrado = df[(df["hora"] >= hora_ini) & (df["hora"] <= hora_fin)].copy()
if tipo_dia != "Todos":
    df_filtrado = df_filtrado[df_filtrado["tipo_dia"] == tipo_dia]

col1, col2 = st.columns(2)
total_alq = int(df_filtrado[col_activa].sum())
prom_hora = df_filtrado[col_activa].mean() if len(df_filtrado) > 0 else 0.0

col1.metric("Total de alquileres", f"{total_alq:,}".replace(",", "."))
col2.metric("Promedio por hora observada", f"{prom_hora:,.1f}".replace(".", ","))

tab1, tab2 = st.tabs(["Gráfico diario", "Datos"])

with tab1:
    diario = df_filtrado.groupby("fecha", as_index=False)[col_activa].sum()
    st.line_chart(
        diario,
        x="fecha",
        y=col_activa,
        x_label="Fecha",
        y_label="Alquileres por día",
        color="#197A8D"
    )

with tab2:
    df_mostrar = df_filtrado.copy()
    df_mostrar["alquileres"] = df_mostrar[col_activa]
    
    st.dataframe(df_mostrar, use_container_width=True)
    
    csv_descarga = df_mostrar.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="Descargar datos filtrados",
        data=csv_descarga,
        file_name="bicicletas_filtradas.csv",
        mime="text/csv"
    )
    
    st.caption("Fanaee-T, H. (2013). Bike Sharing [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894. Licencia CC BY 4.0.")
    st.link_button("Consultar la fuente en UCI", "https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset")
