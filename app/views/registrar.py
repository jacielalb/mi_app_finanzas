import streamlit as st
from database import supabase
from datetime import date

def show():
    st.title("Registrar movimiento")

    categorias_res = supabase.table("categorias").select("*").execute()
    categorias = categorias_res.data

    with st.form("form_movimiento"):
        col1, col2 = st.columns(2)

        with col1:
            fecha = st.date_input("Fecha", value=date.today())
            tipo = st.selectbox("Tipo", ["ingreso", "gasto"])
            monto = st.number_input("Monto", min_value=0.01, step=0.01, format="%.2f")

        with col2:
            concepto = st.text_input("Concepto")
            cats_filtradas = [c for c in categorias if c["tipo"] == tipo]
            cat_nombres = {c["nombre"]: c["id"] for c in cats_filtradas}
            cat_seleccionada = st.selectbox("Categoria", list(cat_nombres.keys()))
            descripcion = st.text_area("Descripcion (opcional)", height=100)

        submitted = st.form_submit_button("Guardar", use_container_width=True)

        if submitted:
            if not concepto:
                st.error("El concepto es obligatorio.")
            else:
                nuevo = {
                    "fecha": str(fecha),
                    "concepto": concepto,
                    "tipo": tipo,
                    "monto": monto,
                    "categoria_id": cat_nombres[cat_seleccionada],
                    "descripcion": descripcion,
                }
                res = supabase.table("movimientos").insert(nuevo).execute()
                if res.data:
                    st.success("Movimiento registrado correctamente.")
                    st.rerun()
                else:
                    st.error("Error al guardar. Intenta de nuevo.")
