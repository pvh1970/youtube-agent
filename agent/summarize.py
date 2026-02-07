import os
import requests

HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
HF_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

def summarize_text(text: str) -> str:
    text = text[:2000]

    prompt = f"Oppsummer følgende tekst kort og presist:\n\n{text}"

    headers = {
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.2
        }
    }

    response = requests.post(HF_URL, headers=headers, json=payload)

    # Hvis API-et returnerer HTML eller tomt svar
    if not response.text.strip():
        print("HF tom respons:", response.status_code)
        return "Kunne ikke oppsummere innholdet."

    try:
        data = response.json()
    except Exception as e:
        print("HF JSON-feil:", e)
        print("Rå respons:", response.text[:500])
        return "Kunne ikke oppsummere innholdet."

    print("\n--- HF RAW RESPONSE ---")
    print(data)
    print("-----------------------\n")

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]

    return "Kunne ikke oppsummere innholdet."
