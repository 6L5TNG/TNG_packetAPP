"""
Internationalization (I18n) module for TNG Packet APP.
Loads JSON locale files from the resources/locales/ directory.
"""

import json
from pathlib import Path


class I18n:
    """Internationalization class for loading and managing translations."""

    def __init__(self, locale="en"):
        """
        Initialize the I18n instance.

        Args:
            locale: The locale code (e.g., 'en', 'ko', 'jp'). Defaults to 'en'.
        """
        self.locale = locale
        self.translations = {}
        self._load_locale(locale)

    def _get_locales_path(self):
        """Get the path to the locales directory."""
        return Path(__file__).parent.parent / "resources" / "locales"

    def _load_locale(self, locale):
        """
        Load translations from a locale file.

        Args:
            locale: The locale code to load.
        """
        locales_path = self._get_locales_path()
        locale_file = locales_path / f"{locale}.json"

        if locale_file.exists():
            with open(locale_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        else:
            # Fall back to English if requested locale doesn't exist
            fallback_file = locales_path / "en.json"
            if fallback_file.exists():
                with open(fallback_file, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)

    def get(self, key, default=None):
        """
        Get a translation for the given key.

        Args:
            key: The translation key.
            default: Default value if key is not found.

        Returns:
            The translated string or the default value.
        """
        return self.translations.get(key, default if default is not None else key)

    def set_locale(self, locale):
        """
        Change the current locale.

        Args:
            locale: The new locale code.
        """
        self.locale = locale
        self._load_locale(locale)

    def get_available_locales(self):
        """
        Get a list of available locale codes.

        Returns:
            List of locale codes.
        """
        locales_path = self._get_locales_path()
        if locales_path.exists():
            return [f.stem for f in locales_path.glob("*.json")]
        return []
