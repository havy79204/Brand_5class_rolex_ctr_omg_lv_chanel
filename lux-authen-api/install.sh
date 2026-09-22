#!/bin/bash

# Lux-Authen-API Installation Script (Core dependencies only)

set -e # Exit on error

echo "1. Installing raiki-sdk..."
uv pip install git+ssh://git@gitlab.com/dat.tram/raiki-sdk.git

echo "2. Installing requirements.txt..."
uv pip install -r requirements.txt

echo "3. Installing transformers and peft..."
uv pip install "transformers>=4.56,<5" "peft==0.18.0"

echo "4. Installing torch with CUDA 12.1..."
uv pip install torch==2.3.0+cu121 torchvision==0.18.0+cu121 torchaudio==2.3.0+cu121 -f https://download.pytorch.org/whl/torch_stable.html

echo "5. Installing inplace_abn..."
uv pip install git+https://github.com/mapillary/inplace_abn.git@v1.1.0 --no-build-isolation

echo "6. Installing websockets..."
uv pip install websockets==15.0.1

echo "7. Installing clip..."
uv pip install clip==0.2.0

echo "Installation completed successfully!"
