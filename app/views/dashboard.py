import streamlit as st
import pandas as pd
import altair as alt
from database import supabase

def show():
    st.title("Dashboard")

    res = supabase.table("movimientos").select(
        "fecha, tipo, monto, categorias(nombre)"
    ).execute()

    if not res.data:
        st.info("No hay movimientos registrados.")
        return

    df = pd.DataFrame(res.data)
    df["categoria"] = df["categorias"].apply(lambda x: x["nombre"] if x else "—")
    df = df.drop(columns=["categorias"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["monto"] = df["monto"].astype(float)

    ingresos = df[df["tipo"] == "ingreso"]["monto"].sum()
    gastos = df[df["tipo"] == "gasto"]["monto"].sum()
    balance = ingresos - gastos

    # Metricas principales
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos totales", f"${ingresos:,.2f}")
    col2.metric("Gastos totales", f"${gastos:,.2f}")
    col3.metric("Balance", f"${balance:,.2f}", delta=f"${balance:,.2f}")

    st.divider()

    col_a, col_b = st.columns(2)

    # Grafica gastos por categoria
    with col_a:
        st.subheader("Gastos por categoria")
        gastos_cat = (
            df[df["tipo"] == "gasto"]
            .groupby("categoria")["monto"]
            .sum()
            .reset_index()
            .sort_values("monto", ascending=False)
        )
        if not gastos_cat.empty:
            chart = alt.Chart(gastos_cat).mark_bar().encode(
                x=alt.X("monto:Q", title="Monto ($)"),
                y=alt.Y("categoria:N", sort="-x", title=""),
                color=alt.value("#e05c5c"),
                tooltip=["categoria", alt.Tooltip("monto:Q", format="$,.2f")]
            ).properties(height=280)
            st.altair_chart(chart, use_container_width=True)

    # Grafica ingresos por categoria
    with col_b:
        st.subheader("Ingresos por categoria")
        ingresos_cat = (
            df[df["tipo"] == "ingreso"]
            .groupby("categoria")["monto"]
            .sum()
            .reset_index()
            .sort_values("monto", ascending=False)
        )
        if not ingresos_cat.empty:
            chart2 = alt.Chart(ingresos_cat).mark_bar().encode(
                x=alt.X("monto:Q", title="Monto ($)"),
                y=alt.Y("categoria:N", sort="-x", title=""),
                color=alt.value("#4caf82"),
                tooltip=["categoria", alt.Tooltip("monto:Q", format="$,.2f")]
            ).properties(height=280)
            st.altair_chart(chart2, use_container_width=True)

    # Evolucion temporal
    st.subheader("Evolucion por mes")
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    evolucion = df.groupby(["mes", "tipo"])["monto"].sum().reset_index()

    if not evolucion.empty:
        line = alt.Chart(evolucion).mark_line(point=True).encode(
            x=alt.X("mes:N", title="Mes"),
            y=alt.Y("monto:Q", title="Monto ($)"),
            color=alt.Color("tipo:N", scale=alt.Scale(
                domain=["ingreso", "gasto"],
                range=["#4caf82", "#e05c5c"]
            )),
            tooltip=["mes", "tipo", alt.Tooltip("monto:Q", format="$,.2f")]
        ).properties(height=250)
        st.altair_chart(line, use_container_width=True)
