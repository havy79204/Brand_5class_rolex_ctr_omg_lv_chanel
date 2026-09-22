# TResNet Utils

TResNet models with CMAL-Net (Cross-layer Mutual Attention Learning) implementation for fine-grained visual classification.

## Overview

This package provides implementations of:
- **TResNet** (TResNet-M, TResNet-L, TResNet-XL) - Efficient image classification models
- **TResNet-V2** (TResNet-L-V2) - Improved version with enhanced features
- **CMAL-Net** - Cross-layer Mutual Attention Learning for fine-grained classification

Based on the paper: *"Learn from each other to Classify better: Cross-layer mutual attention learning for fine-grained visual classification"* published in Pattern Recognition (2023).

## Requirements

- Python >= 3.7
- numpy >= 2.2.6,
- timm >= 1.0.20,

### Additional Dependencies (Manual Installation Required)

This package requires `inplace-abn` which must be installed separately:

```bash
pip install git+https://github.com/mapillary/inplace_abn.git
```

For detailed installation instructions, see: [InPlace-ABN Installation Guide](https://github.com/Alibaba-MIIL/TResNet/blob/master/INPLACE_ABN_TIPS.md)

## Installation

### Install from Git

```bash
pip install git+https://gitlab.com/dat.tram/tresnet-utils.git
```

### Install in Development Mode

```bash
git clone https://gitlab.com/dat.tram/tresnet-utils.git
cd tresnet-utils
pip install -e .
```

## Quick Start

### Basic Usage

```python
import torch
from tresnet_utils import create_model, TResnetL
from argparse import Namespace

# Method 1: Using create_model factory
args = Namespace(
    model_name='tresnet_l',
    num_classes=196,  # e.g., Stanford Cars dataset
    remove_aa_jit=False
)
model = create_model(args)

# Method 2: Direct model instantiation
model_params = {
    'num_classes': 196,
    'remove_aa_jit': False,
    'args': args
}
model = TResnetL(model_params)

# Load weights (if available)
# checkpoint = torch.load('path/to/checkpoint.pth')
# model.load_state_dict(checkpoint['state_dict'])

# Set to evaluation mode
model.eval()

# Inference
with torch.no_grad():
    output = model(torch.randn(1, 3, 448, 448))
    print(f"Output shape: {output.shape}")
```

### Available Models

```python
from tresnet_utils import TResnetM, TResnetL, TResnetXL, TResnetL_V2

# TResNet variants
model_params = {'num_classes': 1000, 'remove_aa_jit': False, 'args': args}

# Medium model (TResNet-M)
model_m = TResnetM(model_params)

# Large model (TResNet-L)
model_l = TResnetL(model_params)

# Extra-large model (TResNet-XL)
model_xl = TResnetXL(model_params)

# TResNet-L V2
model_v2 = TResnetL_V2(model_params)
```

### Using Helper Functions

```python
from tresnet_utils import create_dataloader, validate, accuracy, AverageMeter
from argparse import Namespace

# Create dataloader
args = Namespace(
    val_dir='path/to/validation/dataset',
    batch_size=32,
    input_size=448,
    val_zoom_factor=0.875,
    num_workers=4
)

val_loader = create_dataloader(args)

# Validate model
model.cuda()
results = validate(model, val_loader)
print(f"Validation Accuracy: {results.avg:.2f}%")
```

## Model Architecture

### TResNet Features:
- Space-to-depth stem for efficient processing
- Anti-aliasing downsampling layers
- Squeeze-and-excitation (SE) modules
- In-place Activated Batch Normalization (InPlace-ABN)

### CMAL-Net Features:
- Cross-layer mutual attention mechanism
- Multi-scale feature extraction
- Fine-grained classification capabilities

## Training

For training your own models, please refer to the training scripts in the original repository:
- `train_Stanford_Cars_TResNet_L.py` - Stanford Cars dataset
- `train_FGVC_Aircraft_ResNet50.py` - FGVC Aircraft dataset  
- `train_Food_11_ResNet50.py` - Food-11 dataset

## Citation

If you use this code in your research, please cite:

```bibtex
@article{LIU2023109550,
    title = {Learn from each other to Classify better: Cross-layer mutual attention learning for fine-grained visual classification},
    journal = {Pattern Recognition},
    volume = {140},
    pages = {109550},
    year = {2023},
    issn = {0031-3203},
    doi = {https://doi.org/10.1016/j.patcog.2023.109550},
    url = {https://www.sciencedirect.com/science/article/pii/S0031320323002509},
    author = {Dichao Liu and Longjiao Zhao and Yu Wang and Jien Kato}
}
```

## Acknowledgments

- Original CMAL-Net implementation: [CMAL GitHub Repository](https://github.com/Dichao-Liu/CMAL)
- TResNet implementation: [Alibaba-MIIL TResNet](https://github.com/Alibaba-MIIL/TResNet)
- Training code inspired by: [PMG Progressive Multi-Granularity Training](https://github.com/PRIS-CV/PMG-Progressive-Multi-Granularity-Training)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Open an issue on [GitLab](https://gitlab.com/dat.tram/tresnet-utils/-/issues)
- Check the original paper for methodology details

## Project Status

This package is actively maintained. Contributions and feedback are welcome!
