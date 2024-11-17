import json
import os

JSON_FILE = 'messages.json'

def save_message(text: str) -> None:
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            messages = json.load(f)
    else:
        messages = []

    messages.append(text)

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)
        