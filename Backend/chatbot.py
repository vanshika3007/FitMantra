
import json, os
from difflib import SequenceMatcher

DATASET_PATHS = [
    os.path.join(os.path.dirname(__file__), "dataset.json"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset", "Fitness_Chatbot.json")
]

def _load_dataset():
    data = None
    for p in DATASET_PATHS:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    break
                except json.JSONDecodeError:
                    continue
    return data or []

DATASET = _load_dataset()

def _similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_bot_response(user_input: str) -> str:
    if not DATASET:
        return "Dataset not found. Please add dataset.json."

    # Support two formats:
    # 1) {"intents": [{"patterns": [...], "responses": [...]}]}
    # 2) [{"prompt": "text", "response": "text"}]
    best_resp = None
    best_score = 0.55

    # Format 1
    if isinstance(DATASET, dict) and "intents" in DATASET:
        for intent in DATASET.get("intents", []):
            for pat in intent.get("patterns", []):
                score = _similar(user_input, pat)
                if score > best_score:
                    best_score = score
                    resp_list = intent.get("responses") or []
                    best_resp = resp_list[0] if resp_list else None
    else:
        # Format 2
        for item in DATASET:
            prompt = item.get("prompt", "")
            score = _similar(user_input, prompt)
            if score > best_score:
                best_score = score
                best_resp = item.get("response")

    return best_resp or "Sorry, I didn’t understand. Could you rephrase?"
