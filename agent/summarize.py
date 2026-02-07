import os
import requests

def summarize_text(text: str) -> str:
    text = text[:2000]

    prompt = f"Oppsummer følgende tekst kort og presist:\n\n{text}"

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://github.com",   # kreves av OpenRouter
        "X-Title": "YouTube Agent"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.2
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    try:
        data = response.json()
    except Exception:
        print("OpenRouter rå respons:", response.text[:500])
        return "Kunne ikke oppsummere innholdet."

    print("\n--- OpenRouter RAW RESPONSE ---")
    print(data)
    print("-------------------------------\n")

    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return "Kunne ikke oppsummere innholdet."
