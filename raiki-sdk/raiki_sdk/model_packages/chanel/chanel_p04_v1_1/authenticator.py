"""
Authenticator for Chanel P04

Handles authentication logic using trained model.
"""

from raiki_sdk.base import AuthenticateBase, AuthResult
from .config import (
    AUTH_WEIGHTS, AUTH_CLASS_LABELS,
    AUTH_MODEL_NAME, AUTH_MODEL_VERSION,
    YOLO_MODEL_VERSION, AUTH_NUM_CLASSES)
from .architecture import Maxvit
from .preprocessor import get_transform
import torch
from typing import Tuple
from PIL import Image

class ChanelP04Authenticator(AuthenticateBase):
    """
    Authentication model for Chanel P04
    """

    def __init__(self, device: str):
        self.device = device
        self.model = Maxvit(num_classes=AUTH_NUM_CLASSES, checkpoint=AUTH_WEIGHTS, device=device).to(self.device).eval()
        self.transform = get_transform()

        self.metadata = {
            "auth_model_name": AUTH_MODEL_NAME,
            "auth_class_labels": AUTH_CLASS_LABELS,
            "auth_model_version": AUTH_MODEL_VERSION,
            "yolo_model_version": YOLO_MODEL_VERSION
        }

    def forward(self, image: Image.Image) -> AuthResult:
        with torch.no_grad():
            tensor_image = self.transform(image).unsqueeze(0).to(self.device)
            logits = self.model(tensor_image)
            probs = torch.softmax(logits, -1).squeeze(0)
            probs, label = self.get_prob(probs)
            metadata = self.metadata

            return AuthResult(probability=probs, label=label, metadata=metadata)

    def get_prob(self, probs: torch.Tensor) -> Tuple[float, str]:
        index = torch.argmax(probs, -1)
        label = AUTH_CLASS_LABELS[index]

        # Logic cho 2 lớp: ['fake', 'real']
        if index == 1:  # real
            return max(0.7, probs[index].item()), f"{probs[index].item():.4f}-{label}"
        else:  # fake (index == 0)
            return max(0.5, 1.0 - probs[index].item()), f"{probs[index].item():.4f}-{label}"

    def generate_heatmap(self) -> Image.Image:
        pass