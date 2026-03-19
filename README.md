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
    A[Input Image / Camera] --> B[Perception]
    B --> C[Situation Interpretation]
    C --> D{Decision}
subgraph D2[Planning Phase]
    D1 -->|TTC < 1.5s| E[AEB Brake]
    D1 -->|TTC < 3s| F[ACC Slow Down]
    D1 -->|Else| G[Safe]
end

