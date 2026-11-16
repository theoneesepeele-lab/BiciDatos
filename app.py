import streamlit as st

st.set_page_config(
    page_title="BiciDatos | Análisis de Alquileres",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar variables de estado compartido (R1, R2, R3)
if "df" not in st.session_state:
    st.session_state["df"] = None
if "tipo_usuario" not in st.session_state:
    st.session_state["tipo_usuario"] = "Todos"
if "tipo_dia" not in st.session_state:
    st.session_state["tipo_dia"] = "Todos"
if "horas" not in st.session_state:
    st.session_state["horas"] = (0, 23)

# Barra lateral estilizada con los 3 filtros compartidos (R3)
with st.sidebar:
    st.markdown("## 🚲 BiciDatos")
    st.caption("Panel de exploración de demanda horaria (Capital Bikeshare 2011–2012)")
    st.divider()
    
    st.subheader("Filtros globales")
    
    st.session_state["tipo_usuario"] = st.selectbox(
        "Tipo de usuario",
        options=["Todos", "Ocasionales", "Registrados"],
        index=["Todos", "Ocasionales", "Registrados"].index(st.session_state["tipo_usuario"]),
        help="Selecciona el segmento de usuarios para recalcular métricas y gráficos."
    )
    
    st.session_state["tipo_dia"] = st.radio(
        "Tipo de día",
        options=["Todos", "Laborable", "No laborable"],
        index=["Todos", "Laborable", "No laborable"].index(st.session_state["tipo_dia"]),
        help="Filtra por jornadas laborales o fines de semana/feriados."
    )
    
    st.session_state["horas"] = st.slider(
        "Horas del día",
        min_value=0,
        max_value=23,
        value=st.session_state["horas"],
        help="Selecciona el rango horario (extremos incluidos)."
    )
    
    st.divider()
    if st.session_state["df"] is not None:
        st.success(f"Base activa: {len(st.session_state['df']):,} registros".replace(",", "."))
    else:
        st.warning("Base de datos pendiente de carga")

# Configuración de navegación multipágina (R2)
pag_explorar = st.Page("explorar.py", title="Explorar los datos", icon="📊", default=True)
pag_comparar = st.Page("comparar.py", title="Comparar horarios", icon="⏰")

pg = st.navigation([pag_explorar, pag_comparar])
pg.run()
