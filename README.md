# TNG Packet APP

A multi-mode amateur radio transceiver platform for packet communication.

## Overview

TNG Packet APP is designed as a modular platform where new packet protocols can be added as modules in the `modes/` directory. The application supports internationalization and provides a clean architecture for amateur radio packet communication.

## Project Structure

```
TNG_packetAPP/
├── launcher.py           # Update checker and application launcher
├── generate_bootstrap.py # Utility to bundle the project
├── version.json          # Version information
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── tng_packet/           # Main package
    ├── main.py           # Application entry point
    ├── core/             # Core modules
    │   └── i18n.py       # Internationalization support
    ├── modes/            # Packet protocol modes
    │   └── base.py       # Abstract base modem class
    └── resources/
        └── locales/      # Translation files
            ├── en.json   # English
            ├── ko.json   # Korean
            └── jp.json   # Japanese
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application using the launcher:
```bash
python launcher.py
```

Or run the main application directly:
```bash
python -m tng_packet.main
```

## Adding New Modes

To add a new packet protocol mode:

1. Create a new module in `tng_packet/modes/`
2. Inherit from `BaseModem` and implement `modulate()` and `demodulate()` methods
3. Register the mode in `tng_packet/modes/__init__.py`

## Dependencies

- numpy
- sounddevice
- scipy

## License

See LICENSE file for details.