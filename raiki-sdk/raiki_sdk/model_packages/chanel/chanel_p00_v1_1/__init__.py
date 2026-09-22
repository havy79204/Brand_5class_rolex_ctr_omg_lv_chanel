"""
Chanel P00 V1.1 Model Package

This package provides detector and authenticator for Chanel P00 models version 1.1.
"""

def get_detector(device: str):
    """
    Factory function to create detector instance

    Returns:
        ChanelP00Detector: Detector instance
    """
    from .detector import ChanelP00Detector
    return ChanelP00Detector(device)

def get_main_model(device: str):
    """
    Factory function to create classifier instance

    Returns:
        ChanelP00Classificator: Classifier instance
    """
    from .classifier import ChanelP00Classificator
    return ChanelP00Classificator(device)

__all__ = ['get_detector', 'get_main_model']