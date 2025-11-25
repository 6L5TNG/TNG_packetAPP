"""
Base Modem Module for TNG Packet APP.
Defines the abstract base class for all packet protocol modes.
"""

from abc import ABC, abstractmethod


class BaseModem(ABC):
    """
    Abstract base class for packet protocol modems.

    All packet protocol implementations should inherit from this class
    and implement the modulate and demodulate methods.
    """

    @abstractmethod
    def modulate(self, text):
        """
        Modulate text data into audio signal.

        Args:
            text: The text data to modulate.

        Returns:
            Audio signal data.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement modulate()")

    @abstractmethod
    def demodulate(self, audio):
        """
        Demodulate audio signal into text data.

        Args:
            audio: The audio signal to demodulate.

        Returns:
            Decoded text data.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement demodulate()")
