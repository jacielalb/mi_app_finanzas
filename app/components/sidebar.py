import os
import streamlit as st

def render_sidebar():
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
    st.sidebar.image(logo_path, use_container_width=True)
    st.sidebar.title("Menú")

    menu = st.sidebar.radio(
        "Navegación",
        ["Dashboard", "Registros", "Registrar"]
    )

    return menu