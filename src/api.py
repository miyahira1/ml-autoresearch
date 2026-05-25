import json
import re

from anthropic import Anthropic

from .constants import MAX_TOKENS, MODEL, SYSTEM_PROMPT


def analyze_niche(client: Anthropic, nicho: str) -> dict | None:
    user_message = (
        f'Analiza el nicho "{nicho}" para Mercado Libre Argentina. '
        f"Considera el contexto económico actual de Argentina. "
        f"Devuelve SOLO el JSON, sin texto adicional."
    )

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        text = response.content[0].text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return json.loads(text)
    except Exception:
        return None
