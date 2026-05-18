import json
import os
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

METRICS_FILE = os.getenv("METRICS_FILE", "/metrics/model_metrics.json")

st.set_page_config(
    page_title="KPIs de Performance Modèle",
    layout="wide"
)

st.title("KPIs de Performance Modèle")
st.caption("Simulation pédagogique : classification, régression et clustering")


def load_metrics():
    if not os.path.exists(METRICS_FILE):
        return None

    with open(METRICS_FILE, "r") as f:
        return json.load(f)


data = load_metrics()

if data is None:
    st.warning("En attente des premières métriques...")
    time.sleep(3)
    st.rerun()


st.info(f"Dernière simulation : {data['timestamp']}")

summary_df = pd.DataFrame([
    {
        "Type de problème": data["balanced_classification"]["problem_type"],
        "KPIs pertinents": ", ".join(data["balanced_classification"]["recommended_kpis"]),
        "Quand les choisir": data["balanced_classification"]["when_to_choose"],
    },
    {
        "Type de problème": data["imbalanced_classification"]["problem_type"],
        "KPIs pertinents": ", ".join(data["imbalanced_classification"]["recommended_kpis"]),
        "Quand les choisir": data["imbalanced_classification"]["when_to_choose"],
    },
    {
        "Type de problème": data["regression"]["problem_type"],
        "KPIs pertinents": ", ".join(data["regression"]["recommended_kpis"]),
        "Quand les choisir": data["regression"]["when_to_choose"],
    },
    {
        "Type de problème": data["clustering"]["problem_type"],
        "KPIs pertinents": ", ".join(data["clustering"]["recommended_kpis"]),
        "Quand les choisir": data["clustering"]["when_to_choose"],
    },
])

st.subheader("Table de décision pédagogique")
st.dataframe(summary_df, use_container_width=True)

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Classification équilibrée",
    "Classification déséquilibrée",
    "Régression",
    "Clustering",
    "Vue globale"
])


with tab1:
    model = data["balanced_classification"]
    m = model["metrics"]

    st.subheader("Classification équilibrée")
    st.write(model["interpretation"])

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Accuracy", m["accuracy"])
    c2.metric("Precision", m["precision"])
    c3.metric("Recall", m["recall"])
    c4.metric("F1-score", m["f1_score"])
    c5.metric("AUC-ROC", m["auc_roc"])

    metric_df = pd.DataFrame([
        {"KPI": key, "Valeur": value}
        for key, value in m.items()
    ])

    fig = px.bar(metric_df, x="KPI", y="Valeur", range_y=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

    cm = model["confusion_matrix"]
    cm_df = pd.DataFrame(cm, index=["Réel 0", "Réel 1"], columns=["Prédit 0", "Prédit 1"])

    fig = px.imshow(cm_df, text_auto=True, aspect="auto")
    st.plotly_chart(fig, use_container_width=True)


with tab2:
    model = data["imbalanced_classification"]
    m = model["metrics"]

    st.subheader("Classification déséquilibrée")
    st.write(model["interpretation"])

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Accuracy", m["accuracy"])
    c2.metric("Precision", m["precision"])
    c3.metric("Recall", m["recall"])
    c4.metric("F1-score", m["f1_score"])
    c5.metric("AUC-ROC", m["auc_roc"])

    metric_df = pd.DataFrame([
        {"KPI": key, "Valeur": value}
        for key, value in m.items()
    ])

    fig = px.bar(metric_df, x="KPI", y="Valeur", range_y=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

    cm = model["confusion_matrix"]
    cm_df = pd.DataFrame(cm, index=["Réel 0", "Réel 1"], columns=["Prédit 0", "Prédit 1"])

    fig = px.imshow(cm_df, text_auto=True, aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

    st.warning(
        "Point pédagogique : une accuracy élevée peut cacher un mauvais recall "
        "sur la classe minoritaire."
    )


with tab3:
    model = data["regression"]
    m = model["metrics"]

    st.subheader("Régression")
    st.write(model["interpretation"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("RMSE", m["rmse"])
    c2.metric("MAE", m["mae"])
    c3.metric("MAPE", f"{m['mape']} %")
    c4.metric("R²", m["r2"])

    pred_df = pd.DataFrame(model["sample_predictions"])

    fig = px.scatter(
        pred_df,
        x="real",
        y="predicted",
        size="error",
        labels={
            "real": "Valeur réelle",
            "predicted": "Valeur prédite",
            "error": "Erreur absolue"
        }
    )
    fig.add_trace(go.Scatter(
        x=pred_df["real"],
        y=pred_df["real"],
        mode="lines",
        name="Prédiction parfaite"
    ))
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        pred_df,
        x=pred_df.index,
        y="error",
        labels={"x": "Observation", "error": "Erreur absolue"}
    )
    st.plotly_chart(fig, use_container_width=True)


with tab4:
    model = data["clustering"]
    m = model["metrics"]

    st.subheader("Clustering")
    st.write(model["interpretation"])

    c1, c2 = st.columns(2)
    c1.metric("Silhouette", m["silhouette"])
    c2.metric("Davies-Bouldin", m["davies_bouldin"])

    cluster_df = pd.DataFrame(model["cluster_points"])

    fig = px.scatter(
        cluster_df,
        x="x",
        y="y",
        color="cluster",
        title="Visualisation des clusters simulés"
    )
    st.plotly_chart(fig, use_container_width=True)


with tab5:
    st.subheader("Vue globale des performances")

    history = pd.DataFrame(data["history"])

    if len(history) > 1:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=history["timestamp"],
            y=history["balanced_accuracy"],
            mode="lines+markers",
            name="Accuracy classification équilibrée"
        ))

        fig.add_trace(go.Scatter(
            x=history["timestamp"],
            y=history["imbalanced_f1"],
            mode="lines+markers",
            name="F1 classification déséquilibrée"
        ))

        fig.add_trace(go.Scatter(
            x=history["timestamp"],
            y=history["regression_r2"],
            mode="lines+markers",
            name="R² régression"
        ))

        fig.add_trace(go.Scatter(
            x=history["timestamp"],
            y=history["clustering_silhouette"],
            mode="lines+markers",
            name="Silhouette clustering"
        ))

        fig.update_layout(
            yaxis_title="Score",
            xaxis_title="Temps",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("En attente d'historique supplémentaire.")

    with st.expander("Voir le JSON complet"):
        st.json(data)


time.sleep(5)
st.rerun()
