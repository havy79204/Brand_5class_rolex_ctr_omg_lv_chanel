"""
TResNet Utils - TResNet models with CMAL-Net implementation

This package provides TResNet model implementations along with CMAL-Net
(Cross-layer Mutual Attention Learning) for fine-grained visual classification.
"""

__version__ = "0.1.0"

# Import model factory and models
from tresnet_utils.models import create_model
from tresnet_utils.models.tresnet import TResnetM, TResnetL, TResnetXL
from tresnet_utils.models.tresnet_v2 import TResnetL_V2

# Import helper functions
from tresnet_utils.helper_functions.helper_functions import (
    create_dataloader,
    accuracy,
    AverageMeter,
    validate
)

__all__ = [
    # Version
    '__version__',
    # Model factory
    'create_model',
    # TResNet models
    'TResnetM',
    'TResnetL',
    'TResnetXL',
    'TResnetL_V2',
    # Helper functions
    'create_dataloader',
    'accuracy',
    'AverageMeter',
    'validate',
]

