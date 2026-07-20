import json
import os
import re
import shutil
from datetime import datetime

_APP_NAME = "poe2-mirror-crafter"


def _get_appdata_dir():
    appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
    path = os.path.join(appdata, _APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path


def get_saves_dir():
    path = os.path.join(_get_appdata_dir(), "saves")
    os.makedirs(path, exist_ok=True)
    return path


def migrate_saves_from_legacy():
    legacy_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
    target_dir = get_saves_dir()
    moved = 0

    old_appdata = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "poe2-crafting", "saves")
    if os.path.isdir(old_appdata):
        for entry in os.listdir(old_appdata):
            if not entry.endswith(".json"):
                continue
            src = os.path.join(old_appdata, entry)
            dst = os.path.join(target_dir, entry)
            if os.path.isfile(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)
                moved += 1

    if not os.path.isdir(legacy_dir):
        return moved

    for entry in os.listdir(legacy_dir):
        if not entry.endswith(".json"):
            continue
        src = os.path.join(legacy_dir, entry)
        dst = os.path.join(target_dir, entry)
        if os.path.isfile(src):
            shutil.move(src, dst)
            moved += 1
    try:
        remaining = os.listdir(legacy_dir)
        if not remaining:
            os.rmdir(legacy_dir)
    except OSError:
        pass
    return moved


def list_saves():
    saves_dir = get_saves_dir()
    results = []
    try:
        entries = os.listdir(saves_dir)
    except OSError:
        return results

    for entry in entries:
        if not entry.endswith(".json"):
            continue
        filepath = os.path.join(saves_dir, entry)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        results.append({
            "filename": entry,
            "display_name": data.get("display_name", entry),
            "date": data.get("saved_at", ""),
            "category": data.get("category", ""),
            "sub_type": data.get("sub_type", ""),
            "phase": data.get("current_phase", 0),
            "step": data.get("current_step", 0),
            "steps_complete": len(data.get("completed_steps", [])),
        })

    results.sort(key=lambda r: r["date"], reverse=True)
    return results


def save_state(filename, state_dict):
    state_dict.setdefault("saved_at", datetime.now().isoformat())
    if "display_name" not in state_dict:
        cat = state_dict.get("category", "")
        sub = state_dict.get("sub_type", "")
        state_dict["display_name"] = f"{cat} \u2014 {sub}" if sub else cat

    saves_dir = get_saves_dir()
    filepath = os.path.join(saves_dir, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(state_dict, f, indent=2, ensure_ascii=False)
        return True
    except OSError:
        return False


def load_state(filename):
    saves_dir = get_saves_dir()
    filepath = os.path.join(saves_dir, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def delete_save(filename):
    saves_dir = get_saves_dir()
    filepath = os.path.join(saves_dir, filename)
    try:
        os.remove(filepath)
        return True
    except OSError:
        return False


def auto_save_filename(category, sub_type):
    def sanitize(s):
        return re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_")

    parts = ["craft"]
    if category:
        parts.append(sanitize(category))
    if sub_type:
        parts.append(sanitize(sub_type))
    return "_".join(parts) + ".json"
