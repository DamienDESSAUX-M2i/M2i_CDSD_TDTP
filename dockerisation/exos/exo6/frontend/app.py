import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://api:5000")

st.set_page_config(page_title="Wine Quality Prediction", page_icon="🍷", layout="wide")

st.title("Système de Prédiction de Qualité du Vin")

# Sidebar - Status
st.sidebar.header("Système")
try:
    health = requests.get(f"{API_URL}/health", timeout=5).json()
    st.sidebar.success(f"API: {health['status']}")
except:
    st.sidebar.error("API: Déconnectée")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["Prédiction", "Entraînement", "Historique", "Métriques"]
)

# TAB 1: Prédiction
with tab1:
    st.header("Prédire la qualité d'un vin")

    col1, col2 = st.columns(2)

    with col1:
        fixed_acidity = st.number_input("Fixed Acidity", value=7.4, step=0.1)
        volatile_acidity = st.number_input("Volatile Acidity", value=0.7, step=0.01)
        citric_acid = st.number_input("Citric Acid", value=0.0, step=0.01)
        residual_sugar = st.number_input("Residual Sugar", value=1.9, step=0.1)
        chlorides = st.number_input("Chlorides", value=0.076, step=0.001)
        free_sulfur_dioxide = st.number_input(
            "Free Sulfur Dioxide", value=11.0, step=1.0
        )

    with col2:
        total_sulfur_dioxide = st.number_input(
            "Total Sulfur Dioxide", value=34.0, step=1.0
        )
        density = st.number_input("Density", value=0.9978, step=0.0001)
        pH = st.number_input("pH", value=3.51, step=0.01)
        sulphates = st.number_input("Sulphates", value=0.56, step=0.01)
        alcohol = st.number_input("Alcohol", value=9.4, step=0.1)

    if st.button("🔮 Prédire", type="primary"):
        payload = {
            "fixed_acidity": fixed_acidity,
            "volatile_acidity": volatile_acidity,
            "citric_acid": citric_acid,
            "residual_sugar": residual_sugar,
            "chlorides": chlorides,
            "free_sulfur_dioxide": free_sulfur_dioxide,
            "total_sulfur_dioxide": total_sulfur_dioxide,
            "density": density,
            "pH": pH,
            "sulphates": sulphates,
            "alcohol": alcohol,
        }

        try:
            response = requests.post(f"{API_URL}/predict", json=payload)
            result = response.json()

            if result.get("success"):
                st.success(f"### Qualité prédite: {result['prediction']}/10")
            else:
                st.error(f"Erreur: {result.get('error')}")
        except Exception as e:
            st.error(f"Erreur de connexion: {e}")

# TAB 2: Entraînement
with tab2:
    st.header("Entraîner un nouveau modèle")

    n_estimators = st.slider("Nombre d'estimateurs", 10, 500, 100, step=10)

    if st.button("Lancer l'entraînement", type="primary"):
        with st.spinner("Entraînement en cours..."):
            try:
                response = requests.post(
                    f"{API_URL}/train", json={"n_estimators": n_estimators}
                )
                result = response.json()

                if result.get("success"):
                    st.success("Entraînement terminé!")
                    st.metric("Précision", f"{result['accuracy']:.2%}")
                    st.metric("Échantillons", result["n_samples"])
                else:
                    st.error(f"Erreur: {result.get('error')}")
            except Exception as e:
                st.error(f"Erreur: {e}")

# TAB 3: Historique
with tab3:
    st.header("Historique des prédictions")

    if st.button("Rafraîchir"):
        try:
            response = requests.get(f"{API_URL}/history")
            result = response.json()

            if result.get("success"):
                predictions = result["predictions"]
                if predictions:
                    df = pd.DataFrame(predictions)
                    st.dataframe(df, use_container_width=True)
                    st.metric("Total de prédictions", len(predictions))
                else:
                    st.info("Aucune prédiction enregistrée")
            else:
                st.error(f"Erreur: {result.get('error')}")
        except Exception as e:
            st.error(f"Erreur: {e}")

# TAB 4: Métriques
with tab4:
    st.header("Métriques d'entraînement")

    try:
        response = requests.get(f"{API_URL}/metrics")
        result = response.json()

        if result.get("success"):
            training_runs = result["training_runs"]
            if training_runs:
                df = pd.DataFrame(training_runs)

                # Graphique de l'évolution de l'accuracy
                fig = px.line(
                    df,
                    x="timestamp",
                    y="accuracy",
                    title="Évolution de la précision",
                    labels={"accuracy": "Précision", "timestamp": "Date"},
                )
                st.plotly_chart(fig, use_container_width=True)

                # Tableau
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Aucun entraînement enregistré")
        else:
            st.error(f"Erreur: {result.get('error')}")
    except Exception as e:
        st.error(f"Erreur: {e}")
