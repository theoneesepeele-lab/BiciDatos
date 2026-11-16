import streamlit as st
import pandas as pd

col_titulo, col_img = st.columns([5, 1])

with col_titulo:
    st.title("📊 Explorar los datos")
    st.markdown("Carga el archivo preparado para analizar la evolución diaria, el comportamiento por día de la semana y descargar registros filtrados.")

with col_img:
    st.image("bici.jpg", width=110)

# Sección de carga en contenedor con borde (R1)
with st.container(border=True):
    st.subheader("1. Carga del conjunto de datos")
    archivo = st.file_uploader("Selecciona bicicletas_listas.csv", type=["csv"])
    
    col_btn, col_msg = st.columns([1, 3])
    with col_btn:
        cargar = st.button("Cargar datos", type="primary", use_container_width=True)
        
    if cargar:
        if archivo is not None:
            df_leido = pd.read_csv(archivo, parse_dates=["fecha"], encoding="utf-8-sig")
            st.session_state["df"] = df_leido
        else:
            with col_msg:
                st.warning("Selecciona primero el archivo bicicletas_listas.csv antes de presionar Cargar datos.")

if st.session_state["df"] is None:
    st.info("👋 Para comenzar, sube el archivo **bicicletas_listas.csv** arriba y haz clic en **Cargar datos**.")
    st.stop()

df = st.session_state["df"].copy()
st.success(f"{len(df):,} registros cargados.")

# Aplicar filtros compartidos desde st.session_state (R3)
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

# Indicadores principales (R4)
st.subheader("2. Indicadores clave")
total_alq = int(df_filtrado[col_activa].sum())
prom_hora = df_filtrado[col_activa].mean() if len(df_filtrado) > 0 else 0.0
registros_activos = len(df_filtrado)

m1, m2, m3 = st.columns(3)
with m1:
    with st.container(border=True):
        st.metric("Total de alquileres", f"{total_alq:,}".replace(",", "."))
with m2:
    with st.container(border=True):
        st.metric("Promedio por hora observada", f"{prom_hora:,.1f}".replace(".", ","))
with m3:
    with st.container(border=True):
        st.metric("Horas observadas (registros)", f"{registros_activos:,}".replace(",", "."))

st.markdown("")

# Pestañas de exploración (R2 + pestaña extra de análisis semanal)
tab1, tab2, tab3 = st.tabs(["📈 Gráfico diario", "📅 Demanda por día de semana", "🗂️ Datos y descarga"])

with tab1:
    st.markdown("#### Evolución de alquileres totales por día")
    st.caption("Cada punto suma las horas seleccionadas en los filtros para esa fecha.")
    
    diario = df_filtrado.groupby("fecha", as_index=False)[col_activa].sum()
    st.line_chart(
        diario,
        x="fecha",
        y=col_activa,
        x_label="Fecha",
        y_label="Alquileres por día",
        color="#197A8D",
        height=400
    )

with tab2:
    st.markdown("#### Alquileres totales y promedio por día de la semana")
    st.caption("Permite identificar qué días de la semana concentran mayor demanda según los filtros activos.")
    
    orden_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    por_dia = df_filtrado.groupby("dia_semana", as_index=False).agg(
        total_alquileres=(col_activa, "sum"),
        promedio_horario=(col_activa, "mean")
    )
    por_dia["dia_semana"] = pd.Categorical(por_dia["dia_semana"], categories=orden_dias, ordered=True)
    por_dia = por_dia.sort_values("dia_semana")
    
    c_graf, c_tab = st.columns([2, 1])
    with c_graf:
        st.bar_chart(
            por_dia,
            x="dia_semana",
            y="total_alquileres",
            x_label="Día de la semana",
            y_label="Total de alquileres",
            color="#197A8D",
            height=360
        )
    with c_tab:
        por_dia_fmt = por_dia.copy()
        por_dia_fmt["promedio_horario"] = por_dia_fmt["promedio_horario"].round(1)
        st.dataframe(por_dia_fmt, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("#### Registros filtrados")
    df_mostrar = df_filtrado.copy()
    df_mostrar["alquileres"] = df_mostrar[col_activa]
    
    st.dataframe(df_mostrar, use_container_width=True, height=350)
    
    col_dl, col_ref = st.columns([1, 2])
    with col_dl:
        csv_descarga = df_mostrar.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="⬇️ Descargar datos filtrados",
            data=csv_descarga,
            file_name="bicicletas_filtradas.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_ref:
        st.link_button(
            "🔗 Consultar la fuente en UCI",
            "https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset",
            use_container_width=True
        )
        
    st.caption(
        "Fanaee-T, H. (2013). Bike Sharing [Conjunto de datos]. UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C5W894. Licencia CC BY 4.0."
    )
