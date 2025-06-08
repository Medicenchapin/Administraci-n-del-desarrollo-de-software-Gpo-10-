import os
from together import Together
from ..config import settings

_SYSTEM_PROMPT = (
    "Eres un analista de sentimientos. Devuelve JSON con "
    "`label` (positive|negative|neutral) y `explanation` breve."
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

