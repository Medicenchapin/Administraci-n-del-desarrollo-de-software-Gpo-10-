import streamlit as st
from src.models.emotion_classifier import EmotionClassifier

st.title("Analizador de emociones")
text = st.text_area("Escribe un texto:")
if st.button("Analizar") and text:
    result = EmotionClassifier().classify(text)
    st.success(f"Emoción: {result['label']}")
    st.write(result["explanation"])
