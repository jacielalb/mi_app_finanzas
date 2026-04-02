import streamlit as st
import pandas as pd
from database import supabase

def show():
    st.title("Registros")

    res = supabase.table("movimientos").select(
        "id, fecha, concepto, tipo, monto, descripcion, categorias(nombre)"
    ).order("fecha", desc=True).execute()

    if not res.data:
        st.info("No hay movimientos registrados.")
        return

    df = pd.DataFrame(res.data)
    df["categoria"] = df["categorias"].apply(lambda x: x["nombre"] if x else "—")
    df = df.drop(columns=["categorias"])
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        tipo_filtro = st.selectbox("Tipo", ["Todos", "ingreso", "gasto"])
    with col2:
        categorias_lista = ["Todas"] + sorted(df["categoria"].unique().tolist())
        cat_filtro = st.selectbox("Categoria", categorias_lista)
    with col3:
        busqueda = st.text_input("Buscar concepto")

    df_filtrado = df.copy()
    if tipo_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["tipo"] == tipo_filtro]
    if cat_filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado["categoria"] == cat_filtro]
    if busqueda:
        df_filtrado = df_filtrado[df_filtrado["concepto"].str.contains(busqueda, case=False)]

    st.markdown(f"**{len(df_filtrado)} registros encontrados**")

    st.dataframe(
        df_filtrado[["fecha", "concepto", "tipo", "categoria", "monto", "descripcion"]],
        use_container_width=True,
        column_config={
            "fecha": "Fecha",
            "concepto": "Concepto",
            "tipo": "Tipo",
            "categoria": "Categoria",
            "monto": st.column_config.NumberColumn("Monto", format="$%.2f"),
            "descripcion": "Descripcion",
        },
        hide_index=True,
    )
