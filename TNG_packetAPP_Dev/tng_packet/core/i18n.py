import json
import os
from pathlib import Path

class I18n:
    def __init__(self, lang_code="en"):
        self.lang = lang_code
        self.data = {}
        self.load_locale(lang_code)
    
    def load_locale(self, code):
        # locales 폴더 위치 찾기
        path = Path(__file__).parent.parent / "resources" / "locales" / f"{code}.json"
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"[Warn] {code} 언어 파일을 찾을 수 없어 영어를 시도합니다.")
            if code != "en":
                self.load_locale("en")

    def get(self, key):
        return self.data.get(key, key)
