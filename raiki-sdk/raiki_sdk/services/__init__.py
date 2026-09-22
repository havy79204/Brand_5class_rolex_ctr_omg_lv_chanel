"""Services for specialized detection tasks."""

from .brand_detection import BrandDetectionService, DetectionResult
import logging
from typing import Optional
_logger = logging.getLogger(__name__)

# Global cache for BrandDetectionService
_brand_detection_cache: Optional[BrandDetectionService] = None


def get_brand_detection_service(
    device: str = "cuda"
) -> BrandDetectionService:
    """
    Get cached BrandDetectionService instance.
    
    Args:
        device: "cuda", "mps", or "cpu"
    
    Returns:
        BrandDetectionService: Cached service instance
    
    Example:
        >>> from raiki_sdk import get_brand_detection_service
        >>> service = get_brand_detection_service(device="cuda")
        >>> result = service.detect(image)
        >>> if result:
        ...     print(f"Detected: {result.category}")
    """
    global _brand_detection_cache
    if _brand_detection_cache is None:
        _logger.info(f"Creating new BrandDetectionService on {device}")
        _brand_detection_cache = BrandDetectionService(device=device)
    return _brand_detection_cache


__all__ = [
    "get_brand_detection_service",
    "BrandDetectionService",
    "DetectionResult",
]