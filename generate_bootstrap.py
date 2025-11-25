#!/usr/bin/env python3
"""
TNG Packet APP Bootstrap Generator
Utility script to bundle the project into a single installer file.
"""

import os
import zipfile
from pathlib import Path


def bundle_project(output_filename="tng_packet_installer.zip"):
    """Bundle the project into a single installer file."""
    project_root = Path(__file__).parent
    output_path = project_root / output_filename

    # Files and directories to include in the bundle
    include_items = [
        "launcher.py",
        "version.json",
        "requirements.txt",
        "README.md",
        "tng_packet",
    ]

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for item in include_items:
            item_path = project_root / item
            if item_path.is_file():
                zipf.write(item_path, item)
                print(f"Added file: {item}")
            elif item_path.is_dir():
                for root, dirs, files in os.walk(item_path):
                    # Skip __pycache__ directories
                    dirs[:] = [d for d in dirs if d != "__pycache__"]
                    for file in files:
                        if file.endswith(".pyc"):
                            continue
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(project_root)
                        zipf.write(file_path, arcname)
                        print(f"Added: {arcname}")

    print(f"\nBundle created: {output_path}")
    return output_path


if __name__ == "__main__":
    bundle_project()
