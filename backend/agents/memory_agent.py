import json
from pathlib import Path
from threading import Lock

class MemoryAgent:
    def __init__(self, path="../data/memory_db.json"):
        self.path = Path(path)
        self.lock = Lock()
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps({}))
        self._load()

    def _load(self):
        with self.lock:
            self.data = json.loads(self.path.read_text())

    def _save(self):
        with self.lock:
            self.path.write_text(json.dumps(self.data, indent=2))

    def get_user(self, user_id):
        return self.data.get(user_id, {"profile": {}, "moods": [], "notes": []})

    def set_user(self, user_id, payload):
        self.data[user_id] = payload
        self._save()

    def add_mood(self, user_id, mood):
        u = self.get_user(user_id)
        u.setdefault("moods", []).append(mood)
        self.set_user(user_id, u)

    def add_note(self, user_id, note):
        u = self.get_user(user_id)
        u.setdefault("notes", []).append(note)
        self.set_user(user_id, u)

    def update_profile(self, user_id, profile):
        u = self.get_user(user_id)
        u["profile"].update(profile)
        self.set_user(user_id, u)
