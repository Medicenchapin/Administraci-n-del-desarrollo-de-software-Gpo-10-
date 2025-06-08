import json
from ..services.llm_client import ask_llm


class EmotionClassifier:
    """Envuelve la llamada al modelo y valida la salida JSON."""
    LABELS = {"positive", "negative", "neutral"}

    def _extract_json_block(self, raw: str) -> str:
        """
        Devuelve la sub-cadena que va del primer '{' al último '}'.
        Si no encuentra ambos, lanza ValueError.
        """
        start = raw.find("{")
        end   = raw.rfind("}")
        if start == -1 or end == -1 or end < start:
            raise ValueError("No se encontró bloque JSON en la respuesta")
        return raw[start : end + 1].strip()

    def classify(self, text: str) -> dict:
        raw = ask_llm(text)  # cadena que viene del modelo
        try:
            json_block = self._extract_json_block(raw)
            data = json.loads(json_block)
            label = data.get("label", "").lower()
            if label not in self.LABELS:
                raise ValueError(f"Etiqueta inesperada: {label!r}")
            return {"label": label, "explanation": data.get("explanation", "")}
        except Exception as e:
            # Fallback seguro, nunca propaga la excepción al frontend
            return {"label": "neutral", "explanation": f"Error: {e}"}
        # Si no se puede extraer un JSON válido, devuelve neutral
        return {"label": "neutral", "explanation": "No se pudo analizar la emoción"}

