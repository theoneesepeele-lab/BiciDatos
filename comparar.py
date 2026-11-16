import streamlit as st
import pandas as pd

st.title("Comparar horarios")

if st.session_state["df"] is None:
    st.info("Primero debes cargar los datos en la página 'Explorar los datos'.")
    st.stop()

df = st.session_state["df"].copy()

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

color_barras = st.color_picker("Color de las barras", "#197A8D")

prom_horas = df_filtrado.groupby("hora", as_index=False)[col_activa].mean()
prom_horas.rename(columns={col_activa: "promedio_alquileres"}, inplace=True)

st.bar_chart(
    prom_horas,
    x="hora",
    y="promedio_alquileres",
    x_label="Hora del día",
    y_label="Alquileres por hora observada",
    color=color_barras
)

if st.checkbox("Mostrar tabla de promedios"):
    tabla_fmt = prom_horas.copy()
    tabla_fmt["promedio_alquileres"] = tabla_fmt["promedio_alquileres"].round(2)
    st.dataframe(tabla_fmt, use_container_width=True)

st.divider()

limite = st.number_input("Límite de alquileres por hora", min_value=0, value=250, step=10)

superan = prom_horas[prom_horas["promedio_alquileres"] > limite]
total_horas_datos = len(prom_horas)
cant_superan = len(superan)

st.metric("Horarios con promedio mayor que el límite", f"{cant_superan}/{total_horas_datos}")

if cant_superan > 0:
    lista_horas = ", ".join([f"{int(h):02d}:00" for h in superan["hora"]])
    st.write(f"**Horarios:** {lista_horas}.")
else:
    st.write("**Horarios:** Ningún horario supera el límite establecido.")
