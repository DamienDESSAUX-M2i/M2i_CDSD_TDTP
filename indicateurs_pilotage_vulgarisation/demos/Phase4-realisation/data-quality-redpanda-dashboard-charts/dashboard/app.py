import json
import os
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

METRICS_FILE = os.getenv("METRICS_FILE", "/metrics/metrics.json")

st.set_page_config(
    page_title="Dashboard Qualité des Données",
    layout="wide"
)

st.title("Dashboard Qualité des Données")
st.caption("Monitoring temps réel : Kafka / Redpanda → Analyse qualité → Dashboard")


def load_metrics():
    if not os.path.exists(METRICS_FILE):
        return None

    with open(METRICS_FILE, "r") as f:
        return json.load(f)


def status_icon(status):
    return "OK" if status == "OK" else "KO"


metrics = load_metrics()

if metrics is None:
    st.warning("En attente des premières métriques...")
    time.sleep(3)
    st.rerun()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Nombre de lignes", metrics["total_rows"])
col2.metric(
    "Complétude",
    f"{metrics['completeness_rate']} %",
    status_icon(metrics["status"]["completeness"])
)
col3.metric(
    "Doublons",
    f"{metrics['duplicate_rate']} %",
    status_icon(metrics["status"]["duplicates"])
)
col4.metric(
    "Erreurs",
    f"{metrics['error_rate']} %",
    status_icon(metrics["status"]["errors"])
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("KPI vs cibles")

    kpi_df = pd.DataFrame([
        {
            "KPI": "Complétude",
            "Valeur": metrics["completeness_rate"],
            "Cible": metrics["targets"]["completeness"]
        },
        {
            "KPI": "Doublons",
            "Valeur": metrics["duplicate_rate"],
            "Cible": metrics["targets"]["duplicates"]
        },
        {
            "KPI": "Erreurs",
            "Valeur": metrics["error_rate"],
            "Cible": metrics["targets"]["errors"]
        }
    ])

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=kpi_df["KPI"],
        y=kpi_df["Valeur"],
        name="Valeur actuelle"
    ))

    fig.add_trace(go.Scatter(
        x=kpi_df["KPI"],
        y=kpi_df["Cible"],
        mode="markers+lines",
        name="Cible"
    ))

    fig.update_layout(
        yaxis_title="Pourcentage",
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Répartition des lignes")

    quality_df = pd.DataFrame([
        {"Type": "Lignes valides", "Nombre": metrics["valid_rows"]},
        {"Type": "Lignes invalides", "Nombre": metrics["error_rows"]},
        {"Type": "Doublons", "Nombre": metrics["duplicate_rows"]}
    ])

    fig = px.pie(
        quality_df,
        names="Type",
        values="Nombre",
        hole=0.55
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)

st.divider()

left2, right2 = st.columns(2)

with left2:
    st.subheader("Évolution des KPI en temps réel")

    history = metrics.get("history", [])

    if len(history) >= 2:
        history_df = pd.DataFrame(history)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=history_df["timestamp"],
            y=history_df["completeness_rate"],
            mode="lines+markers",
            name="Complétude"
        ))

        fig.add_trace(go.Scatter(
            x=history_df["timestamp"],
            y=history_df["duplicate_rate"],
            mode="lines+markers",
            name="Doublons"
        ))

        fig.add_trace(go.Scatter(
            x=history_df["timestamp"],
            y=history_df["error_rate"],
            mode="lines+markers",
            name="Erreurs"
        ))

        fig.update_layout(
            xaxis_title="Temps",
            yaxis_title="Pourcentage",
            height=420
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("En attente de plus de points pour afficher la courbe.")

with right2:
    st.subheader("Types d'erreurs détectées")

    error_types = metrics.get("error_types", {})

    if error_types:
        error_df = pd.DataFrame([
            {"Erreur": key, "Nombre": value}
            for key, value in error_types.items()
        ]).sort_values("Nombre", ascending=True)

        fig = px.bar(
            error_df,
            x="Nombre",
            y="Erreur",
            orientation="h"
        )

        fig.update_layout(height=420)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("Aucune erreur détectée pour le moment.")

st.divider()

with st.expander("Voir les détails techniques JSON"):
    st.json(metrics)

time.sleep(3)
st.rerun()
