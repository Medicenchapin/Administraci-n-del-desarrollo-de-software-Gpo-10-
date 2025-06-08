# tests/test_emotion_classifier.py
import json
import pytest
from src.models.emotion_classifier import EmotionClassifier

# ---------- Helper para simular TogetherAI ----------
class FakeLLMResponse:
    """Simula la estructura que devuelve together.chat.completions.create."""
    def __init__(self, label):
        self.choices = [
            type(
                "Choice",
                (),
                {
                    "message": type(
                        "Msg",
                        (),
                        {"content": json.dumps({"label": label, "explanation": "OK"})}
                    )()
                },
            )()
        ]

class FakeChat:
    """Expone .completions.create() para que monkeypatch lo sustituya."""
    class completions:
        @staticmethod
        def create(*args, **kwargs):
            label_map = {
                "¡Me encanta!": "positive",
                "Odio esto.": "negative",
            }
            user_msg = kwargs["messages"][-1]["content"]
            return FakeLLMResponse(label_map.get(user_msg, "neutral"))

# ---------- Fixture que sustituye el cliente real ----------
@pytest.fixture(autouse=True)
def patch_llm(monkeypatch):
    import src.services.llm_client as client_mod
    monkeypatch.setattr(client_mod, "client", type("Client", (), {"chat": FakeChat}))

# ---------- Pruebas ----------
def test_positive():
    assert EmotionClassifier().classify("¡Me encanta!")["label"] == "positive"

def test_negative():
    assert EmotionClassifier().classify("Odio esto.")["label"] == "negative"
