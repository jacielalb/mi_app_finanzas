import streamlit as st

def render_sidebar():
    st.sidebar.image("app/assets/logo.png", use_container_width=True)
    st.sidebar.title("Menú")

    menu = st.sidebar.radio(
        "Navegación",
        ["Dashboard", "Registros", "Registrar"]
    )

    return menu