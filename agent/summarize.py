import requests

HF_MODEL = "facebook/bart-large-cnn"
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

def summarize_text(text: str) -> str:
    # Trunkér tekst for å unngå modellkrasj
    text = text[:2000]

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 150,
            "min_length": 40,
            "do_sample": False
        }
    }

    response = requests.post(HF_URL, json=payload)

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

    # BART returnerer en liste med dicts
    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]

    return "Kunne ikke oppsummere innholdet."
