#!/usr/bin/env python3
"""
TNG Packet APP Launcher
Checks for updates and launches the main application.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def check_for_updates():
    """Placeholder for update checking logic."""
    version_file = Path(__file__).parent / "version.json"
    if version_file.exists():
        with open(version_file, "r", encoding="utf-8") as f:
            version_data = json.load(f)
            print(f"Current version: {version_data.get('version', 'unknown')}")
    # TODO: Implement actual update checking logic
    print("Checking for updates... (placeholder)")
    return False


def launch_main():
    """Launch the main application."""
    project_root = Path(__file__).parent
    main_script = project_root / "tng_packet" / "main.py"
    if main_script.exists():
        env = dict(os.environ)
        # Add project root to PYTHONPATH for module imports
        python_path = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(project_root) + (os.pathsep + python_path if python_path else "")
        subprocess.run([sys.executable, str(main_script)], check=True, env=env)
    else:
        print(f"Error: Main script not found at {main_script}")
        sys.exit(1)


if __name__ == "__main__":
    check_for_updates()
    launch_main()
