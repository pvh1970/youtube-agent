import requests
import os

def summarize_text(text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"Oppsummer følgende innhold kort og presist:\n\n{text}"

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200
        }
    )

    return response.json()["choices"][0]["message"]["content"]
