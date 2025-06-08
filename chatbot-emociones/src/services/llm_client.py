import os
from together import Together
from ..config import settings

_SYSTEM_PROMPT = (
    "Eres un analista de sentimientos. Devuelve JSON con "
    "`label` (positive|negative|neutral) y `explanation` breve."
)

client = Together(api_key=settings.togetherai_api_key)

def ask_llm(text: str) -> dict:
    resp = client.chat.completions.create(
        model=settings.model_name,          # "lgai/exaone-3-5-32b-instruct"
        temperature=settings.temperature,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user",   "content": text},
        ],
    )
    # resp.choices[0].message.content ya es un JSON serializado
    return resp.choices[0].message.content

