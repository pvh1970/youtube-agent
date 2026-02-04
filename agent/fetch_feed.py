import os
import json
import requests
from summarize import summarize_text
from notify import send_notification

API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST_ID = "PLsY30fLfDNuLC7gou9-l7GLt5U-exQh39"   # bytt til din egen hvis ønskelig
STATE_FILE = "agent/state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"seen_ids": []}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def fetch_playlist_items():
    url = (
        "https://www.googleapis.com/youtube/v3/playlistItems"
        f"?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    items = []
    for entry in data.get("items", []):
        snippet = entry["snippet"]
        video_id = snippet["resourceId"]["videoId"]
        title = snippet["title"]
        description = snippet.get("description", "")
        link = f"https://www.youtube.com/watch?v={video_id}"

        items.append({
            "id": video_id,
            "title": title,
            "description": description,
            "link": link
        })

    return items

def main():
    state = load_state()
    items = fetch_playlist_items()

    new_items = [i for i in items if i["id"] not in state["seen_ids"]]

    if not new_items:
        print("Ingen nye videoer i spillelisten.")
        return

    for item in new_items:
        print(f"Ny video: {item['title']}")

        text = f"{item['title']}\n\n{item['description']}"
        summary = summarize_text(text)

        send_notification(item["title"], summary, item["link"])

        state["seen_ids"].append(item["id"])

    save_state(state)

if __name__ == "__main__":
    main()
