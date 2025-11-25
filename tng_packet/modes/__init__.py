"""
TNG Packet APP Modes Module
Provides access to available packet protocol modes.
"""

from tng_packet.modes.base import BaseModem


def get_available_modes():
    """
    Get a list of available mode instances.

    Returns:
        List of mode instances that can be used for packet communication.
        New packet protocols can be added as modules in this directory
        and registered here.
    """
    modes = []
    # Future modes will be instantiated and added here
    # Example:
    # from tng_packet.modes.ax25 import AX25Modem
    # modes.append(AX25Modem())
    return modes
