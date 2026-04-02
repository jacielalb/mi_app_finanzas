import streamlit as st
from app.components.sidebar import render_sidebar
from app.pages import dashboard, registros, registrar

st.set_page_config(page_title="App Finanzas", layout="wide")

# Simulación de login (temporal)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Login")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if user == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

if not st.session_state.logged_in:
    login()
else:
    menu = render_sidebar()

    if menu == "Dashboard":
        dashboard.show()

    elif menu == "Registros":
        registros.show()

    elif menu == "Registrar":
        registrar.show()