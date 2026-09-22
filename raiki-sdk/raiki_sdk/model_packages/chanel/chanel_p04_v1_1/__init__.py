"""
Chanel P04 V1.1 Model Package

This package provides detector and authenticator for Chanel P04 models version 1.1.
"""

def get_detector(device: str):
    """
    Factory function to create detector instance
    
    Returns:
        ChanelP04Detector: Detector instance
    """
    from .detector import ChanelP04Detector
    return ChanelP04Detector(device)

def get_main_model(device: str):
    """
    Factory function to create authenticator instance
        
    Returns:
        ChanelP04Authenticator: Authenticator instance
    """
    from .authenticator import ChanelP04Authenticator
    return ChanelP04Authenticator(device)

__all__ = ['get_detector', 'get_main_model']