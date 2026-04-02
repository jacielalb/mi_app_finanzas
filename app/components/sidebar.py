import streamlit as st

def render_sidebar():
    st.sidebar.image("https://via.placeholder.com/150", use_container_width=True)
    st.sidebar.title("Menú")

    menu = st.sidebar.radio(
        "Navegación",
        ["Dashboard", "Registros", "Registrar"]
    )

    return menu