# ADAS 1V Solution AEB/ACC Demo

## Overview
This project demonstrates:
- YOLOv8 object detection
- Distance estimation using bounding boxes
- Time-to-Collision (TTC)
- AEB and ACC decision logic

## Run
pip install ultralytics opencv-python
python your_script.py

## Env Setup
### System Setup
- Ubuntu 20.04.6 LTS
### Conda Installation
- Download Miniconda -->         wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
- Install -->                  bash Miniconda3-latest-Linux-x86_64.sh
- Restart terminal or run -->   source ~/.bashrc
- Verify -->                 conda --version

### Yolo & Dependencies Installation
  - pip install ultralytics
  - pip install opencv-python numpy

### Flowchart
```mermaid
flowchart LR
    A[Input Image / Camera] --> B[YOLOv8 Detection]
    B --> C[Vehicle Filtering]
    C --> D[Lead Vehicle Selection]
    D --> E[Distance Estimation]
    E --> F[Relative Speed Calculation]
    F --> G[TTC Computation]
    G --> H{Decision}
    H -->|TTC < 1.5s| I[AEB Brake]
    H -->|TTC < 3s| J[ACC Slow Down]
    H -->|Else| K[Safe]
