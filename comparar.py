import streamlit as st
import pandas as pd

st.title("⏰ Comparar horarios")
st.markdown("Analiza el promedio histórico de alquileres por hora del día e identifica las franjas que superan el umbral definido.")

if st.session_state["df"] is None:
    st.info("👈 Primero debes cargar el archivo CSV en la página **Explorar los datos**.")
    st.stop()

df = st.session_state["df"].copy()

# Aplicar filtros compartidos (R3)
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

# Calcular promedios horarios (R6)
prom_horas = df_filtrado.groupby("hora", as_index=False)[col_activa].mean()
prom_horas.rename(columns={col_activa: "promedio_alquileres"}, inplace=True)

# Controles superiores y gráfico de barras (R6)
with st.container(border=True):
    col_color, col_check = st.columns([1, 2])
    with col_color:
        color_barras = st.color_picker("Color de las barras", "#197A8D")
    with col_check:
        st.markdown("<br>", unsafe_allow_html=True)
        mostrar_tabla = st.checkbox("Mostrar tabla de promedios")

    st.bar_chart(
        prom_horas,
        x="hora",
        y="promedio_alquileres",
        x_label="Hora del día",
        y_label="Alquileres por hora observada",
        color=color_barras,
        height=400
    )

    if mostrar_tabla:
        tabla_fmt = prom_horas.copy()
        tabla_fmt["hora_formateada"] = tabla_fmt["hora"].apply(lambda h: f"{int(h):02d}:00")
        tabla_fmt["promedio_alquileres"] = tabla_fmt["promedio_alquileres"].round(2)
        st.dataframe(
            tabla_fmt[["hora", "hora_formateada", "promedio_alquileres"]],
            use_container_width=True,
            hide_index=True
        )

# Evaluación contra el límite de alquileres (R7)
st.subheader("Evaluación de demanda pico")
with st.container(border=True):
    col_lim, col_res = st.columns([1, 2])
    
    with col_lim:
        limite = st.number_input(
            "Límite de alquileres por hora",
            min_value=0,
            value=250,
            step=10
        )
        
    superan = prom_horas[prom_horas["promedio_alquileres"] > limite]
    total_horas_datos = len(prom_horas)
    cant_superan = len(superan)
    
    with col_res:
        st.metric(
            label="Horarios con promedio mayor que el límite",
            value=f"{cant_superan}/{total_horas_datos}"
        )
        
        if cant_superan > 0:
            lista_horas = ", ".join([f"{int(h):02d}:00" for h in superan["hora"]])
            st.success(f"**Horarios:** {lista_horas}.")
        else:
            st.warning("**Horarios:** Ningún horario supera el límite establecido.")
