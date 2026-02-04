import requests

HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
HF_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

def summarize_text(text: str) -> str:
    # Trunkér tekst for å unngå modellkrasj
    text = text[:2000]

    prompt = f"Oppsummer følgende tekst kort og presist:\n\n{text}"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.2
        }
    }

    response = requests.post(HF_URL, json=payload)
    data = response.json()

    # DEBUG: print hele responsen
    print("\n--- HF RAW RESPONSE ---")
    print(data)
    print("-----------------------\n")

    # Mistral returnerer en liste med dicts
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    # Noen ganger returnerer router direkte dict
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]

    return "Kunne ikke oppsummere innholdet."
