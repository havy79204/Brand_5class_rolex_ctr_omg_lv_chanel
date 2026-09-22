import torch
import torch.nn as nn
import timm

class Maxvit(nn.Module):
    def __init__(self, num_classes=2, model_name='maxvit_small_tf_512.in1k',  # Dùng bản Small (cho ra 768 chiều)
                 pretrained=False, checkpoint=None, device='cpu'):
        super(Maxvit, self).__init__()

        self.backbone = timm.create_model(model_name, pretrained=pretrained, in_chans=3)

        in_features = self.backbone.num_features  # Sẽ tự động là 768

        self.backbone.reset_classifier(num_classes=0)

        # Lớp classifier khớp hoàn toàn với checkpoint (768 -> 1024 -> 512 -> num_classes)
        self.classifier = nn.Sequential(
            nn.Linear(in_features, 1024),
            nn.BatchNorm1d(1024),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

        if checkpoint is not None:
            state_dict = torch.load(checkpoint, map_location=device)
            self.load_state_dict(state_dict)

    def forward(self, x):
        features = self.backbone(x)
        output = self.classifier(features)
        return output