#!/bin/bash

# Lux-Authen-API Update raiki-sdk Script

set -e # Exit on error

echo "1. Upgrading raiki-sdk..."
uv pip install --upgrade git+ssh://git@gitlab.com/dat.tram/raiki-sdk.git

echo "2. Installing transformers and peft..."
uv pip install "transformers>=4.56,<5" "peft==0.18.0"

echo "3. Installing torch with CUDA 12.1..."
uv pip install torch==2.3.0+cu121 torchvision==0.18.0+cu121 torchaudio==2.3.0+cu121 -f https://download.pytorch.org/whl/torch_stable.html

echo "Update completed successfully!"
