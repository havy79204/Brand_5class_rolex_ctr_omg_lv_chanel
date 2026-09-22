# Package tresnet-utils Setup Plan

## Overview

Chuyển folder `src/` thành một Python package tên `tresnet-utils` với module name `tresnet_utils`, có thể pip install trực tiếp từ git repository.

## Key Changes

### 1. Cấu trúc package mới

```
cv-model-collection/CMAL/
├── pyproject.toml          # Package configuration (NEW)
├── README.md               # Package documentation (NEW)
├── LICENSE                 # MIT License (NEW)
├── .gitignore             # Python gitignore (NEW)
├── tresnet_utils/         # Renamed from src/ (RENAMED)
│   ├── __init__.py        # Top-level exports (MODIFIED)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tresnet/
│   │   ├── tresnet_v2/
│   │   └── utils/
│   └── helper_functions/
└── [existing training files remain outside package]
```

### 2. Import path fixes

Sửa tất cả imports trong code:

- **Before**: `from src.models.tresnet.layers.xxx`
- **After**: `from tresnet_utils.models.tresnet.layers.xxx`

Files cần sửa:

- `src/models/tresnet/tresnet.py` (lines 6, 9)
- `src/models/tresnet_v2/tresnet_v2.py` (lines 9, 11)
- `src/models/tresnet_v2/layers/squeeze_and_excite.py` (line 3)

### 3. Package metadata (pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]

[project]
name = "tresnet-utils"
version = "0.1.0"
description = "TResNet models with CMAL-Net implementation for fine-grained classification"
requires-python = ">=3.7"
license = {text = "MIT"}
dependencies = [
    "torch>=1.8.0",
    "torchvision>=0.9.0",
    "numpy"
]

[project.readme]
file = "README.md"
content-type = "text/markdown"
```

### 4. Top-level API exports

File `tresnet_utils/__init__.py` sẽ expose:

```python
from .models import create_model
from .models.tresnet import TResnetM, TResnetL, TResnetXL
from .models.tresnet_v2 import TResnetL_V2
from .helper_functions.helper_functions import (
    create_dataloader, accuracy, AverageMeter, validate
)
```

### 5. Installation instructions

Users sẽ có thể install bằng:

```bash
pip install git+https://github.com/YOUR_USERNAME/YOUR_REPO.git@branch#subdirectory=cv-model-collection/CMAL
```

## Notes

- `inplace_abn` dependency phải được cài riêng trước (user tự cài)
- Training scripts (`train_*.py`, `network_wrapper.py`, etc.) vẫn ở ngoài package để tham khảo
- Package chỉ chứa core models và utilities, không bao gồm training code