import json
import os

SETTINGS_FILE = 'tng_settings.json'

DEFAULT_SETTINGS = {
    'callsign': 'NOCALL',
    'grid': 'PM37',
    'tracks': 4,
    'speed': 10,
    'audio_in': None,
    'audio_out': None,
    'theme': 'dark'
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Update defaults with loaded data
            settings = DEFAULT_SETTINGS.copy()
            settings.update(data)
            return settings
    except Exception:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f'Error saving settings: {e}')
