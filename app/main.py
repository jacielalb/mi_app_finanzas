import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from auth import login as auth_login, restore_session
from components.sidebar import render_sidebar
from views import dashboard, registros, registrar, admin

st.set_page_config(page_title="App Finanzas", layout="wide")


def show_login():
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.title("Iniciar sesión")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Ingresar", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("Ingresa tu email y contraseña.")
                else:
                    ok, _ = auth_login(email, password)
                    if ok:
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas. Verifica tu email y contraseña.")


if not st.session_state.get("logged_in"):
    show_login()
else:
    restore_session()
    menu = render_sidebar()

    if menu == "Dashboard":
        dashboard.show()
    elif menu == "Registros":
        registros.show()
    elif menu == "Registrar":
        registrar.show()
    elif menu == "Administración":
        admin.show()
