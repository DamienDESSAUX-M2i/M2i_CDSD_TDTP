import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="NLP Suite", page_icon="🤖", layout="wide")

st.title("Suite NLP Multi-Tâches")

model_summarizer = "facebook/bart-large-cnn"
model_translator = "Helsinki-NLP/opus-mt-en-fr"
model_classifier = "j-hartmann/emotion-english-distilroberta-base"


@st.cache_resource
def load_models():
    summarizer = pipeline("summarization", model=model_summarizer)
    translator = pipeline("translation_en_to_fr", model=model_translator)
    emotion_classifier = pipeline("text-classification", model=model_classifier)
    return summarizer, translator, emotion_classifier


summarizer, translator, emotion_classifier = load_models()

tab1, tab2, tab3 = st.tabs(["📝 Résumé", "🌍 Traduction", "😊 Émotions"])

with tab1:
    st.subheader("Résumé de texte")
    input_text = st.text_area("Entrez un texte long :", height=200)

    if st.button("Résumer"):
        if input_text.strip():
            with st.spinner("Génération du résumé..."):
                summary = summarizer(
                    input_text,
                    max_length=130,
                    min_length=30,
                    do_sample=False,
                )
                st.success("Résumé :")
                st.write(summary[0]["summary_text"])
        else:
            st.warning("Veuillez entrer un texte.")

with tab2:
    st.subheader("Traduction Anglais → Français")
    input_text_trans = st.text_area("Entrez un texte en anglais :", height=200)

    if st.button("Traduire"):
        if input_text_trans.strip():
            with st.spinner("Traduction en cours..."):
                translation = translator(input_text_trans)
                st.success("Traduction :")
                st.write(translation[0]["translation_text"])
        else:
            st.warning("Veuillez entrer un texte.")

with tab3:
    st.subheader("Analyse d'émotions")
    input_text_emotion = st.text_input("Entrez une phrase :")

    if st.button("Analyser"):
        if input_text_emotion.strip():
            with st.spinner("Analyse en cours..."):
                result = emotion_classifier(input_text_emotion)
                st.success("Émotion détectée :")
                st.write(f"{result[0]['label']} (score: {result[0]['score']:.2f})")
        else:
            st.warning("Veuillez entrer une phrase.")
