import requests

HF_MODEL = "facebook/bart-large-cnn"
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

def summarize_text(text: str) -> str:
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 150,
            "min_length": 40,
            "do_sample": False
        }
    }

    response = requests.post(HF_URL, json=payload)
    data = response.json()

    # HuggingFace returnerer en liste med dicts
    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]

    # fallback
    return "Kunne ikke oppsummere innholdet."

