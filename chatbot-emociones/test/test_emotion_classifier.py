import json
import pytest
from src.models.emotion_classifier import EmotionClassifier

class Dummy:
    @staticmethod
    def create(*args, **kwargs):
        class R: 
            choices = [type("C", (), {"message": type("M", (), {"content": json.dumps({"label":"positive","explanation":"OK"})})})()]
        return R()

@pytest.fixture(autouse=True)
def patch_llm(monkeypatch):
    import src.services.llm_client as client_mod
    monkeypatch.setattr(client_mod, "client", type("C", (), {"chat": type("CC", (), {"completions": Dummy})()}))

def test_positive():
    out = EmotionClassifier().classify("¡Me encanta!")
    assert out["label"] == "positive"
