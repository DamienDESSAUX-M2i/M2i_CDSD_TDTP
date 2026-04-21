import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

API_URL = os.getenv('API_URL', 'http://api:5000')

st.set_page_config(page_title="ML System", page_icon="🤖", layout="wide")

st.title('Système ML - Wine Quality Prediction')

# Sidebar - Status
st.sidebar.header('Status')
try:
    health = requests.get(f'{API_URL}/health', timeout=5).json()
    st.sidebar.success("API en ligne")
except:
    st.sidebar.error("API hors ligne")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Prédiction", "Entraînement", "Historique", "Modèles"])

# TAB 1: Prédiction
with tab1:
    st.header("Prédire la qualité d'un vin")

    col1, col2 = st.columns(2)

    with col1:
        fixed_acidity = st.slider('Fixed Acidity', 4.0, 16.0, 7.0)
        volatile_acidity = st.slider('Volatile Acidity', 0.0, 2.0, 0.5)
        citric_acid = st.slider('Citric Acid', 0.0, 1.0, 0.3)
        residual_sugar = st.slider('Residual Sugar', 0.0, 16.0, 2.0)
        chlorides = st.slider('Chlorides', 0.0, 0.2, 0.08)
        free_sulfur_dioxide = st.slider('Free SO2', 0.0, 80.0, 15.0)

    with col2:
        total_sulfur_dioxide = st.slider('Total SO2', 0.0, 300.0, 50.0)
        density = st.slider('Density', 0.99, 1.01, 0.996)
        pH = st.slider('pH', 2.5, 4.5, 3.3)
        sulphates = st.slider('Sulphates', 0.0, 2.0, 0.6)
        alcohol = st.slider('Alcohol', 8.0, 15.0, 10.0)

    if st.button('Prédire', type='primary'):
        features = [
            fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
            chlorides, free_sulfur_dioxide, total_sulfur_dioxide,
            density, pH, sulphates, alcohol
        ]

        try:
            response = requests.post(f'{API_URL}/predict', json={'features': features})
            result = response.json()

            if result['success']:
                pred = result['result']
                st.success(f"### Qualité prédite: {pred['prediction']}/10")
                st.metric("Confiance", f"{pred['confidence']:.1%}")
            else:
                st.error(result['error'])
        except Exception as e:
            st.error(f"Erreur: {e}")

# TAB 2: Entraînement
with tab2:
    st.header("Entraîner un nouveau modèle")

    n_estimators = st.slider('Nombre d\'arbres', 10, 500, 100, step=10)

    if st.button('Lancer l\'entraînement', type='primary'):
        with st.spinner('Entraînement en cours...'):
            try:
                response = requests.post(f'{API_URL}/train', json={'n_estimators': n_estimators})
                result = response.json()

                if result['success']:
                    st.success('Entraînement terminé!')
                    res = result['result']
                    col1, col2, col3 = st.columns(3)
                    col1.metric('Accuracy', f"{res['accuracy']:.2%}")
                    col2.metric('Échantillons', res['n_samples'])
                    col3.metric('Features', res['n_features'])
                else:
                    st.error(result['error'])
            except Exception as e:
                st.error(f"Erreur: {e}")

# TAB 3: Historique
with tab3:
    st.header("Historique")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Entraînements")
        try:
            response = requests.get(f'{API_URL}/history/training')
            result = response.json()

            if result['success']:
                df = pd.DataFrame(result['runs'])
                if not df.empty:
                    st.dataframe(df, use_container_width=True)

                    fig = px.line(df, x='timestamp', y='accuracy',
                                 title='Évolution de l\'accuracy')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aucun entraînement")
        except Exception as e:
            st.error(f"Erreur: {e}")

    with col2:
        st.subheader("Prédictions")
        try:
            response = requests.get(f'{API_URL}/history/predictions')
            result = response.json()

            if result['success']:
                df = pd.DataFrame(result['predictions'])
                if not df.empty:
                    st.dataframe(df, use_container_width=True)

                    fig = px.histogram(df, x='prediction',
                                      title='Distribution des prédictions')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aucune prédiction")
        except Exception as e:
            st.error(f"Erreur: {e}")

# TAB 4: Modèles
with tab4:
    st.header("Modèles disponibles")

    try:
        response = requests.get(f'{API_URL}/models')
        result = response.json()

        if result['success']:
            models = result['models']
            st.metric("Nombre de modèles", len(models))

            for model in models:
                st.code(model)
        else:
            st.error(result['error'])
    except Exception as e:
        st.error(f"Erreur: {e}")