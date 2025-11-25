#!/usr/bin/env python3
"""
TNG Packet APP Main Entry Point
A multi-mode amateur radio transceiver platform.
"""

from tng_packet.core.i18n import I18n
from tng_packet.modes import get_available_modes


def main():
    """Main application entry point."""
    # Initialize internationalization
    i18n = I18n()

    # Display application title
    print(i18n.get("app_title"))

    # List available modes
    modes = get_available_modes()
    print(f"\nAvailable modes: {len(modes)}")
    for mode in modes:
        print(f"  - {mode.__class__.__name__}")

    if not modes:
        print("  No modes currently registered.")
        print("  Add new packet protocols as modules in the modes/ directory.")


if __name__ == "__main__":
    main()
