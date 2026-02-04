import feedparser
import json
import os
from summarize import summarize_text
from notify import send_notification

FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=KANALID"  # bytt ut
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

def main():
    state = load_state()
    feed = feedparser.parse(FEED_URL)

    new_items = [
        entry for entry in feed.entries
        if entry.id not in state["seen_ids"]
    ]

    if not new_items:
        print("Ingen nye episoder.")
        return

    for item in new_items:
        title = item.title
        link = item.link
        description = getattr(item, "summary", "")

        print(f"Ny episode: {title}")

        summary = summarize_text(f"{title}\n\n{description}")

        send_notification(title, summary, link)

        state["seen_ids"].append(item.id)

    save_state(state)

if __name__ == "__main__":
    main()
