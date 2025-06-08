import json
from ..services.llm_client import ask_llm

class EmotionClassifier:
    LABELS = {"positive","negative","neutral"}

    def classify(self, text: str) -> dict:
        raw = ask_llm(text)
        try:
            data = json.loads(raw)
            label = data.get("label","").lower()
            if label not in self.LABELS:
                raise ValueError(f"Etiqueta inesperada: {label}")
            return {"label": label, "explanation": data.get("explanation","")}
        except Exception as e:
            return {"label": "neutral", "explanation": f"Error: {e}"}
