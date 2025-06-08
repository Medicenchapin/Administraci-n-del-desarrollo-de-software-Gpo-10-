import os
from together import Together
from ..config import settings

_SYSTEM_PROMPT = (
    "Eres un analista de sentimientos. Responde ÚNICAMENTE con un JSON válido, "
    "sin texto adicional ni bloques markdown. El JSON debe tener:\n"
    "- label: positive | negative | neutral\n"
    "- explanation: frase breve en español"
)




client = Together(api_key=settings.togetherai_api_key)

def ask_llm(text: str) -> str:
    resp = client.chat.completions.create(
        model=settings.model_name,
        temperature=settings.temperature,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user",   "content": text},
        ],
    )
    return resp.choices[0].message.content

