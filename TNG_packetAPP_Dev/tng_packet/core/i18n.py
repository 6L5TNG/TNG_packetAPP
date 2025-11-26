import json
import os

class Translator:
    _instance = None
    _data = {}

    @classmethod
    def load(cls, lang_code='en'):
        # Load JSON file from tng_packet/resources/locales
        try:
            # Get the directory of this file (tng_packet/core)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to tng_packet, then into resources/locales
            base_path = os.path.join(os.path.dirname(current_dir), 'resources', 'locales', f'{lang_code}.json')
            
            with open(base_path, 'r', encoding='utf-8') as f:
                cls._data = json.load(f)
        except Exception as e:
            print(f"Failed to load locale {lang_code}: {e}")
            cls._data = {}

    @classmethod
    def tr(cls, key):
        return cls._data.get(key, key)
