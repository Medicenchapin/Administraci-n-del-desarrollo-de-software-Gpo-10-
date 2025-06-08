import sys, os

# Inserta la carpeta raíz (una arriba de app/) en la lista de paths de Python:
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
import streamlit as st
from src.models.emotion_classifier import EmotionClassifier

st.title("Analizador de emociones")
text = st.text_area("Escribe un texto:")
if st.button("Analizar") and text:
    result = EmotionClassifier().classify(text)
    st.success(f"Emoción: {result['label']}")
    st.write(result["explanation"])
