import os
import streamlit as st
from auth import logout, is_admin, is_editor


def render_sidebar():
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
    st.sidebar.image(logo_path, use_container_width=True)

    # Info del usuario
    user_name = st.session_state.get("user_name", "Usuario")
    roles = st.session_state.get("roles", [])
    roles_str = ", ".join(roles) if roles else "sin rol"
    st.sidebar.markdown(f"**{user_name}**")
    st.sidebar.caption(f"Rol: {roles_str}")
    st.sidebar.divider()

    # Menú según rol
    opciones = ["Dashboard", "Registros"]
    if is_editor():
        opciones.append("Registrar")
    if is_admin():
        opciones.append("Administración")

    st.sidebar.title("Menú")
    menu = st.sidebar.radio("Navegación", opciones, label_visibility="collapsed")

    st.sidebar.divider()
    if st.sidebar.button("Cerrar sesión", use_container_width=True):
        logout()
        st.rerun()

    return menu
